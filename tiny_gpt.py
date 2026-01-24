"""
Tiny GPT - Complete Training Example

This shows how LLMs actually LEARN patterns from data.
Key insight: It learns to predict the next character based on patterns,
but has NO concept of truth, logic, or facts.

This demonstrates WHY Frankenstein's Logic Filter is necessary.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F

# ----- Config -----
device      = "cuda" if torch.cuda.is_available() else "cpu"
block_size  = 32      # Reduced context length for small dataset
batch_size  = 8       # Reduced batch size
n_layers    = 2
n_heads     = 4
d_model     = 64      # Reduced model size
d_ff        = 4 * d_model
dropout     = 0.1
max_iters   = 300     # Fewer iterations
lr          = 3e-4

# ----- Tiny dataset (character-level) -----
text = """
In the beginning was the Word, and the Word was with code, and the Word was code.
This is a tiny corpus for a tiny GPT. We need more text to train properly.
The quick brown fox jumps over the lazy dog. Cats are mammals. Dogs are animals.
Logic is the foundation of reasoning. Patterns emerge from data. Truth requires proof.
Artificial intelligence learns from examples. Neural networks process information.
Transformers use attention mechanisms. Language models predict next tokens.
Machine learning finds patterns in data. Deep learning uses multiple layers.
Knowledge comes from experience. Understanding requires context and meaning.
The sun rises in the east. Water flows downhill. Fire needs oxygen to burn.
Mathematics is the language of science. Physics describes natural laws.
Chemistry studies matter and its transformations. Biology explores living systems.
"""

chars = sorted(list(set(text)))
vocab_size = len(chars)
stoi = {ch: i for i, ch in enumerate(chars)}
itos = {i: ch for ch, i in stoi.items()}

def encode(s): return torch.tensor([stoi[c] for c in s], dtype=torch.long)
def decode(t): return ''.join(itos[int(i)] for i in t)

data = encode(text)
print(f"Total data length: {len(data)} characters")

# Need enough data for validation
if len(data) < block_size * 2:
    print(f"ERROR: Dataset too small. Need at least {block_size * 2} characters, have {len(data)}")
    print("Expanding dataset by repeating...")
    # Repeat text to make it large enough
    text = text * 10
    data = encode(text)
    print(f"New data length: {len(data)} characters")

n = int(0.9 * len(data))
train_data = data[:n]
val_data   = data[n:]

print(f"Train data: {len(train_data)} characters")
print(f"Val data: {len(val_data)} characters")

def get_batch(split):
    d = train_data if split == "train" else val_data
    ix = torch.randint(len(d) - block_size, (batch_size,))
    x = torch.stack([d[i:i+block_size] for i in ix])
    y = torch.stack([d[i+1:i+block_size+1] for i in ix])
    return x.to(device), y.to(device)

# ----- Model components -----
class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=block_size):
        super().__init__()
        pos = torch.arange(0, max_len).unsqueeze(1)
        i   = torch.arange(0, d_model, 2)
        div = torch.exp(-torch.log(torch.tensor(10000.0)) * i / d_model)
        pe  = torch.zeros(max_len, d_model)
        pe[:, 0::2] = torch.sin(pos * div)
        pe[:, 1::2] = torch.cos(pos * div)
        self.register_buffer("pe", pe.unsqueeze(0))

    def forward(self, x):
        return x + self.pe[:, :x.size(1), :]

class CausalSelfAttention(nn.Module):
    def __init__(self, d_model, n_heads):
        super().__init__()
        assert d_model % n_heads == 0
        self.n_heads = n_heads
        self.head_dim = d_model // n_heads
        self.qkv = nn.Linear(d_model, 3 * d_model)
        self.proj = nn.Linear(d_model, d_model)
        self.dropout = nn.Dropout(dropout)
        self.register_buffer(
            "mask",
            torch.tril(torch.ones(block_size, block_size)).unsqueeze(0).unsqueeze(0)
        )

    def forward(self, x):
        B, T, C = x.size()
        qkv = self.qkv(x)  # (B, T, 3C)
        q, k, v = qkv.chunk(3, dim=-1)

        def split_heads(t):
            return t.view(B, T, self.n_heads, self.head_dim).transpose(1, 2)

        q = split_heads(q)
        k = split_heads(k)
        v = split_heads(v)

        att = (q @ k.transpose(-2, -1)) / (self.head_dim ** 0.5)
        att = att.masked_fill(self.mask[:, :, :T, :T] == 0, float("-inf"))
        att = F.softmax(att, dim=-1)
        att = self.dropout(att)
        out = att @ v  # (B, n_heads, T, head_dim)
        out = out.transpose(1, 2).contiguous().view(B, T, C)
        return self.proj(out)

class Block(nn.Module):
    def __init__(self, d_model, n_heads):
        super().__init__()
        self.ln1 = nn.LayerNorm(d_model)
        self.ln2 = nn.LayerNorm(d_model)
        self.attn = CausalSelfAttention(d_model, n_heads)
        self.ff = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.GELU(),
            nn.Linear(d_ff, d_model),
            nn.Dropout(dropout),
        )

    def forward(self, x):
        x = x + self.attn(self.ln1(x))
        x = x + self.ff(self.ln2(x))
        return x

class TinyGPT(nn.Module):
    def __init__(self):
        super().__init__()
        self.token_emb = nn.Embedding(vocab_size, d_model)
        self.pos_enc   = PositionalEncoding(d_model)
        self.blocks    = nn.ModuleList([Block(d_model, n_heads) for _ in range(n_layers)])
        self.ln_f      = nn.LayerNorm(d_model)
        self.head      = nn.Linear(d_model, vocab_size, bias=False)

    def forward(self, idx, targets=None):
        x = self.token_emb(idx)
        x = self.pos_enc(x)
        for blk in self.blocks:
            x = blk(x)
        x = self.ln_f(x)
        logits = self.head(x)

        if targets is None:
            return logits, None

        B, T, C = logits.shape
        loss = F.cross_entropy(logits.view(B*T, C), targets.view(B*T))
        return logits, loss

    @torch.no_grad()
    def generate(self, idx, max_new_tokens, temperature=1.0, top_k=None):
        for _ in range(max_new_tokens):
            idx_cond = idx[:, -block_size:]
            logits, _ = self(idx_cond)
            logits = logits[:, -1, :] / temperature
            if top_k is not None:
                v, _ = torch.topk(logits, top_k)
                logits[logits < v[:, [-1]]] = -float("inf")
            probs = F.softmax(logits, dim=-1)
            next_token = torch.multinomial(probs, num_samples=1)
            idx = torch.cat((idx, next_token), dim=1)
        return idx


def explain_what_this_shows():
    """Explain what this code demonstrates"""
    print("=" * 70)
    print("WHAT THIS CODE SHOWS")
    print("=" * 70)
    print()
    print("This is a COMPLETE GPT implementation that:")
    print("  1. Takes text as input")
    print("  2. Learns patterns in that text")
    print("  3. Generates new text based on those patterns")
    print()
    print("Training data: 'In the beginning was the Word...'")
    print()
    print("The model learns:")
    print("  - After 'the' often comes 'Word'")
    print("  - After 'was' often comes 'the' or 'with' or 'code'")
    print("  - Patterns of character sequences")
    print()
    print("=" * 70)
    print("WHAT IT DOES NOT LEARN")
    print("=" * 70)
    print()
    print("  X What 'Word' means")
    print("  X What 'code' means")
    print("  X Whether statements are true or false")
    print("  X Logical relationships")
    print("  X How to verify facts")
    print()
    print("It's PURE pattern matching - no understanding!")
    print()
    print("=" * 70)
    print("THE FRANKENSTEIN INSIGHT")
    print("=" * 70)
    print()
    print("If we train this on:")
    print("  'Cats are mammals' (100 times)")
    print("  'Cats are fish' (10 times)")
    print()
    print("The model learns: 'Cats are mammals' is more likely")
    print()
    print("But if we train on:")
    print("  'Cats are fish' (100 times)")
    print("  'Cats are mammals' (10 times)")
    print()
    print("The model learns: 'Cats are fish' is more likely")
    print()
    print("IT HAS NO CONCEPT OF TRUTH!")
    print()
    print("That's why we need Frankenstein:")
    print("  - LLM generates text based on patterns")
    print("  - Frankenstein validates against ACTUAL FACTS")
    print("  - Logic is master, not training data frequency")
    print()


if __name__ == "__main__":
    explain_what_this_shows()
    
    print("=" * 70)
    print("TRAINING THE MODEL")
    print("=" * 70)
    print()
    print(f"Device: {device}")
    print(f"Vocabulary size: {vocab_size} characters")
    print(f"Training data length: {len(train_data)} characters")
    print()
    
    model = TinyGPT().to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr)

    # ----- Training loop -----
    for step in range(max_iters):
        model.train()
        xb, yb = get_batch("train")
        logits, loss = model(xb, yb)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        optimizer.step()

        if step % 100 == 0:
            model.eval()
            with torch.no_grad():
                xb_val, yb_val = get_batch("val")
                _, val_loss = model(xb_val, yb_val)
            print(f"step {step}: train loss {loss.item():.3f}, val loss {val_loss.item():.3f}")

    # ----- Generate -----
    print()
    print("=" * 70)
    print("GENERATED TEXT (based on learned patterns)")
    print("=" * 70)
    print()
    
    model.eval()
    start = torch.randint(0, vocab_size, (1, 1), device=device)
    out = model.generate(start, max_new_tokens=200, temperature=0.8, top_k=20)
    generated = decode(out[0].cpu())
    print(generated)
    print()
    
    print("=" * 70)
    print("ANALYSIS")
    print("=" * 70)
    print()
    print("The generated text:")
    print("  - Mimics the style of training data")
    print("  - Uses similar words and patterns")
    print("  - May be grammatically correct")
    print()
    print("But it:")
    print("  X Has no understanding of meaning")
    print("  X Cannot verify if statements are true")
    print("  X Cannot detect contradictions")
    print("  X Cannot reason logically")
    print()
    print("This is why Frankenstein's Logic Filter is essential:")
    print("  - Use LLM for language generation (what it's good at)")
    print("  - Add Frankenstein for logical validation (what LLMs lack)")
    print("  - Result: Powerful language + Logical correctness")
    print()
