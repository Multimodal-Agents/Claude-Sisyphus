# Task: Extract Optimization Techniques from Research Papers

## Goal
Read every paper in `C:/Users/Blue/git_work/sisyphus_main/Claude-Sisyphus/research_papers/` and extract techniques directly applicable to improving unsloth's speed, memory efficiency, or output quality.

## How to process each paper
For each file in research_papers/ (skip README.md):
1. Read the full paper
2. Extract the core technical contribution
3. Assess applicability to unsloth's stack (1-10 scale)
4. Estimate implementation effort (hours/days/weeks)
5. Estimate potential speedup or efficiency gain
6. Identify the exact unsloth files that would need to change
7. Note any prerequisites (e.g., "requires CUDA 12.x", "requires H100")

## Categories to look for
- New attention mechanisms or memory-efficient attention variants
- Quantization schemes (FP8, INT4, mixed precision innovations)
- Triton/CUDA kernel optimization techniques
- LoRA variants with better efficiency/quality tradeoffs
- Gradient compression or approximation methods
- Training stability improvements that allow larger learning rates
- Data efficiency techniques (fewer tokens needed for same quality)

## If research_papers/ is empty
Note this in the output and proceed. New papers can be added later and this task re-run.

## Output
Save to `workspace/020_paper_analysis.md`:
- One section per paper with: title, core technique, applicability score, effort estimate, impact estimate, specific files to change
- Summary table ranked by (applicability × impact) / effort
