# Nightly Survival Tip Generator

Generates a `survival_tip.txt` file in the current directory containing a whimsical yet practical survival tip. Useful for daily motivation in post‑apocalyptic settings.

## Usage

```bash
ansible-playbook -i src/inventory.ini src/tip_generator.yml
```

The playbook creates (or overwrites) `survival_tip.txt` with the tip.

## Testing

Run the test playbook:

```bash
ansible-playbook -i src/inventory.ini tests/test_tip_generator.yml
```

It will verify that the file exists and contains the expected tip.
