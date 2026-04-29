# Task: Optimize the Quantization Pipeline

## Goal
Improve how unsloth integrates with bitsandbytes and other quantization libraries.

## What to analyze
1. Read `C:/Users/Blue/git_work/sisyphus_main/Claude-Sisyphus/workspace/unsloth/unsloth/import_fixes.py` — find all quantization-related patches
2. Read `C:/Users/Blue/git_work/sisyphus_main/Claude-Sisyphus/workspace/bitsandbytes/bitsandbytes/` — understand the 4-bit quantization implementation
3. Read `C:/Users/Blue/git_work/sisyphus_main/Claude-Sisyphus/workspace/unsloth/unsloth/models/llama.py` — find all `bnb.nn.Linear4bit` usage
4. Read `C:/Users/Blue/git_work/sisyphus_main/Claude-Sisyphus/workspace/torchao/` — is there a faster path for 4-bit that bypasses bitsandbytes?

## Specific opportunities
- **Dequantization overhead**: How much time is spent dequantizing weights during forward pass? Can this be fused with the matmul?
- **NF4 vs other formats**: Is NF4 the best quantization format for finetuning, or are newer formats better?
- **Double quantization**: When is double quantization worth the overhead?
- **Quantization-aware LoRA backward**: Can the quantized weights affect the gradient computation negatively?
- **TorchAO integration**: Could `C:/Users/Blue/git_work/sisyphus_main/Claude-Sisyphus/workspace/torchao/` replace bitsandbytes for better speed?

## Output
- `workspace/036_quantization_analysis.md`
- Any prototype implementations in `workspace/kernels/`
- Benchmarks comparing current quantization vs proposed improvements
