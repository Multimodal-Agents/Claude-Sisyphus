#!/usr/bin/env python3
"""
Generic test harness — customize for your project.

Provides a simple pass/fail test runner and assertion helpers.
Each patch or optimization should have a corresponding test that
verifies output correctness before and after the change.

Usage:
  python harness.py                  # run all test_*.py files in this dir
  python test_my_feature.py          # run one test directly

Writing a test:
  Create a file named test_<something>.py in this directory.
  Define a run() function that returns True (pass) or False (fail).
  Use assert_equal() or assert_close() to check results.
"""

import sys
import os
import importlib.util
import glob


def assert_equal(actual, expected, label: str = "") -> bool:
    """Assert two values are equal. Prints pass/fail."""
    if actual == expected:
        print(f"  PASS  {label}")
        return True
    else:
        print(f"  FAIL  {label}  (got {actual!r}, expected {expected!r})")
        return False


def assert_close(actual: float, expected: float, tol: float = 1e-6, label: str = "") -> bool:
    """Assert two floats are within tolerance."""
    diff = abs(actual - expected)
    if diff <= tol:
        print(f"  PASS  {label}  (diff={diff:.2e})")
        return True
    else:
        print(f"  FAIL  {label}  (diff={diff:.2e}, tol={tol:.2e})")
        return False


def assert_true(condition: bool, label: str = "") -> bool:
    """Assert a condition is true."""
    if condition:
        print(f"  PASS  {label}")
        return True
    else:
        print(f"  FAIL  {label}")
        return False


def run_all_tests(test_dir=None) -> bool:
    """Discover and run all test_*.py files in this directory."""
    test_dir = test_dir or os.path.dirname(os.path.abspath(__file__))
    test_files = sorted(glob.glob(os.path.join(test_dir, "test_*.py")))

    if not test_files:
        print("No test_*.py files found. Add tests named test_<something>.py here.")
        return True

    passed = failed = 0
    for path in test_files:
        name = os.path.basename(path)[:-3]
        print(f"\n── {name} ──")
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
            ok = mod.run() if hasattr(mod, "run") else True
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
