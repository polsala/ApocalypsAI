# nightly-ssh-key-rotator

Utility to rotate SSH key pairs for a given `.ssh` directory. It backs up existing `id_rsa` and `id_rsa.pub` to `id_rsa.old` and `id_rsa.pub.old`, then creates new dummy key files. In real usage replace the dummy generation with `ssh-keygen`.

## Usage

```sh
./src/rotate_ssh_keys.sh /path/to/.ssh
```

## How it works

1. Verify the target directory exists.
2. Move existing `id_rsa` and `id_rsa.pub` to `.old` backups.
3. Write placeholder key contents to new files.
4. Set appropriate permissions.

## Testing

Run the test suite:

```sh
bash tests/test_rotate_ssh_keys.sh
```
