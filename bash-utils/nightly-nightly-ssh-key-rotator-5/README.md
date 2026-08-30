# nightly-ssh-key-rotator

Utility to rotate a user's SSH key pair safely. Generates a new RSA key pair, backs up the existing `authorized_keys`, and installs the new public key. Includes a `--mock-keygen` flag for testing without invoking `ssh-keygen`.

## Usage

```sh
./rotate_ssh_key.sh -u <username> -d <ssh_dir> [--mock-keygen]
```

### Options

- `-u` **username** – Identifier used only for logging/clarity.
- `-d` **ssh_dir** – Path to the user's `.ssh` directory (must contain `authorized_keys`).
- `--mock-keygen` – Generate placeholder keys instead of calling `ssh-keygen`. Useful for automated tests or environments without `ssh-keygen`.

The script creates `id_rsa_new` and `id_rsa_new.pub` inside the supplied directory, backs up the existing `authorized_keys` to `authorized_keys.bak`, and replaces `authorized_keys` with the newly generated public key.

## Example

```sh
# Rotate keys for user "alice" whose .ssh folder is /home/alice/.ssh
./rotate_ssh_key.sh -u alice -d /home/alice/.ssh
```

## Testing

Run the provided test suite with:

```sh
cd tests && bash test_rotate_ssh_key.sh
```

The test uses the `--mock-keygen` flag to avoid real key generation.
