#!/usr/bin/env python3
"""
Download arxiv papers as LaTeX source (tar.gz) into this directory.
Edit the PAPERS list below, then run: python download_papers.py
Requires: pip install arxiv certifi
"""

import os
import ssl
import certifi
import time

os.environ['SSL_CERT_FILE'] = certifi.where()
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

import arxiv

# Add papers as ("arxiv_id", "short_slug") tuples.
# Find the ID in the arxiv URL: arxiv.org/abs/2307.08691  →  "2307.08691"
PAPERS = [
    # ("2307.08691", "flashattention2"),
    # ("2106.09685", "lora"),
]

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
client = arxiv.Client(num_retries=3, delay_seconds=3)


def download_all():
    if not PAPERS:
        print("PAPERS list is empty — add arxiv IDs to download_papers.py")
        return

    already = {f for f in os.listdir(OUTPUT_DIR) if f.endswith('.tar.gz')}
    print(f"Found {len(already)} already downloaded.\n")

    for arxiv_id, slug in PAPERS:
        filename = f"{arxiv_id}_{slug}.tar.gz"
        if filename in already:
            print(f"  SKIP  {arxiv_id} — {slug}")
            continue
        try:
            search = arxiv.Search(id_list=[arxiv_id])
            paper = next(client.results(search))
            dest = paper.download_source(dirpath=OUTPUT_DIR, filename=f"{arxiv_id}_{slug}")
            if os.path.exists(dest) and not dest.endswith('.tar.gz'):
                os.rename(dest, dest + '.tar.gz')
            print(f"  OK    {arxiv_id} — {paper.title[:60]}")
        except StopIteration:
            print(f"  MISS  {arxiv_id} — not found on arxiv")
        except Exception as e:
            print(f"  ERR   {arxiv_id} — {e}")
        time.sleep(1)

    print("\nDone.")


if __name__ == "__main__":
    download_all()
