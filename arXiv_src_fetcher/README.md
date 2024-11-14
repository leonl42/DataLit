# How to use
1. Place one of the OpenReview scraped .json files from [paperlists](https://github.com/papercopilot/paperlists?tab=readme-ov-file) in this directory.
2. Run `python arXiv_fetcher.py  --json_file FILENAME` with an optional `--limit` parameter in this directory.

# What it does
1. Goes through the json and looks up the arXiv ID using the paper title and the arXiv API.
2. Downloads and extracts the source files of each paper into a folder named the same as the json, where each papers source files are contained in a folder named with its OpenReview id (i.e. `id` field of the json).
3. Writes some additional stats about how many of the papers were on arXiv to that same folder.
