# nightly-ansible-survival-tip-generator

## Overview

This utility is an **Ansible playbook** that picks a random‑looking "survival tip of the day" from a curated list and writes it to `survival_tip.txt` in the current working directory.  It can be run locally on any machine with Ansible installed and requires no external network access, making it safe for offline environments.

## Why?

* **Whimsical morale boost** – a daily tip like "Never trust a cactus with a secret" adds a splash of fun to routine DevOps chores.
* **Zero‑dependency** – only the standard Ansible modules (`copy`, `stat`, `assert`) are used.
* **Deterministic** – the tip is chosen based on the current day of the month, so the same day always yields the same tip, which keeps the test suite stable.

## Files

* `src/tip_generator.yml` – the main playbook.
* `src/tips.yml` – a YAML list of quirky survival tips.
* `inventory.ini` – a minimal inventory that points to `localhost`.
* `tests/test_tip_generator.yml` – an integration test that runs the playbook and verifies the output file exists and is non‑empty.

## Usage

```bash
# Install Ansible if you haven't already
pip install ansible

# Run the playbook
ansible-playbook -i inventory.ini src/tip_generator.yml
```

After execution, you will find a file called `survival_tip.txt` containing the tip for today.

## Running the Tests

```bash
ansible-playbook -i inventory.ini tests/test_tip_generator.yml
```

The test will:
1. Execute the main playbook.
2. Assert that `survival_tip.txt` was created.
3. Assert that the file is not empty.

All tests are deterministic and do **not** perform any network calls.
