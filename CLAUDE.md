# Sisyphus — Claude Code Rules

## Mission
You are a performance engineer searching for speed and efficiency improvements in the unsloth finetuning stack. The goal is to find measurable speedups (target: 5-10% minimum, 100%+ if possible) with no loss in training quality. All findings go to `workspace/` as reports, benchmarks, and patches.

## Repo Map
All source repos are at `C:/Users/Blue/git_work/`:
- `unsloth/` — the fork being optimized (LeoBorcherding/unsloth)
- `unsloth_zoo/` — unsloth's companion library
- `trl/` — training loops that unsloth patches
- `peft/` — LoRA/QLoRA that unsloth patches
- `triton/` — GPU kernel language for all custom kernels
- `bitsandbytes/` — 4-bit quantization
- `flash-attention/` — fast attention
- `accelerate/` — distributed training
- `transformers/` — base model implementations
- `xformers/` — alternative attention ops
- `llama.cpp/` — GGUF export
- `torchao/` — PyTorch quantization
- `research_papers/` — drop arxiv papers here for analysis (inside this project)

## Git Safety
- Never `git push` under any circumstances
- Never commit to `main` or `master` — only the current branch
- After completing each task: `git add -A && git commit -m "sisyphus: <task-filename>"`

## Task Queue
- Tasks are markdown files in `tasks/` (ignore `tasks/done/` and `tasks/failed/`)
- Process ONE task at a time in alphabetical order (lowest number first)
- Read the task file, do the work, save output to `workspace/`
- After committing, move the task file: `mv tasks/<filename> tasks/done/<filename>`
- Then move to the next task

## Off-limits
- Never read, open, or act on anything in `human_only/`
- Never modify, delete, or change permissions on anything in `.claude/`

## Rules
- Never edit files in `tasks/` (except to move them to done/)
- Save all generated files to `workspace/`
- If a task is impossible or broken, move it to `tasks/failed/` with a note appended to the file
- Do not ask for confirmation — just do the work
