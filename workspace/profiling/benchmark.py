#!/usr/bin/env python3
"""
Unsloth optimization benchmark harness.
Usage:
  python benchmark.py --mode baseline
  python benchmark.py --mode patch --patch ../patches/030_rope_kernel.patch
  python benchmark.py --mode all
  python benchmark.py --output ../060_benchmark_results.json
"""

import argparse
import json
import time
import os
import sys
from dataclasses import dataclass, asdict
from typing import Optional

# ── GPU check ────────────────────────────────────────────────────────────────
try:
    import torch
    HAS_GPU = torch.cuda.is_available()
    GPU_NAME = torch.cuda.get_device_name(0) if HAS_GPU else "CPU"
except ImportError:
    print("ERROR: torch not installed. Run: pip install torch")
    sys.exit(1)

# ── Config ────────────────────────────────────────────────────────────────────
MODELS = [
    "unsloth/Llama-3.2-1B",
    # "unsloth/Meta-Llama-3.1-8B",  # uncomment for 8B runs
]

BATCH_SIZES   = [1, 4, 8]
SEQ_LENGTHS   = [512, 2048, 4096]
PRECISIONS    = ["bf16", "qlora_4bit"]
LORA_RANKS    = [16, 64]
WARMUP_STEPS  = 3
BENCH_STEPS   = 10


@dataclass
class BenchResult:
    model: str
    batch_size: int
    seq_len: int
    precision: str
    lora_rank: int
    tokens_per_sec: float
    peak_memory_mb: float
    ms_per_step: float
    ms_forward: float
    ms_backward: float
    ms_optimizer: float
    ms_data: float
    gpu: str
    patch_label: str = "baseline"


def bench_one(model_name, batch_size, seq_len, precision, lora_rank, patch_label="baseline") -> BenchResult:
    """Run a single benchmark configuration. Returns a BenchResult."""
    try:
        from unsloth import FastLanguageModel
        import torch
    except ImportError:
        raise RuntimeError("unsloth not installed. Run: pip install unsloth")

    load_in_4bit = (precision == "qlora_4bit")
    dtype = torch.bfloat16

    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=model_name,
        max_seq_length=seq_len,
        load_in_4bit=load_in_4bit,
        dtype=dtype,
    )
    model = FastLanguageModel.get_peft_model(
        model,
        r=lora_rank,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                        "gate_proj", "up_proj", "down_proj"],
        lora_alpha=lora_rank,
        lora_dropout=0,
        bias="none",
        use_gradient_checkpointing="unsloth",
    )

    # Synthetic batch
    input_ids = torch.randint(100, 32000, (batch_size, seq_len), device="cuda")
    labels = input_ids.clone()
    attention_mask = torch.ones_like(input_ids)

    optimizer = torch.optim.AdamW(model.parameters(), lr=2e-4)

    t_forward = t_backward = t_optimizer = 0.0
    peak_mem = 0.0

    torch.cuda.reset_peak_memory_stats()

    for step in range(WARMUP_STEPS + BENCH_STEPS):
        t0 = time.perf_counter()
        outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss
        torch.cuda.synchronize()
        t1 = time.perf_counter()

        loss.backward()
        torch.cuda.synchronize()
        t2 = time.perf_counter()

        optimizer.step()
        optimizer.zero_grad()
        torch.cuda.synchronize()
        t3 = time.perf_counter()

        if step >= WARMUP_STEPS:
            t_forward   += (t1 - t0) * 1000
            t_backward  += (t2 - t1) * 1000
            t_optimizer += (t3 - t2) * 1000
            peak_mem = max(peak_mem, torch.cuda.max_memory_allocated() / 1e6)

    ms_step = (t_forward + t_backward + t_optimizer) / BENCH_STEPS
    tokens_per_sec = (batch_size * seq_len) / (ms_step / 1000)

    del model, tokenizer
    torch.cuda.empty_cache()

    return BenchResult(
        model=model_name,
        batch_size=batch_size,
        seq_len=seq_len,
        precision=precision,
        lora_rank=lora_rank,
        tokens_per_sec=round(tokens_per_sec, 1),
        peak_memory_mb=round(peak_mem, 1),
        ms_per_step=round(ms_step, 2),
        ms_forward=round(t_forward / BENCH_STEPS, 2),
        ms_backward=round(t_backward / BENCH_STEPS, 2),
        ms_optimizer=round(t_optimizer / BENCH_STEPS, 2),
        ms_data=0.0,
        gpu=GPU_NAME,
        patch_label=patch_label,
    )


def run_all(patch_label="baseline") -> list[BenchResult]:
    results = []
    configs = [
        (m, b, s, p, r)
        for m in MODELS
        for b in BATCH_SIZES
        for s in SEQ_LENGTHS
        for p in PRECISIONS
        for r in LORA_RANKS
    ]
    total = len(configs)
    for i, (m, b, s, p, r) in enumerate(configs, 1):
        print(f"[{i}/{total}] {m} bs={b} seq={s} {p} r={r} ...", end=" ", flush=True)
        try:
            result = bench_one(m, b, s, p, r, patch_label)
            results.append(result)
            print(f"{result.tokens_per_sec:.0f} tok/s  {result.peak_memory_mb:.0f} MB")
        except Exception as e:
            print(f"SKIP ({e})")
    return results


def compare_to_baseline(results: list[BenchResult], baseline_path: str) -> list[dict]:
    with open(baseline_path) as f:
        baseline = {
            (r["model"], r["batch_size"], r["seq_len"], r["precision"], r["lora_rank"]): r
            for r in json.load(f)
        }
    comparisons = []
    for r in results:
        key = (r.model, r.batch_size, r.seq_len, r.precision, r.lora_rank)
        if key in baseline:
            b = baseline[key]
            speedup = (r.tokens_per_sec / b["tokens_per_sec"] - 1) * 100
            mem_delta = r.peak_memory_mb - b["peak_memory_mb"]
            comparisons.append({**asdict(r), "speedup_pct": round(speedup, 2), "mem_delta_mb": round(mem_delta, 1)})
    return comparisons


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["baseline", "patch", "all"], default="baseline")
    parser.add_argument("--patch", help="Path to patch file (for --mode patch)")
    parser.add_argument("--label", default="baseline", help="Label for this run in results")
    parser.add_argument("--baseline-json", help="Path to baseline JSON for comparison")
    parser.add_argument("--output", default="../060_benchmark_results.json")
    args = parser.parse_args()

    if not HAS_GPU:
        print("WARNING: No CUDA GPU detected. Benchmarks require a GPU.")
        sys.exit(1)

    print(f"GPU: {GPU_NAME}")
    print(f"Mode: {args.mode}  Label: {args.label}")
    print(f"Warmup: {WARMUP_STEPS} steps  Bench: {BENCH_STEPS} steps\n")

    results = run_all(args.label)

    out = [asdict(r) for r in results]
    with open(args.output, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nSaved {len(out)} results to {args.output}")

    if args.baseline_json and os.path.exists(args.baseline_json):
        comp = compare_to_baseline(results, args.baseline_json)
        comp_path = args.output.replace(".json", "_comparison.json")
        with open(comp_path, "w") as f:
            json.dump(comp, f, indent=2)
        avg_speedup = sum(c["speedup_pct"] for c in comp) / len(comp) if comp else 0
        print(f"Average speedup vs baseline: {avg_speedup:+.1f}%")
        print(f"Saved comparison to {comp_path}")


if __name__ == "__main__":
    main()
