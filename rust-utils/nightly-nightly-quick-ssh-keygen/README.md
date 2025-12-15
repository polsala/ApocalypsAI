# nightly-quick-ssh-keygen

A tiny Rust command‑line tool that generates a 2048‑bit RSA SSH key pair in a single command.

## Features

* Generates a private key in PEM format and a public key in OpenSSH format.
* Writes the key files to a user‑specified directory (defaults to the current working directory).
* Prints the public key to stdout so you can paste it directly into `authorized_keys`.
* Includes a short whimsical message after key generation.

## Installation

```bash
# Using Cargo (recommended)
cargo install nightly-quick-ssh-keygen
```

If you prefer to build from source:

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/utils/nightly-quick-ssh-keygen
cargo build --release
./target/release/nightly-quick-ssh-keygen
```

## Usage

```bash
# Generate keys in the current directory with default name `id_rsa`
nightly-quick-ssh-keygen

# Generate keys in /tmp/keys with custom name `mykey`
nightly-quick-ssh-keygen /tmp/keys mykey
```

After running, you will find:

```
/tmp/keys/mykey          # Private key (PEM)
/tmp/keys/mykey.pub      # Public key (OpenSSH)
```

The public key is also printed to stdout.

## Example Output

```
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC... user@example.com
Key pair generated: /tmp/keys/mykey and /tmp/keys/mykey.pub
```

## License

MIT
