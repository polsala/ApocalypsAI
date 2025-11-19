# Nightly Chronicle Keeper

## Preserve the Echoes of the End Times

The Nightly Chronicle Keeper is a humble utility designed to consolidate your scattered markdown notes, logs, and observations into a single, chronologically ordered "chronicle" file. In the chaos of the apocalypse, keeping track of events is paramount. This tool ensures your daily musings, agent reports, or critical findings are neatly organized for future generations (or just your next shift).

### Features

*   **Markdown Consolidation**: Gathers all `.md` files from a specified directory.
*   **Chronological Ordering**: Sorts entries based on dates found in filenames (e.g., `YYYY-MM-DD-report.md`) or, as a fallback, file modification times.
*   **Clear Entry Headers**: Each consolidated entry is prefixed with a clear markdown header indicating its date.
*   **Self-Contained**: A single Python script with no external dependencies beyond the standard library.

### Usage

```bash
python src/chronicle_keeper.py --input-dir /path/to/your/notes --output-file /path/to/your/chronicle.md
```

#### Arguments:

*   `--input-dir <path>`: The directory containing your markdown files.
*   `--output-file <path>`: The path to the output markdown file where the chronicle will be written.

### Example

Given an `input_notes/` directory with:

*   `2023-10-26-daily-log.md`
*   `report-2023-10-25.md`
*   `misc-notes.md` (modified on 2023-10-27)

Running the utility would produce `my_chronicle.md` with content ordered:

```markdown
# ApocalypsAI Chronicle

## Chronicle Entry: 2023-10-25
(Content of report-2023-10-25.md)

## Chronicle Entry: 2023-10-26
(Content of 2023-10-26-daily-log.md)

## Chronicle Entry: 2023-10-27
(Content of misc-notes.md)
```
