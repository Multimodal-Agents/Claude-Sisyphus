# Operator Prompt Reference

Copy and paste these prompts directly into Claude Code. You do not need to know any git commands.

---

## Unlocking for a manual push

**Step 1 — Unlock everything:**
```
Unlock Sisyphus for a manual push: remove the read-only flags from .claude/settings.json and .git/hooks/pre-push, disable the pre-push hook, and restore the push remote URL to https://github.com/YOUR-ORG/YOUR-REPO.git
```

**Step 2 — Push:**
```
Push the current branch to origin
```

**Step 3 — Lock it back down:**
```
Re-lock Sisyphus: enable the pre-push hook, set the push remote URL back to no_push, and mark .claude/settings.json and .git/hooks/pre-push as read-only
```

---

## Checking the current lock status

```
Check the Sisyphus lock status: is the pre-push hook active, are .claude/settings.json and .git/hooks/pre-push read-only, and what is the current push remote URL?
```

---

## Adding new tasks to the queue

```
Add a new task to the Sisyphus queue. Name it the next number in sequence after the highest existing task in tasks/ and call it [YOUR TASK NAME]. The task should do the following: [DESCRIBE YOUR TASK]
```

---

## Checking queue status

```
Show me the current Sisyphus queue status: list all pending tasks in tasks/, completed tasks in tasks/done/, and any failed tasks in tasks/failed/
```

---

## Clearing failed tasks

```
Show me the contents of all files in tasks/failed/ so I can decide what to do with them
```

```
Move all failed tasks back to tasks/ so Sisyphus will retry them on the next run
```

---

## Resetting the queue

```
Archive the workspace and reset the Sisyphus queue: move everything in workspace/ to a timestamped folder, and move all tasks in tasks/done/ and tasks/failed/ to that same archive folder
```

---

## Running the queue

After enabling Bypass Permissions, type this directly into the Claude Code input — it is a slash command, not a prompt:

```
/loop Process the task queue
```

---

## Re-locking after a fresh clone

If you have cloned the repo on a new machine and need to set up the locks:

```
Set up Sisyphus lock protection on this fresh clone: enable the pre-push hook using scripts/hook.bat on (Windows) or bash scripts/hook.sh on (Mac/Linux), mark .claude/settings.json and .git/hooks/pre-push as read-only, and set the push remote URL to no_push
```

---

## Notes

- Always re-lock after pushing. If you forget, run the re-lock prompt above.
- The `/loop` command is a Claude Code slash command — it will not work as a regular prompt. You must type it into the Claude Code input directly.
- If a prompt gets refused due to permission rules, that means the lock is working. Unlock first, then try again.
