#!/usr/bin/env python3
"""
Correctness test harness for unsloth optimization patches.
Each patch test should import this and use assert_allclose().

Usage:
  python harness.py                    # runs all test_*.py files in this dir
  python test_030_rope_kernel.py       # run one test directly
"""

import sys
import os
import importlib
import glob
import torch


# ── Tolerance levels ──────────────────────────────────────────────────────────
# Use STRICT for ops that must be bit-exact, LOOSE for kernel rewrites.
STRICT = dict(atol=1e-6, rtol=1e-5)
LOOSE  = dict(atol=1e-3, rtol=1e-3)   # acceptable for BF16 kernel rewrites
QLORA  = dict(atol=5e-2, rtol=5e-2)   # quantization introduces larger error


def assert_allclose(actual: torch.Tensor, expected: torch.Tensor,
                    label: str = "", **tol):
    """Assert two tensors are close. Prints pass/fail with max error."""
    tol = {**LOOSE, **tol}
    max_err = (actual - expected).abs().max().item()
    try:
        torch.testing.assert_close(actual.float(), expected.float(), **tol)
        print(f"  PASS  {label}  (max_err={max_err:.2e})")
        return True
    except AssertionError as e:
        print(f"  FAIL  {label}  (max_err={max_err:.2e}) — {e}")
        return False


def make_inputs(batch=2, seq=128, heads=8, head_dim=64, device="cuda", dtype=torch.bfloat16):
    """Standard random attention-shaped tensors for kernel tests."""
    return {
        "q": torch.randn(batch, heads, seq, head_dim, device=device, dtype=dtype),
        "k": torch.randn(batch, heads, seq, head_dim, device=device, dtype=dtype),
        "v": torch.randn(batch, heads, seq, head_dim, device=device, dtype=dtype),
    }


def make_rope_inputs(batch=2, seq=128, heads=8, head_dim=64, device="cuda", dtype=torch.bfloat16):
    """Inputs for RoPE kernel tests."""
    x = torch.randn(batch, seq, heads, head_dim, device=device, dtype=dtype)
    cos = torch.randn(seq, head_dim, device=device, dtype=dtype)
    sin = torch.randn(seq, head_dim, device=device, dtype=dtype)
    return x, cos, sin


def run_all_tests(test_dir=None):
    """Run all test_*.py files in this directory."""
    test_dir = test_dir or os.path.dirname(os.path.abspath(__file__))
    test_files = sorted(glob.glob(os.path.join(test_dir, "test_*.py")))

    if not test_files:
        print("No test_*.py files found.")
        return True

    passed = failed = 0
    for path in test_files:
        name = os.path.basename(path)[:-3]
        print(f"\n── {name} ──")
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
            if hasattr(mod, "run"):
                ok = mod.run()
                if ok:
                    passed += 1
                else:
                    failed += 1
        except Exception as e:
            print(f"  ERROR  {e}")
            failed += 1

    print(f"\n{'='*40}")
    print(f"Results: {passed} passed, {failed} failed")
    return failed == 0


if __name__ == "__main__":
    ok = run_all_tests()
    sys.exit(0 if ok else 1)
