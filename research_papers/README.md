# Research Papers / Reference Material Drop Zone

Drop papers, docs, or reference material here before running the queue.

If your mission involves research or analysis, add a task that reads this folder
and extracts techniques or ideas relevant to your goals. Sisyphus will process
whatever you leave here — PDFs, markdown summaries, plain text, or arxiv LaTeX source.

## Format

- PDFs from arxiv, docs, or blog exports
- Markdown or plain text summaries
- LaTeX source archives (`.tar.gz`) from arxiv
- Name files descriptively: `attention_paper_2024.pdf`, `profiling_notes.md`

## Downloading arxiv papers

A helper script is included — edit the `PAPERS` list and run:

```bash
pip install arxiv certifi
python research_papers/download_papers.py
```

This fetches LaTeX source (`.tar.gz`) for each paper ID directly from arxiv.
To read a downloaded paper: `tar -xzf <file>.tar.gz -C /tmp/paper/`

## Examples of what to put here

For ML / systems work:
- New algorithms you want Sisyphus to evaluate for applicability
- Benchmark methodology papers
- Prior art on the problem you're solving

For software projects:
- Design docs or specs for features you want built
- API documentation for libraries being used
- Architecture decision records

This folder is optional — if empty, tasks that reference it should skip gracefully.
