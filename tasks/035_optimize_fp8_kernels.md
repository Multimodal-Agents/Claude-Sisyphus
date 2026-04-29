# Task: Analyze and Improve FP8 Training Support

## Goal
FP8 training can give 2x+ throughput on H100s with no quality loss when done correctly. Assess and improve unsloth's FP8 implementation.

## What to analyze
1. Read `C:/Users/Blue/git_work/unsloth/unsloth/kernels/fp8.py` thoroughly
2. Read `C:/Users/Blue/git_work/torchao/` — how does TorchAO handle FP8?
3. Check Transformer Engine (NVIDIA's FP8 library) approach — what does unsloth not implement from TE?
4. Check `C:/Users/Blue/git_work/unsloth_zoo/` for additional FP8 utilities

## Key questions
- Does the current FP8 implementation support both E4M3 and E5M2 formats where appropriate?
- Is scaling factor management (per-tensor, per-channel, delayed scaling) implemented correctly?
- Does FP8 work correctly with LoRA (the A and B matrices need careful handling)?
- Is the FP8 → FP32 accumulation done at the right precision boundary?
- What's the actual measured speedup of FP8 vs BF16 in unsloth vs theoretical maximum?
- Are there any correctness bugs in the current FP8 implementation?

## Output
- `workspace/035_fp8_analysis.md` — current state, gaps, improvement proposals
- `workspace/kernels/fp8_v2.py` — improved implementation if gaps found
- Benchmark showing FP8 vs BF16 training throughput and loss curves
