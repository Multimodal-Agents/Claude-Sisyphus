# Task: Build the Master Optimization Priority List

## Goal
Synthesize everything from the survey (001), kernel analysis (011), memory analysis (012), and paper analysis (020) into a single ranked priority list that Sisyphus will execute in subsequent tasks.

## Inputs
Read:
- `workspace/001_survey.md`
- `workspace/011_kernel_analysis.md`
- `workspace/012_memory_analysis.md`
- `workspace/020_paper_analysis.md`

## What to produce
A ranked master list of every optimization opportunity, scored by:
- **Impact**: estimated % speedup or memory reduction (be conservative — divide your first estimate by 2)
- **Confidence**: how certain are we this will work (high/medium/low)
- **Effort**: hours to implement and test
- **Risk**: could this break correctness? (none/low/medium/high)
- **Score**: Impact × Confidence / Effort (higher = do first)

Categorize as:
- **Tier 1 — Quick wins**: < 4 hours, >1% gain, low risk. Do these first.
- **Tier 2 — High value**: < 2 days, >5% gain, medium risk. Core optimization work.
- **Tier 3 — Big bets**: 1+ week, potential >20% gain, higher risk. Worth attempting but validate carefully.

## Output
Save to `workspace/021_priority_list.md` — this is the roadmap for all subsequent tasks.
Also save `workspace/021_priority_list.json` with the same data in structured format.
