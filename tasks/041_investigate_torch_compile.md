# Task: Investigate torch.compile Integration Opportunities

## Goal
`torch.compile` with `mode='max-autotune'` can sometimes outperform hand-written triton kernels by finding fusions and scheduling that manual implementations miss. Find where unsloth should and should not use it.

## What to do
1. Find every place unsloth explicitly disables or avoids `torch.compile`
2. Find every place it's enabled — with what settings?
3. Write a test script that runs unsloth's forward pass with and without `torch.compile`
4. Compare: compiled vs uncompiled vs manual triton kernels for each major operation
5. Check if `torch.compile` is compatible with unsloth's custom autograd functions
6. Investigate `torch.compile` with `fullgraph=True` — does unsloth's code graph-break anywhere?

## Specific things to test
- Does `torch.compile` on the full model + LoRA forward pass outperform unsloth's manual kernels?
- Can `torch.compile` be applied selectively to just the MLP or just the attention?
- Does compilation work correctly with QLoRA (4-bit weights)?
- What is the compilation time overhead and warmup cost?

## Also check
- `C:/Users/Blue/git_work/sisyphus_main/Claude-Sisyphus/workspace/torchao/` — does TorchAO's `quantize_` + `torch.compile` path beat current approach?

## Output
- `workspace/041_torch_compile_analysis.md` — benchmark results and recommendations
- `workspace/profiling/benchmark_compile.py` — the test script
