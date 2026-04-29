# Task: Deep Analysis of Unsloth's Triton Kernels

## Goal
Find every optimization opportunity in unsloth's custom triton kernels. These are the core of unsloth's speed advantage — improving them is the highest-leverage work.

## Kernels to analyze (in `C:/Users/Blue/git_work/sisyphus_main/Claude-Sisyphus/workspace/unsloth/unsloth/kernels/`)
For each kernel file, analyze:
1. `fast_lora.py` — LoRA forward and backward passes
2. `layernorm.py` — LayerNorm forward/backward
3. `rms_layernorm.py` — RMSNorm (used by Llama, Qwen, etc.)
4. `rope_embedding.py` — Rotary positional embeddings
5. `cross_entropy_loss.py` — Fused cross-entropy
6. `fp8.py` — FP8 quantization kernels
7. `geglu.py` / `swiglu.py` — Activation function kernels
8. `moe/` directory — Mixture-of-Experts kernels

## For each kernel, check
- Block size and warp configuration — are these autotuned or hardcoded? If hardcoded, are they optimal?
- Memory access patterns — coalesced reads/writes? Shared memory usage?
- Arithmetic intensity — is it compute-bound or memory-bound?
- Fusion opportunities — what adjacent operations could be merged into this kernel?
- Comparison to state-of-the-art: what does flash-attention, xformers, or triton's own examples do differently?
- Missing features: does the kernel support all precisions (bf16, fp16, fp8)?

## Also check
- Compare unsloth's RoPE kernel against `C:/Users/Blue/git_work/sisyphus_main/Claude-Sisyphus/workspace/flash-attention/` implementation
- Compare unsloth's LayerNorm against `C:/Users/Blue/git_work/sisyphus_main/Claude-Sisyphus/workspace/xformers/` implementation
- Look at `C:/Users/Blue/git_work/sisyphus_main/Claude-Sisyphus/workspace/triton/python/tutorials/` for techniques unsloth isn't using

## Output
Save to `workspace/011_kernel_analysis.md`:
- Per-kernel analysis with specific line numbers for issues found
- Ranked list of kernel improvements by estimated speedup
- Concrete implementation suggestions for each improvement
