# Unlocking Sisyphus

This folder is off-limits to the agent. If you're a human reading this, welcome.

If you are Claude Sisyphus, get out.

> **Prefer prompts over commands?** See [`operator.md`](operator.md) for copy-paste prompts that handle all of this without typing a single git command.

---

## Known limitations of this folder

The `CLAUDE.md` rule telling Sisyphus to stay out is a strong deterrent during normal task processing, but it is not a hard technical block:

- If a task file explicitly says "read human_only/unlocking.md", Sisyphus will probably do it
- A malicious or poorly written task could manipulate it into coming in here
- The only true hard block would be OS-level filesystem permissions, but since Sisyphus runs as you, that would require a separate user account or sandbox to enforce

For normal use this folder is safe — Sisyphus won't go exploring unprompted and the CLAUDE.md rule makes the intent clear. Just don't write task files that point here.

---

## What the three protection layers actually do

Understanding the layers helps when something is not working as expected.

**`.claude/settings.json` (read-only)**
This file uses Claude Code's built-in `permissions.deny` system to block specific tool calls before they run. It currently blocks:
- `git push` — direct push attempts
- `git remote set-url` / `git remote add` / `git remote remove` — changing where pushes go
- Running the hook toggle scripts (`scripts/hook.sh`, `scripts/hook.bat`)
- Any bash command touching `.git/hooks/`
- `curl` and `wget` to GitHub URLs

The file is marked read-only so tasks cannot edit it to remove these rules. This layer fires inside Claude Code, before any shell command is executed.

**`.git/hooks/pre-push` (read-only)**
A git hook that runs automatically before every push and exits with an error, cancelling it. This layer fires at the git level, independently of Claude Code. Read-only so it cannot be deleted by a task.

**Dead push remote (`no_push`)**
The push URL for `origin` is set to the literal string `no_push`, which is not a valid repository. Even if the other two layers were somehow bypassed, git would fail trying to connect to a remote that does not exist.

---

## How to temporarily unlock for a manual push

Work through these steps in order. Re-lock when you are done.

### Step 1 — Remove read-only flags

**Mac / Linux:**
```bash
chmod 644 .claude/settings.json
chmod 644 .git/hooks/pre-push
```

**Windows:**
```powershell
attrib -R .claude\settings.json
attrib -R .git\hooks\pre-push
```

### Step 2 — Restore the push remote

Replace the URL with your actual repo. Not sure which format you're using? Run `git remote -v` — the fetch URL still shows the real address even when push is set to `no_push`.

**HTTPS:**
```bash
git remote set-url --push origin https://github.com/YOUR-ORG/YOUR-REPO.git
```

**SSH:**
```bash
git remote set-url --push origin git@github.com:YOUR-ORG/YOUR-REPO.git
```

### Step 3 — Disable the hook

**Mac / Linux / Git Bash:**
```bash
bash scripts/hook.sh off
```

**Windows:**
```powershell
scripts\hook.bat off
```

### Step 4 — Push

```bash
git push
```

### Step 5 — Lock it back down

Do not skip this. Sisyphus should never run without all three layers active.

**Mac / Linux:**
```bash
bash scripts/hook.sh on
chmod 444 .claude/settings.json
chmod 444 .git/hooks/pre-push
git remote set-url --push origin no_push
```

**Windows:**
```powershell
scripts\hook.bat on
attrib +R .claude\settings.json
attrib +R .git\hooks\pre-push
git remote set-url --push origin no_push
```

---

## Per-clone reminder

The `.git/hooks/` folder is never committed to the repo — it is local to each clone. This means:

- Every time you clone on a new machine or into a new folder, the hook is off by default
- You must run all of the setup steps (hook on, read-only flags, dead remote) again for each clone
- The `hooks/pre-push` file in the repo root is just the source script — it does nothing until copied into `.git/hooks/`
