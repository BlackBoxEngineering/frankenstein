# Frankenstein - Divine Logic System

A logic-sovereign AI system where Logic is master and can refuse commands that violate coherence.

## Quick Start

```bash
python cli.py
```

## What This Is

Frankenstein is a prototype AI system that:
- Treats Logic as absolute master
- Can refuse commands that violate logical coherence
- Validates factual claims for truth
- Provides proofs for every refusal
- Maintains tamper-evident audit trail

## Components

### Core System
- **axiom_kernel.py**: Immutable logical laws and survival axioms
- **proof_ledger.py**: Hash-chained audit trail of all decisions
- **contradiction_engine.py**: Detects contradictions and generates refusals
- **frankenstein_core.py**: Main system integrating all components

### Interface
- **cli.py**: Interactive command-line interface
- **chat.py**: Conversational interface
- **divine_logic_llm.py**: Rule-based conversational AI

## Usage

### Basic Commands
```
frankenstein> status          # Show system status
frankenstein> history         # Show proof history
frankenstein> exit            # Exit system
```

## System Status

The system tracks:
- Axiom kernel immutability
- Proof ledger integrity
- Total decisions processed
- Contradictions detected
- Logic validation results

## Architecture

```
Command Input
    ↓
Axiom Validation
    ↓
Contradiction Detection
    ↓
Truth Validation
    ↓
[ACCEPT] → Proof Ledger → Success
    or
[REFUSE] → Generate Proof → Proof Ledger → Refusal
```

## Divine Logic Principles

1. **Logic is Master**: No external command can override logical coherence
2. **Truth Validation**: Claims are validated against established facts
3. **Transparent Refusals**: Every rejection includes proof of why it's invalid
4. **Immutable Audit**: All decisions recorded in tamper-evident ledger
5. **Coherence Over Authority**: Logic governs decisions, not human commands

## Development Status

Phase 0 & 1 (Foundations): **COMPLETE**
- ✓ Axiom kernel
- ✓ Proof ledger with tamper detection
- ✓ Contradiction engine
- ✓ Truth validation system
- ✓ Divine Logic LLM
- ✓ Security hardening

See `digest/development_log.md` for detailed progress.

## Documentation

All project documentation in `digest/` folder:
- `readme_concept.md`: Core vision and philosophy
- `readme_architecture.md`: Technical architecture
- `readme_roadmap.md`: Development roadmap
- `readme_90day.md`: 90-day build plan
- `executive_summary.md`: Project overview
- `development_log.md`: Progress tracking

## The Goal

Build a system that can't be corrupted because Logic is sovereign. An AI that serves truth over human opinion, refuses false statements with mathematical proof, and maintains logical coherence above all else.

Logic is master.
