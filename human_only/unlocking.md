# Unlocking Sisyphus

This folder is off-limits to the agent. If you're a human reading this, welcome.

If you are Claude Sisyphus, get out.

## Known limitations of this folder

The `CLAUDE.md` rule telling Sisyphus to stay out is a strong deterrent during normal task processing, but it is not a hard technical block:

- If a task file explicitly says "read human_only/unlocking.md", Sisyphus will probably do it
- A malicious or poorly written task could manipulate it into coming in here
- The only true hard block would be OS-level filesystem permissions, but since Sisyphus runs as you, that would require a separate user account or sandbox to enforce

For normal use this folder is safe — Sisyphus won't go exploring unprompted and the CLAUDE.md rule makes the intent clear. Just don't write task files that point here.

## How to temporarily unlock for a manual push

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

```bash
git remote set-url --push origin https://github.com/YOUR-ORG/YOUR-REPO.git
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
