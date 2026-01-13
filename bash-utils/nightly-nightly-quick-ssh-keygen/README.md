Nightly Quick SSH Keygen
========================

A whimsical Bash utility that quickly generates an RSA key pair and prints the public key.

Usage
-----

```bash
./src/main.sh [--comment <comment>] [--output <path>]
```

Options
-------

- `--comment <comment>`: Comment to add to the public key. Default: `nightly-key`.
- `--output <path>`: Directory to write the key pair. Default: current directory.

Examples
--------

```bash
# Generate a key pair in the current directory
./src/main.sh

# Generate a key pair with a custom comment
./src/main.sh --comment "my-awesome-key"

# Generate a key pair in a specific directory
./src/main.sh --output /tmp/keys
```

The script will output the path to the private key and the public key, and will also print the public key content to stdout.

Testing
-------

Run the test suite:

```bash
bash tests/test_main.sh
```
