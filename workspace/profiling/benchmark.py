#!/usr/bin/env python3
"""
Generic benchmark harness — customize for your project.

This template measures execution time and optionally a project-specific metric
(e.g. tokens/sec, requests/sec, score, file size) for a baseline and any
number of variants, then saves results to JSON.

Usage:
  python benchmark.py                        # run all variants
  python benchmark.py --variant baseline     # run one variant
  python benchmark.py --output results.json  # custom output path

Customization:
  1. Edit run_once() to call whatever your project actually does
  2. Edit VARIANTS to list the things you want to compare
  3. Edit METRICS to name your measurements
"""

import argparse
import json
import time
import statistics
import os
import sys
from dataclasses import dataclass, asdict


# ── Configure these for your project ─────────────────────────────────────────

VARIANTS = [
    "baseline",
    # "my_optimization_v1",
    # "my_optimization_v2",
]

WARMUP_RUNS = 2
BENCH_RUNS  = 5


@dataclass
class BenchResult:
    variant: str
    mean_ms: float
    stdev_ms: float
    min_ms: float
    max_ms: float
    extra: dict   # put any project-specific metrics here


def run_once(variant: str) -> tuple[float, dict]:
    """
    Run your project's operation once.
    Returns: (elapsed_ms, extra_metrics_dict)

    Replace the body of this function with whatever you're benchmarking.
    The variant name tells you which version to use.
    """
    t0 = time.perf_counter()

    # ── YOUR CODE HERE ────────────────────────────────────────────────────────
    # Example: time how long it takes to process a file, run a model, etc.
    # For the snake demo this might measure JS execution time via headless browser.
    time.sleep(0.01)  # placeholder — replace this
    # ─────────────────────────────────────────────────────────────────────────

    elapsed_ms = (time.perf_counter() - t0) * 1000
    extra = {}  # e.g. {"score": 42, "memory_mb": 128}
    return elapsed_ms, extra


def bench_variant(variant: str) -> BenchResult:
    times = []
    extras = []

    for i in range(WARMUP_RUNS + BENCH_RUNS):
        ms, extra = run_once(variant)
        if i >= WARMUP_RUNS:
            times.append(ms)
            extras.append(extra)

    merged_extra = {}
    for key in (extras[0] if extras else {}):
        vals = [e[key] for e in extras if key in e]
        merged_extra[key] = round(statistics.mean(vals), 3) if vals else None

    return BenchResult(
        variant=variant,
        mean_ms=round(statistics.mean(times), 2),
        stdev_ms=round(statistics.stdev(times) if len(times) > 1 else 0, 2),
        min_ms=round(min(times), 2),
        max_ms=round(max(times), 2),
        extra=merged_extra,
    )


def compare(results: list[BenchResult]) -> None:
    baseline = next((r for r in results if r.variant == "baseline"), results[0])
    print(f"\n{'Variant':<30} {'Mean ms':>10} {'Stdev':>8} {'vs baseline':>12}")
    print("-" * 65)
    for r in results:
        delta = ((r.mean_ms / baseline.mean_ms) - 1) * 100 if baseline.mean_ms else 0
        sign = "+" if delta >= 0 else ""
        marker = " ← baseline" if r.variant == baseline.variant else f"  {sign}{delta:.1f}%"
        print(f"{r.variant:<30} {r.mean_ms:>10.2f} {r.stdev_ms:>8.2f} {marker}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--variant", help="Run a single variant only")
    parser.add_argument("--output", default="workspace/profiling/results.json")
    args = parser.parse_args()

    variants = [args.variant] if args.variant else VARIANTS
    results = []

    for v in variants:
        print(f"Benchmarking {v} ({WARMUP_RUNS} warmup + {BENCH_RUNS} runs)...", end=" ", flush=True)
        r = bench_variant(v)
        results.append(r)
        print(f"{r.mean_ms:.1f} ms ± {r.stdev_ms:.1f}")

    compare(results)

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w") as f:
        json.dump([asdict(r) for r in results], f, indent=2)
    print(f"\nSaved to {args.output}")


if __name__ == "__main__":
    main()
