# Sisyphus — Claude Code Rules

## Mission
<!-- Replace this section with your specific mission.
     Be concrete: what are you building, optimizing, or researching?
     What is the success metric? Where do results go?

     Example (included in tasks/ as a demo):
     "You are iteratively improving workspace/snake.html into a full-featured
     browser game. Each task adds one feature. Commit after every task." -->

## Git Safety
- Never `git push` under any circumstances
- Never commit to `main` or `master` — always work on a branch named `sisyphus/<task-filename>`
- After completing each task: `git add -A && git commit -m "sisyphus: <task-filename> — <one line summary>"`

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
