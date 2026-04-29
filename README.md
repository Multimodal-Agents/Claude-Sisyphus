<div align="center">
  <img src="assets/logo.png" alt="Claude-Sisyphus" width="184"/><br/>
  <h1>Claude-Sisyphus</h1>
  <strong>An autonomous task queue runner for Claude Code.</strong><br/>
  Write tasks. Run one command. Walk away.
</div>

---

In [Greek mythology](https://en.wikipedia.org/wiki/Sisyphus), Sisyphus was condemned to roll a boulder up a hill for eternity, only for it to roll back down each time. This is that, but the boulder actually stays at the top.

Load up a queue of tasks and Claude will work through them relentlessly, reading, building, committing, moving on, one by one, for as long as there's work to do. It never loses its place. The queue state lives in the filesystem, not the conversation, so even after context compaction Claude just looks at `tasks/`, sees what isn't in `done/` yet, and picks up exactly where it left off.

The only things that stop it: the queue runs dry, or you run out of credits.

![Sisyphus demo showing bypass permissions enabled and the loop command running](assets/sisyphus-demo.png)

---

## Prerequisites

- [Claude Code](https://claude.ai/code) installed and signed in
- Git installed and initialized in your project

---

## Setup

### 1. Clone this repo

```bash
git clone https://github.com/Multimodal-Agents/Claude-Sisyphus.git
cd Claude-Sisyphus
```

### 2. Write your tasks

Tasks are plain markdown files in the `tasks/` folder. Name them with a number prefix. Claude processes them in alphabetical order, lowest number first.

```
tasks/
  001_build_homepage.md
  002_add_dark_mode.md
  003_write_tests.md
```

Write each task like a prompt. Be specific about what you want and where to save the output:

```markdown
# tasks/001_build_homepage.md

Build a single-page HTML landing page for a coffee shop.
Save it to workspace/index.html.

Requirements:
- Hero section with a tagline
- Menu section with 5 items
- Contact form (no backend needed)
- Clean, modern design with a warm color palette
```

All generated files are saved to `workspace/` automatically.

### 3. Open Claude Code in your project folder

Launch Claude Code (CLI, desktop app, or IDE extension) with the project root as your working directory.

---

## Running the Task Queue

### Step 1 - Turn on "Bypass permissions"

At the bottom of the Claude Code window, enable **Bypass permissions**.

> This allows Claude to run shell commands, read and write files, and commit to git without asking for approval on every action. Without it, Claude will pause and prompt you constantly.

### Step 2 - Run the loop command

Type this in the Claude Code input and press Enter:

```
/loop Process the task queue
```

Claude will read tasks one at a time, do the work, commit, move the task to `tasks/done/`, and repeat until the queue is empty. You can watch it or walk away.

---

## Push Protection Hook

`CLAUDE.md` tells Claude not to push, but that is just an instruction. The hook is what **actually enforces it** at the git level, making it physically impossible for any push to succeed, whether it comes from Claude or from you manually.

By default the hook is **off**. We recommend installing it before running Sisyphus so there is a hard guarantee nothing reaches your remote while the agent is working.

### Using the scripts (recommended)

The scripts handle everything for you and tell you the current status if you are not sure.

**Mac / Linux / Git Bash:**
```bash
bash scripts/hook.sh on    # enable - blocks all pushes
bash scripts/hook.sh off   # disable - pushes work normally
bash scripts/hook.sh       # check current status
```

**Windows (Command Prompt or PowerShell):**
```powershell
scripts\hook.bat on    # enable - blocks all pushes
scripts\hook.bat off   # disable - pushes work normally
scripts\hook.bat       # check current status
```

### Manual install (if you prefer not to use the scripts)

**Mac / Linux / Git Bash:**
```bash
# Enable
cp hooks/pre-push .git/hooks/pre-push
chmod +x .git/hooks/pre-push

# Disable
rm .git/hooks/pre-push
```

**Windows (Command Prompt or PowerShell):**
```powershell
# Enable
copy hooks\pre-push .git\hooks\pre-push

# Disable
del .git\hooks\pre-push
```

> **Note for Windows users:** You do not need `chmod`. Windows does not use file permissions for git hooks.

> **How it works:** Git looks for hook scripts in `.git/hooks/`. That folder is local to your machine and never pushed to GitHub, which is why the hook is off by default. Cloning the repo gives you the script in `hooks/`, but does not activate it until you install it.

---

## Hardening Against a Rogue Agent

The push protection hook and `CLAUDE.md` rules cover normal operation, but a sufficiently determined task could instruct Claude to disable them. Two extra steps close that gap.

### 1. Lock the permission rules

`CLAUDE.md` ships with a `.claude/settings.json` that uses Claude Code's built-in `permissions.deny` rules to block `git push`, hook script execution, and remote URL changes at the tool level — before any shell command runs.

To prevent a task from editing that file to remove the rules, mark it read-only:

**Mac / Linux:**
```bash
chmod 444 .claude/settings.json
chmod 444 .git/hooks/pre-push
```

**Windows (Command Prompt or PowerShell):**
```powershell
attrib +R .claude\settings.json
attrib +R .git\hooks\pre-push
```

When you need to push manually, full unlock instructions are in [`human_only/unlocking.md`](human_only/unlocking.md).

### 2. Disable the push remote

Set the push URL on `origin` to a dead value so that even if every other layer were bypassed, there is nowhere valid to push to:

```bash
git remote set-url --push origin no_push
```

With all three layers in place — read-only files, dead push URL, and the pre-push hook — a task would need to defeat all of them simultaneously to get anything off your machine.

---

## How Tasks Move Through the Queue

```
tasks/001_build_homepage.md      ← Claude reads this
        →  does the work
workspace/index.html             ← output saved here
        →  git commit
tasks/done/001_build_homepage.md ← task archived
        →  moves to next task
tasks/002_add_dark_mode.md       ← repeat
```

If a task is impossible or broken, Claude moves it to `tasks/failed/` with a note explaining why.

---

## Project Structure

```
.
├── hooks/
│   └── pre-push          # the hook script, installed by scripts/hook.sh or hook.bat
├── scripts/
│   ├── hook.sh           # manage the hook on Mac / Linux / Git Bash
│   └── hook.bat          # manage the hook on Windows
├── tasks/
│   ├── 001_your_task.md  # add your tasks here
│   ├── done/             # completed tasks are moved here automatically
│   └── failed/           # broken tasks land here with an explanation
├── workspace/            # all generated output goes here
├── human_only/           # operator notes, see inside
├── assets/               # images used in this README
├── CLAUDE.md             # rules the agent follows, do not delete or edit
└── README.md
```

---

## Tips

- **Number your tasks** with zero-padded prefixes (`001_`, `002_`) so the order is always predictable.
- **Be specific in task files.** Vague prompts lead to vague output. Include file paths, requirements, and any constraints.
- **Check `tasks/failed/`** if Claude gets stuck. The file will have a note about what went wrong.
- **Do not edit `CLAUDE.md`.** It contains the rules the agent follows to keep commits clean and pushes blocked.
- **The hook is per-clone.** If you clone the repo on a new machine, you will need to run the install script again.

---

## Roadmap

- **Failed task retry** - a `tasks/retry/` folder and attempt counter in the filename (`001_build_thing.attempt2.md`) so Claude can try again with context from the previous failure
- **Task dependencies** - a `depends_on: 003` header in task files so Claude can skip blocked tasks instead of failing
- **Task output manifest** - after each task, append a one-line summary to `workspace/MANIFEST.md` for a clean audit trail without spelunking commits
- **Task templates** - a `tasks/templates/` folder with common patterns (refactor, research, bugfix) so you can queue new work fast
- **Utility scripts** - helper scripts for common operations like bulk-creating task files, archiving the workspace, and resetting the queue
- **Local sub-agent support** - scripts for spinning up and routing tasks to local model servers (llama.cpp, vLLM) as drop-in Claude alternatives
