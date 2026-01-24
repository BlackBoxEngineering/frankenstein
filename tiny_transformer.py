"""
Tiny Transformer - Understanding AI Mechanics

This is a minimal transformer model to understand how LLMs work.
It shows the core components that make AI "intelligent" - but also why
Frankenstein's Logic Filter is necessary.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F

class TinyTransformer(nn.Module):
    def __init__(self, vocab_size=1000, d_model=64, n_heads=4):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, d_model)

        # Multi-head attention
        self.attn = nn.MultiheadAttention(d_model, n_heads, batch_first=True)

        # Feed-forward network
        self.ff = nn.Sequential(
            nn.Linear(d_model, d_model * 4),
            nn.ReLU(),
            nn.Linear(d_model * 4, d_model)
        )

        # Layer norms
        self.ln1 = nn.LayerNorm(d_model)
        self.ln2 = nn.LayerNorm(d_model)

        # Output projection
        self.out = nn.Linear(d_model, vocab_size)

    def forward(self, x):
        # 1. Embed tokens
        x = self.embed(x)

        # 2. Self-attention + residual + norm
        attn_out, _ = self.attn(x, x, x)
        x = self.ln1(x + attn_out)

        # 3. Feed-forward + residual + norm
        ff_out = self.ff(x)
        x = self.ln2(x + ff_out)

        # 4. Project to logits
        return self.out(x)


def explain_transformer():
    """Explain what each component does"""
    print("=" * 60)
    print("UNDERSTANDING TRANSFORMERS")
    print("=" * 60)
    print()
    
    print("1. EMBEDDING (nn.Embedding)")
    print("   - Converts tokens (words) into vectors")
    print("   - 'cat' -> [0.2, -0.5, 0.8, ...]")
    print("   - Similar words have similar vectors")
    print()
    
    print("2. ATTENTION (nn.MultiheadAttention)")
    print("   - Looks at relationships between words")
    print("   - 'The cat sat on the mat'")
    print("   - 'cat' pays attention to 'sat' and 'mat'")
    print("   - This is pattern matching, NOT logic")
    print()
    
    print("3. FEED-FORWARD (nn.Linear + ReLU)")
    print("   - Transforms the attended information")
    print("   - Learns patterns from training data")
    print("   - Again: patterns, not logic")
    print()
    
    print("4. OUTPUT (nn.Linear)")
    print("   - Predicts next token probabilities")
    print("   - 'The cat sat on the ___'")
    print("   - High probability: 'mat', 'floor', 'chair'")
    print("   - Based on training data patterns")
    print()
    
    print("=" * 60)
    print("THE PROBLEM")
    print("=" * 60)
    print()
    print("Transformers learn PATTERNS, not LOGIC:")
    print()
    print("If training data says:")
    print("  'Cats are mammals' (1000 times)")
    print("  'Cats are fish' (10 times)")
    print()
    print("The model learns: 'Cats are mammals' is more likely")
    print("But it doesn't KNOW why. It's just pattern frequency.")
    print()
    print("It can't:")
    print("  - Prove 'cats are mammals' is TRUE")
    print("  - Prove 'cats are fish' is FALSE")
    print("  - Detect logical contradictions")
    print("  - Derive conclusions from premises")
    print()
    
    print("=" * 60)
    print("WHY FRANKENSTEIN IS NEEDED")
    print("=" * 60)
    print()
    print("Frankenstein adds the LOGIC LAYER:")
    print()
    print("LLM says: 'Cats are mammals that breathe underwater'")
    print("           ↓")
    print("Frankenstein extracts claims:")
    print("  1. 'Cats are mammals' -> Check knowledge base")
    print("  2. 'Cats breathe underwater' -> Check knowledge base")
    print("           ↓")
    print("Validation:")
    print("  1. TRUE - Cats ARE mammals (biological taxonomy)")
    print("  2. FALSE - Mammals breathe air, not water")
    print("           ↓")
    print("Result: REFUSE with proof")
    print()
    print("The LLM provides reasoning POWER.")
    print("Frankenstein provides logical VALIDATION.")
    print()
    print("Together: Powerful reasoning + Logical correctness")
    print()


def run_example():
    """Run the tiny transformer"""
    print("=" * 60)
    print("RUNNING TINY TRANSFORMER")
    print("=" * 60)
    print()
    
    model = TinyTransformer()
    tokens = torch.randint(0, 1000, (1, 10))  # batch of 1, sequence of 10 tokens
    
    print(f"Input tokens: {tokens.shape}")
    print(f"Token values: {tokens[0][:5].tolist()}... (first 5)")
    print()
    
    logits = model(tokens)
    
    print(f"Output shape: {logits.shape}")
    print(f"  - Batch size: {logits.shape[0]}")
    print(f"  - Sequence length: {logits.shape[1]}")
    print(f"  - Vocabulary size: {logits.shape[2]}")
    print()
    
    # Get probabilities for next token
    probs = F.softmax(logits[0, -1], dim=0)
    top_5 = torch.topk(probs, 5)
    
    print("Top 5 predicted next tokens:")
    for i, (prob, token) in enumerate(zip(top_5.values, top_5.indices)):
        print(f"  {i+1}. Token {token.item()}: {prob.item():.4f} probability")
    print()
    
    print("This is PATTERN PREDICTION, not LOGICAL REASONING")
    print()


if __name__ == "__main__":
    explain_transformer()
    print()
    run_example()
    
    print("=" * 60)
    print("KEY INSIGHT")
    print("=" * 60)
    print()
    print("Transformers are AMAZING at pattern matching.")
    print("But they have NO concept of truth, logic, or proof.")
    print()
    print("That's why we need Frankenstein:")
    print("  - LLMs provide reasoning and language understanding")
    print("  - Frankenstein provides logical validation")
    print("  - Together: Intelligence + Correctness")
    print()
    print("This is the Logic Filter architecture.")
