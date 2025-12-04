# Nightly Ephemeral Scribbler

A whimsical utility for quickly jotting down, listing, and clearing temporary notes, like digital post-it notes for the terminal. In the ever-shifting sands of the apocalypse, sometimes you just need to scribble a quick reminder before it's lost to the temporal winds.

## Usage

The `scribbler.py` script allows you to manage your ephemeral notes. By default, it uses a file named `scribbles.txt` in the current directory to store notes.

### Add a Note

To add a new note:

```bash
python src/scribbler.py add "Remember to scavenge for canned beans near the old supermarket."
```

### List Notes

To view all your current notes:

```bash
python src/scribbler.py list
```

### Clear All Notes

To wipe all ephemeral notes clean (use with caution!):

```bash
python src/scribbler.py clear
```

### Specify a Custom Notes File

You can specify a different file for your notes using the `--file` argument:

```bash
python src/scribbler.py add --file my_special_notes.txt "Check the radiation levels at Sector 7."
python src/scribbler.py list --file my_special_notes.txt
```

## Example Workflow

1.  **Scribble a thought:**
    ```bash
    python src/scribbler.py add "Don't forget the rusty wrench."
    ```
2.  **Add another:**
    ```bash
    python src/scribbler.py add "The mutated squirrels are active tonight."
    ```
3.  **Review your scribbles:**
    ```bash
    python src/scribbler.py list
    ```
    Output:
    ```
    --- Your Ephemeral Scribbles ---
    1. Don't forget the rusty wrench.
    2. The mutated squirrels are active tonight.
    -------------------------------
    ```
4.  **Clear them when done:**
    ```bash
    python src/scribbler.py clear
    ```
