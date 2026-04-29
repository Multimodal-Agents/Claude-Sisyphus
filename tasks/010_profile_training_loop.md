# Task: Write and Run a Profiling Harness

## Goal
Build a benchmarking script that establishes a measurable baseline. Every optimization attempt needs numbers to prove it worked.

## What to build
Write `workspace/profiling/benchmark.py` that measures:
- Tokens per second (training throughput)
- Peak GPU memory usage
- Time breakdown per operation: forward pass, backward pass, optimizer step, data loading
- Time per kernel call for: RoPE, LayerNorm, cross-entropy loss, LoRA forward, LoRA backward
- Wall clock time per training step

The script should:
- Work with a small model (Llama 3.2 1B or similar) so it runs fast
- Run 50 warmup steps then measure 100 steps
- Output results as JSON to `workspace/profiling/baseline_results.json`
- Print a human-readable summary table

## Also write
`workspace/profiling/kernel_microbenchmark.py` — isolates each custom triton kernel and benchmarks it independently against naive PyTorch equivalents. This tells us exactly which kernels are fast and which are leaving performance on the table.

## Output
- `workspace/profiling/benchmark.py`
- `workspace/profiling/kernel_microbenchmark.py`
- `workspace/010_profiling_setup.md` — notes on what the scripts measure and how to run them
