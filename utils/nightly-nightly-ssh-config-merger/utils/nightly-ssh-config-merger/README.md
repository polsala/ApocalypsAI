# Nightly SSH Config Merger

A tiny, self‑contained Python utility that merges a collection of SSH `config` snippet files into one consolidated configuration.

## Features

- **Directory based** – Drop any number of snippet files (any extension) into a folder and point the tool at it.
- **Deduplication** – If the same `Host` appears in multiple snippets, the first occurrence wins and later duplicates are ignored.
- **Preserves ordering** – Snippets are processed in lexical order, making the merge deterministic.
- **Zero external dependencies** – Only the Python standard library is used.

## Installation

Copy the `src/merge_ssh_config.py` script into your PATH or invoke it via `python -m utils.nightly-ssh-config-merger.src.merge_ssh_config`.

```bash
# Example usage
python utils/nightly-ssh-config-merger/src/merge_ssh_config.py \
    --input-dir ./ssh-snippets \
    --output-file ./merged_config
```

## CLI Arguments

| Argument | Description |
|----------|-------------|
| `--input-dir` | Directory containing the snippet files. All regular files are read (sorted alphabetically). |
| `--output-file` | Destination file for the merged configuration. If the file exists it will be overwritten. |

## How it works

The script reads each file line‑by‑line, tracks `Host` declarations, and writes lines to the output only if the host has not been seen before. Non‑`Host` lines are always written.

## Testing

Run the bundled tests with `pytest`:

```bash
pytest utils/nightly-ssh-config-merger/tests
```

---

*Created by the ApocalypsAI Nightly Integrator.*
