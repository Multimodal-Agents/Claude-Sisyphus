# Task: Optimize the Cross-Entropy Loss Kernel

## Goal
Improve `C:/Users/Blue/git_work/sisyphus_main/Claude-Sisyphus/workspace/unsloth/unsloth/kernels/cross_entropy_loss.py`.

## Background
Cross-entropy loss is computed over the entire vocabulary (often 128K+ tokens for modern models) at every training step. The current fused implementation is good but there may be room to improve further, especially for large vocabularies.

## What to do
1. Read the current implementation — understand the chunking strategy
2. Research "chunked cross entropy" and "liger kernel" cross entropy approaches
3. Check `C:/Users/Blue/git_work/sisyphus_main/Claude-Sisyphus/workspace/trl/` for how it computes loss — is there overlap?
4. Check if there's an opportunity to overlap the loss computation with the backward pass
5. Investigate whether the vocabulary parallel approach from Megatron-LM is applicable
6. Implement improvements in `workspace/kernels/cross_entropy_v2.py`
7. Test on vocab sizes: 32K, 64K, 128K, 256K — does performance scale?

## Specific questions
- What is the current memory usage for a 128K vocab size at batch=8, seq=4096?
- Can the softmax and log be fused more aggressively?
- Is there wasted computation for masked/padding tokens?
- Can we avoid the full softmax for chunked CE?

## Output
- `workspace/kernels/cross_entropy_v2.py`
- `workspace/profiling/benchmark_cross_entropy.py`
- `workspace/032_cross_entropy_optimization.md`
