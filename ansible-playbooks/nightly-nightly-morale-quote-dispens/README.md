# nightly‑morale‑quote‑dispenser

## Overview

`nightly-morale-quote-dispenser` is a whimsical yet useful Ansible playbook that:

1. Picks a random morale‑boosting quote from a built‑in list.
2. Writes the quote to a configurable file (default: `/etc/morale_of_the_day.txt`).
3. Installs a tiny shell script in `/etc/profile.d/` that prints the quote each time a user opens a new shell session.

The playbook is completely self‑contained – no external APIs or internet access are required – making it safe to run in isolated or offline environments.

## Files

- `src/morale_dispenser.yml` – The main playbook.
- `src/inventory.ini` – Simple inventory targeting `localhost`.
- `tests/test_morale_dispenser.yml` – Automated test that validates the playbook creates the quote file and that the content is one of the expected quotes.

## Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `morale_path` | `/etc/morale_of_the_day.txt` | Destination file for the random quote. |
| `script_path` | `/etc/profile.d/morale.sh` | Path of the shell script that prints the quote on login. |
| `quotes` | (list of four built‑in quotes) | The pool of possible morale quotes. |

You can override any of these variables on the command line, e.g.:

```bash
ansible-playbook -i src/inventory.ini src/morale_dispenser.yml \
  -e "morale_path=/tmp/morale.txt script_path=/tmp/morale.sh"
```

## Running the Playbook

```bash
# Install the quote (requires root to write to /etc)
ansible-playbook -i src/inventory.ini src/morale_dispenser.yml
```

After a successful run, opening a new terminal will display a random morale quote.

## Testing

The repository includes an offline test suite that can be executed with:

```bash
ansible-playbook -i src/inventory.ini tests/test_morale_dispenser.yml
```

The test runs the playbook against a temporary location (`/tmp`) and asserts that the quote file exists and contains one of the expected quotes.
