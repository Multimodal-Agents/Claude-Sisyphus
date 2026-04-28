# Claude-Sisyphus

An autonomous task queue runner for Claude Code. Drop task files into `tasks/`, run one command, and Claude works through them one by one — committing after each, never pushing.

---

## How It Works

Tasks are markdown files in `tasks/`. Claude reads them in alphabetical order, does the work, saves output to `workspace/`, commits, and moves the task to `tasks/done/`. It loops until the queue is empty.

```
tasks/
  001_build_thing.md     ← processed first
  002_improve_it.md
  done/
    000_previous.md      ← already done
workspace/
  output.html            ← generated files live here
```

---

## Running It

### Step 1 — Enable "Bypass permissions"

At the bottom of the Claude Code window, turn on **Bypass permissions**. This lets Claude run shell commands and edit files without prompting you on each action.

### Step 2 — Run the loop command

```
/loop Process the task queue
```

Claude will keep processing tasks until the queue is empty. You can watch it work or walk away.

![Sisyphus demo — bypass permissions enabled and /loop command running](assets/sisyphus-demo.png)

---

## Push Protection Hook

By default, the push-blocking hook is **off**. Claude will only commit locally — it never pushes — but with the hook disabled you can push manually if you want.

To **enable** the hook (block all pushes, even manual ones):

```bash
cp hooks/pre-push .git/hooks/pre-push
chmod +x .git/hooks/pre-push
```

To **disable** the hook:

```bash
rm .git/hooks/pre-push
```

The hook script lives in [`hooks/pre-push`](hooks/pre-push) and can be inspected or modified there.

---

## Writing Tasks

Each task file is a plain markdown file. Write it like a prompt — be specific about what you want built and where to save it.

Example (`tasks/001_build_thing.md`):

```markdown
Build a single-page HTML todo app. Save it to workspace/todo.html.
Requirements:
- Add/remove items
- Persist to localStorage
- Clean dark UI
```

Tasks are processed in filename order (`001_` before `002_`, etc.), so numbering controls the sequence.

---

## Project Structure

```
.
├── hooks/
│   └── pre-push          # install to .git/hooks/ to block pushes
├── tasks/
│   ├── done/             # completed tasks land here
│   └── failed/           # broken/impossible tasks land here
├── workspace/            # all generated output goes here
├── assets/               # images for this README
├── CLAUDE.md             # rules Claude follows (do not delete)
└── README.md
```
