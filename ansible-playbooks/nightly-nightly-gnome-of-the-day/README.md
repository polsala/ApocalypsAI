# Nightly Gnome of the Day

An Ansible playbook that creates a whimsical "Gnome of the Day" text file with a motivational quote. The quote is selected deterministically based on the current day of month, ensuring reproducible results for testing.

## Usage

```bash
ansible-playbook -i inventory.ini src/playbook.yml
```

It will generate `/tmp/gnome_of_the_day.txt` containing the selected quote.

## Files

- `src/playbook.yml` – main playbook.
- `vars/quotes.yml` – list of gnome quotes.
- `templates/quote.j2` – Jinja2 template for the output file.
- `inventory.ini` – simple localhost inventory.
- `tests/test_playbook.sh` – automated test.
