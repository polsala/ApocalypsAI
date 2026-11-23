# Nightly SSH Key Rotator

Utility to generate a fresh SSH key pair for a given user and distribute the public key to a list of remote hosts. Keeps your access credentials as fresh as a post‑apocalyptic bunker’s air filters.

## Usage

```sh
./rotate_ssh_keys.sh -u <username> -f <hosts_file> [-d <key_dir>]
```

- `-u` – remote username (required)
- `-f` – path to a file containing one host per line (required)
- `-d` – directory to store the new key pair (default: `$HOME/.ssh/rotated`)

The script will:

1. Generate a new ed25519 key pair (no passphrase).
2. Copy the public key to each host using `ssh-copy-id`.
3. Print a summary of actions.

## Example

```sh
hosts.txt:
host1.example.com
host2.example.com

./rotate_ssh_keys.sh -u alice -f hosts.txt
```

## Safety

The script never deletes existing keys; it stores the new pair in a separate directory. Review the generated keys before removing old ones.

## Testing

Run the bundled tests with:

```sh
bash tests/test_rotate_ssh_keys.sh
```
