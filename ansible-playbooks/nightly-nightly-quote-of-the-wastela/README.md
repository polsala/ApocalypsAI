# Nightly Quote of the Wasteland

Utility that, when run, picks a random post‑apocalyptic motivational quote and writes it to `/var/wasteland/quotes/<timestamp>.txt`. Useful for adding a touch of bleak optimism to your servers.

## Usage

```bash
ansible-playbook -i utils/nightly-quote-of-the-wasteland/src/inventory.ini utils/nightly-quote-of-the-wasteland/src/playbook.yml
```

## How it works

- Defines a list of quotes.
- Uses Ansible's `random` filter to pick one.
- Creates the target directory.
- Writes the quote to a timestamped file.

## Testing

Run the test playbook:

```bash
ansible-playbook -i utils/nightly-quote-of-the-wasteland/src/inventory.ini utils/nightly-quote-of-the-wasteland/tests/test_playbook.yml
```
