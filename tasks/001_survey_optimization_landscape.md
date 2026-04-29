# Task: Survey the Optimization Landscape

## Mission
You are a performance engineer tasked with finding speed and efficiency improvements in the unsloth finetuning stack. Your boss wants at minimum a 5-10% training speed improvement with no quality loss, and ideally 100%+ gains.

## Repo locations
All repos are at `C:/Users/Blue/git_work/`:
- `unsloth/` — the fork we are optimizing
- `unsloth_zoo/` — unsloth's companion library
- `trl/` — training loops that unsloth patches
- `peft/` — LoRA/QLoRA implementation that unsloth patches
- `triton/` — GPU kernel language used for all custom kernels
- `bitsandbytes/` — quantization library
- `flash-attention/` — fast attention implementation
- `accelerate/` — distributed training
- `transformers/` — base model implementations that unsloth patches
- `xformers/` — alternative attention/ops library
- `llama.cpp/` — GGUF export and inference
- `torchao/` — PyTorch quantization library

## What to do
1. Read `C:/Users/Blue/git_work/sisyphus_main/Claude-Sisyphus/workspace/unsloth/unsloth/kernels/` — every file, understand what each kernel does
2. Read `C:/Users/Blue/git_work/sisyphus_main/Claude-Sisyphus/workspace/unsloth/unsloth/models/llama.py` — understand how unsloth patches transformers
3. Read `C:/Users/Blue/git_work/sisyphus_main/Claude-Sisyphus/workspace/unsloth/unsloth/trainer.py` — understand the training loop modifications
4. Read `C:/Users/Blue/git_work/sisyphus_main/Claude-Sisyphus/workspace/unsloth/unsloth/import_fixes.py` — understand what bugs unsloth is working around
5. For each of the 12 dependency repos, read the README and key source files
6. Map every point where unsloth touches an external library
7. Identify the top 25 specific code locations with the highest optimization potential, ranked by estimated impact

## Output
Save a comprehensive survey to `workspace/001_survey.md` covering:
- Architecture map: how unsloth interacts with each dependency
- Top 25 optimization opportunities ranked by estimated impact (% gain)
- Quick wins (< 1 day to implement, likely 1-5% gain each)
- Big bets (1+ week, potential 20-100%+ gain)
- What the competition (vLLM, DeepSpeed, Megatron) does differently that unsloth could adopt
