# Task: Full Benchmark — Baseline vs Optimized Stack

## Goal
Produce definitive numbers comparing the original unsloth against all applied optimizations. These numbers go to the boss.

## What to benchmark
Run `workspace/profiling/benchmark.py` with:
1. Baseline (no patches applied)
2. Each patch applied individually (to measure isolated contribution)
3. All Tier 1 patches applied together
4. All patches applied together

## Benchmark configurations
- Model: Llama 3.2 1B (fast to run)
- Model: Llama 3.1 8B (realistic size)
- Batch sizes: 1, 4, 8
- Sequence lengths: 512, 2048, 4096
- Precision: BF16, QLoRA 4-bit
- LoRA rank: 16, 64

## Metrics to report
- Tokens per second (primary metric)
- Peak GPU memory (MB)
- Time per training step (ms)
- Time breakdown: forward / backward / optimizer / data loading
- Improvement % vs baseline for each config

## Output
- `workspace/060_benchmark_results.json` — raw numbers
- `workspace/060_benchmark_results.md` — human-readable tables
- `workspace/060_benchmark_charts.py` — script to generate charts from the JSON
