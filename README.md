# Claude-Sisyphus

An autonomous task queue runner for Claude Code. Write task files, run one command, and Claude works through them one by one — committing after each, never pushing, until the queue is empty.

![Sisyphus demo — bypass permissions enabled and /loop command running](assets/sisyphus-demo.png)

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

Tasks are plain markdown files in the `tasks/` folder. Name them with a number prefix — Claude processes them in order, lowest number first.

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

All generated files get saved to `workspace/` automatically.

### 3. Open Claude Code in your project folder

Launch Claude Code (CLI, desktop app, or IDE extension) with the project root as your working directory.

---

## Running the Task Queue

### Step 1 — Turn on "Bypass permissions"

At the bottom of the Claude Code window, enable **Bypass permissions**.

> This allows Claude to run shell commands, read and write files, and commit to git without asking for approval on every action. Without it, Claude will pause and prompt you constantly.

### Step 2 — Run the loop command

Type this in the Claude Code input and press Enter:

```
/loop Process the task queue
```

Claude will read tasks one at a time, do the work, commit, move the task to `tasks/done/`, and repeat until the queue is empty. You can watch it or walk away.

---

## Push Protection Hook

`CLAUDE.md` tells Claude not to push — but that's just an instruction. The hook is what **actually enforces it** at the git level, making it physically impossible for any push to succeed, whether it comes from Claude or from you manually.

By default the hook is **off**. We recommend installing it before running Sisyphus so there's a hard guarantee nothing reaches your remote while the agent is working.

### Enable the hook

**Mac / Linux:**
```bash
cp hooks/pre-push .git/hooks/pre-push
chmod +x .git/hooks/pre-push
```

**Windows (PowerShell or Command Prompt):**
```powershell
copy hooks\pre-push .git\hooks\pre-push
```
> No `chmod` needed on Windows — git hooks don't require file permissions here.

**Windows (Git Bash):**
```bash
cp hooks/pre-push .git/hooks/pre-push
```

Once installed, any `git push` will be blocked with a message until you remove the hook.

### Disable the hook

**Mac / Linux / Git Bash:**
```bash
rm .git/hooks/pre-push
```

**Windows (PowerShell or Command Prompt):**
```powershell
del .git\hooks\pre-push
```

---

## How Tasks Move Through the Queue

```
tasks/001_build_homepage.md   ← Claude reads this
        ↓ does the work
workspace/index.html          ← output saved here
        ↓ git commit
tasks/done/001_build_homepage.md  ← task archived
        ↓ moves to next task
tasks/002_add_dark_mode.md    ← repeat
```

If a task is impossible or broken, Claude moves it to `tasks/failed/` with a note explaining why.

---

## Project Structure

```
.
├── hooks/
│   └── pre-push          # copy to .git/hooks/ to block all pushes
├── tasks/
│   ├── 001_your_task.md  # add your tasks here
│   ├── done/             # completed tasks are moved here automatically
│   └── failed/           # broken tasks land here with an explanation
├── workspace/            # all generated output goes here
├── assets/               # images used in this README
├── CLAUDE.md             # rules the agent follows — do not delete or edit
└── README.md
```

---

## Tips

- **Number your tasks** with zero-padded prefixes (`001_`, `002_`) so the order is predictable.
- **Be specific in task files** — vague prompts lead to vague output. Include file paths, requirements, and constraints.
- **Check `tasks/failed/`** if Claude gets stuck — the file will have a note about what went wrong.
- **Don't edit `CLAUDE.md`** — it contains the rules the agent follows to keep commits clean and pushes blocked.
