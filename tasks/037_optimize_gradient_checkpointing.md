# Task: Optimize Gradient Checkpointing

## Goal
Gradient checkpointing trades compute for memory. Smarter checkpoint placement can reduce memory with less compute overhead.

## What to analyze
1. Read `C:/Users/Blue/git_work/unsloth_zoo/` — find the gradient checkpointing implementation
2. Read `C:/Users/Blue/git_work/unsloth/unsloth/models/llama.py` — find where checkpointing is applied
3. Research "selective activation recomputation" — the technique of only checkpointing the expensive parts
4. Research "activation offloading" — can activations be moved to CPU during forward pass?

## Key questions
- Does unsloth checkpoint at the right granularity (per-layer vs per-attention-block vs per-MLP)?
- Is there a smarter checkpoint schedule that reduces recomputation more?
- Can we use `torch.utils.checkpoint` with `use_reentrant=False` for better performance?
- Is there any wasted recomputation — things being computed twice that don't need to be?
- How does unsloth's gradient checkpointing interact with LoRA — are we recomputing LoRA operations unnecessarily?

## Output
- `workspace/037_gradient_checkpointing_analysis.md`
- Improved implementation if opportunities found in `workspace/`
- Memory/speed tradeoff curves for different checkpointing strategies
