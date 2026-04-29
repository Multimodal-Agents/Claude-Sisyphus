# Task: Optimize Sample Packing and Data Pipeline

## Goal
Data pipeline inefficiencies can starve the GPU. Sample packing quality directly affects how many real tokens vs padding tokens the GPU processes.

## What to analyze

### Sample packing
1. Find sample packing implementation in `C:/Users/Blue/git_work/sisyphus_main/Claude-Sisyphus/workspace/unsloth/` — search for "packing", "sample_packing"
2. Read `C:/Users/Blue/git_work/sisyphus_main/Claude-Sisyphus/workspace/trl/trl/trainer/` — how does TRL handle data collation?
3. Research "bin packing algorithms" — is unsloth using an optimal algorithm for fitting sequences into batches?
4. What is the typical padding waste % in current implementation? (Estimate with a sample dataset)

### Data loading
1. Find data loading code in unsloth and TRL
2. Is data preprocessing happening on the critical path or pre-cached?
3. Is there a prefetch buffer? Is it large enough?
4. Are tokenization and tensor creation vectorized?

### Padding-free training
1. Does unsloth support padding-free training (packing multiple samples into one sequence)?
2. If yes, is the attention mask (block-diagonal) computed efficiently?
3. If no, could it be added and what would the speedup be?

## Output
- `workspace/038_data_pipeline_analysis.md`
- Estimated GPU utilization improvement from better packing
- Any implementation improvements
