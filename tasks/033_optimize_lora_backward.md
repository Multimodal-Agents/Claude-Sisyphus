# Task: Optimize the LoRA Backward Pass

## Goal
Improve the LoRA backward pass in `C:/Users/Blue/git_work/sisyphus_main/Claude-Sisyphus/workspace/unsloth/unsloth/kernels/fast_lora.py`.

## Background
The LoRA backward pass is the single most-executed piece of code during finetuning. It runs for every LoRA layer on every backward pass. Unsloth already has a custom implementation — this task finds what it's still leaving on the table.

## What to do
1. Read `fast_lora.py` exhaustively — map every tensor operation
2. Draw the computation graph for the LoRA backward pass on paper (save as ASCII art in the output)
3. Identify every intermediate tensor that gets materialized — do any of them not need to exist?
4. Compare against the naive PEFT implementation in `C:/Users/Blue/git_work/sisyphus_main/Claude-Sisyphus/workspace/peft/src/peft/tuners/lora/`
5. Check literature for "gradient checkpointing for LoRA" — can we save memory by recomputing instead of storing?
6. Investigate whether the A and B matrix gradient computations can be better parallelized
7. Check if the current implementation handles gradient accumulation optimally
8. Implement improvements in `workspace/kernels/fast_lora_v2.py`
9. Validate: the output of v2 must be numerically identical to v1 (write a correctness test)

## Output
- `workspace/kernels/fast_lora_v2.py`
- `workspace/profiling/benchmark_lora_backward.py`
- `workspace/kernels/test_lora_correctness.py` — must pass before claiming improvement
- `workspace/033_lora_backward_optimization.md`
