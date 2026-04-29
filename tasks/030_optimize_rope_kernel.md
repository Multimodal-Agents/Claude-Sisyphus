# Task: Optimize the RoPE Embedding Triton Kernel

## Goal
Improve `C:/Users/Blue/git_work/unsloth/unsloth/kernels/rope_embedding.py` for speed and memory efficiency.

## Background
RoPE (Rotary Position Embedding) is applied at every attention layer on every forward and backward pass. Even a 5% improvement here compounds across all layers and all steps.

## What to do
1. Read the current implementation thoroughly — understand every line
2. Read `C:/Users/Blue/git_work/triton/python/tutorials/` for optimization patterns
3. Check if any flash-attention or xformers implementations do RoPE differently
4. Identify: block size tuning, shared memory usage, memory access coalescing, fusion opportunities
5. Implement improvements in a copy of the file: `workspace/kernels/rope_embedding_v2.py`
6. Write a microbenchmark in `workspace/profiling/benchmark_rope.py` that tests both versions
7. Run the benchmark and record results

## Specific things to check
- Can the forward and backward be fused into one kernel pass?
- Is the current block size (BLOCK_SIZE) optimal for modern GPUs (A100/H100)?
- Can the cos/sin tables be cached more efficiently?
- Is there an opportunity for FP8 RoPE?
- Does the kernel handle non-contiguous tensors efficiently?

## Output
- `workspace/kernels/rope_embedding_v2.py` — improved implementation
- `workspace/profiling/benchmark_rope.py` — benchmark comparing v1 vs v2
- `workspace/030_rope_optimization.md` — what changed, why, and measured results
