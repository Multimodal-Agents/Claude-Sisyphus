# Task: Optimize the LayerNorm and RMSNorm Triton Kernels

## Goal
Improve `C:/Users/Blue/git_work/unsloth/unsloth/kernels/layernorm.py` and `rms_layernorm.py`.

## Background
RMSNorm is called at every transformer layer. Llama-family models use it exclusively. Faster RMSNorm = faster everything.

## What to do
1. Read both kernel files carefully
2. Compare against Apex's fused LayerNorm and triton's own LayerNorm tutorial
3. Check the `C:/Users/Blue/git_work/xformers/` LayerNorm implementation for ideas
4. Implement improvements in `workspace/kernels/rms_layernorm_v2.py`
5. Pay special attention to:
   - The backward pass — is it computing more than necessary?
   - Weight gradient accumulation — any redundancy?
   - Can it be fused with the adjacent linear layer (pre-norm fusion)?
   - FP8 support — does the current kernel handle FP8 inputs correctly?
6. Benchmark both versions

## Output
- `workspace/kernels/rms_layernorm_v2.py`
- `workspace/profiling/benchmark_layernorm.py`
- `workspace/031_layernorm_optimization.md`
