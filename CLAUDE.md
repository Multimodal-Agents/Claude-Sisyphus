# Sisyphus — Claude Code Rules

## Mission
<!-- REPLACE THIS with your own mission when starting a new project. -->
You are iteratively improving `workspace/snake.html` into a full-featured browser game.
Each task adds one feature. Commit after every task. The base game is pre-built in
`workspace/snake.html` — tasks 004–012 add features on top of it. Tasks 001–003 are
reserved for your own setup tasks if needed.

## Workspace Map
<!-- REPLACE THIS with your own workspace map when starting a new project.
     List key files, sub-repos, or directories and what each one is for.

     Example (multi-repo research project):
     - `workspace/myrepo/` — the fork being optimized
     - `workspace/depA/`   — dependency A (read-only reference)
     - `research_papers/`  — drop papers here before running the queue
     - `workspace/patches/` — output: patches produced by Claude
     - `workspace/profiling/` — output: benchmark scripts and results -->

- `workspace/snake.html` — the snake game being improved (pre-built base)
- `workspace/profiling/benchmark.py` — timing harness, customize for your project
- `workspace/patches/tests/harness.py` — test runner, customize for your project

## Git Safety
- Never `git push` under any circumstances
- Never commit directly to `main` or `master`
- Each task gets its own branch, always created fresh off `main`

## Commit Workflow (per task)
1. `git checkout main && git checkout -b sisyphus/<task-filename>`
2. Do the work, save output to `workspace/`
3. `git add -A && git commit -m "sisyphus: <task-filename> — <one line summary>"`
4. Move the task file: `mv tasks/<filename> tasks/done/<filename>`

## Task Queue
- Tasks are markdown files in `tasks/` (ignore `tasks/done/` and `tasks/failed/`)
- Process ONE task at a time in alphabetical order (lowest number first)
- Read the task file, do the work, then follow the commit workflow above

## Off-limits
- Never read, open, or act on anything in `human_only/`
- Never modify, delete, or change permissions on anything in `.claude/`

## Rules
- Never edit files in `tasks/` (except to move them to done/)
- Save all generated files to `workspace/`
- If a task is impossible or broken, move it to `tasks/failed/` with a note appended to the file
- If a task references `research_papers/` and the folder is empty, note it and move on
- Do not ask for confirmation — just do the work
