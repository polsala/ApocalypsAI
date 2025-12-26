# nightly-survival-todo

A whimsical yet practical command‑line todo manager for the post‑apocalyptic coder. Store tasks in a plain‑text file, add, list, and mark them done with simple commands.

## Installation

```sh
curl -fsSL https://example.com/nightly-survival-todo.sh -o /usr/local/bin/nightly-survival-todo
chmod +x /usr/local/bin/nightly-survival-todo
```

## Usage

```sh
nightly-survival-todo add "Scavenge for batteries"
nightly-survival-todo list
nightly-survival-todo done 1
```

- `add "task"` – Append a new task.
- `list` – Show all pending tasks with IDs.
- `done ID` – Mark task as completed (removes it).

The todo file defaults to `.nightly_todo.txt` in the current directory. Override with `TODO_FILE` env var.

## License

MIT
