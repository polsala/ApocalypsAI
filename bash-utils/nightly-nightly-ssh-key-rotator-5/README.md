# nightly-ssh-key-rotator

**Purpose**: Rotate your SSH key pair safely while keeping a timestamped backup of the old keys. After the rotation a random post‑apocalyptic quote is printed to remind you that even in the end‑times, security matters.

## How it works
1. Looks for `~/.ssh/id_rsa` and `~/.ssh/id_rsa.pub`.
2. If they exist, copies them into a backup directory named `~/.ssh/backup_<TIMESTAMP>`.
3. Generates a new RSA‑2048 key pair with an empty passphrase.
4. Prints a random, whimsical quote.

## Usage
```bash
# Make the script executable (once)
chmod +x src/rotate_ssh_keys.sh

# Run it (it uses $HOME to locate the .ssh folder)
./src/rotate_ssh_keys.sh
```

### Testing
The test suite lives in `tests/test_rotate_ssh_keys.sh` and can be executed with:
```bash
bash tests/test_rotate_ssh_keys.sh
```
It creates a temporary HOME, injects a deterministic date via `DATE_OVERRIDE`, and verifies that:
* A backup directory is created with the expected timestamp.
* The original key files are copied into the backup.
* New key files are generated.
* The output contains one of the predefined quotes.

## Customisation
* **Key type / size** – modify the `ssh-keygen` arguments in the script.
* **Quote list** – add or change entries in the `quotes` array.
* **Backup naming** – change the `backup_dir` pattern if you prefer a different scheme.

---
*This utility is deliberately self‑contained and requires only the standard `ssh-keygen` binary that ships with OpenSSH.*
