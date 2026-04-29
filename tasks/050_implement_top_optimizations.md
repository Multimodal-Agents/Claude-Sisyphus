# Task: Implement the Top-Priority Optimizations

## Goal
Based on `workspace/021_priority_list.md`, implement all Tier 1 (quick wins) optimizations and the highest-confidence Tier 2 optimizations.

## What to do
1. Read `workspace/021_priority_list.md`
2. For each Tier 1 item:
   a. Implement the change in the appropriate file under `workspace/patches/`
   b. Write a correctness test — output must match the original within float tolerance
   c. Benchmark before and after
   d. Document the change
3. For Tier 2 items with confidence >= "medium":
   a. Same process as Tier 1
   b. Also note any risks and edge cases

## Implementation rules
- All changes go in `workspace/patches/` — never modify the source repos directly
- Every patch file should be a clean diff that could be applied with `git apply`
- Every patch must have a corresponding correctness test
- If a benchmark shows < 0.5% improvement, document it as "not worth the complexity" and move on

## Output
- `workspace/patches/` — one patch file per optimization
- `workspace/patches/tests/` — one test per patch
- `workspace/050_implementation_log.md` — what was implemented, what was skipped and why
