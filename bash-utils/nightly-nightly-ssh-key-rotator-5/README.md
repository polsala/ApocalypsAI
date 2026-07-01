# nightly-ssh-key-rotator

**Purpose**: Quickly generate a new SSH key pair for a given user and push the public key to a set of remote hosts. Perfect for a periodic "key rotation" ritual in your DevOps workflow.

## Installation

```bash
# Clone the repository (or copy the script) into a directory in your $PATH
git clone https://github.com/polsala/ApocalypsAI.git
cp utils/nightly-ssh-key-rotator/src/rotate_ssh_key.sh /usr/local/bin/rotate_ssh_key
chmod +x /usr/local/bin/rotate_ssh_key
```

## Usage

```bash
rotate_ssh_key.sh -u <remote_user> -h "host1 host2 host3" [-p <key_prefix>]
```

- `-u` **(required)** – The username on the remote hosts that will receive the new public key.
- `-h` **(required)** – Space‑separated list of hostnames or IP addresses.
- `-p` *(optional)* – Prefix for the generated key files. Defaults to `id_rsa_rotated` and will be placed in `~/.ssh/`.

### Example

```bash
rotate_ssh_key.sh -u deploy -h "app01.example.com app02.example.com" -p "id_rsa_daily"
```

This will:
1. Create `~/.ssh/id_rsa_daily` and `~/.ssh/id_rsa_daily.pub`.
2. Run `ssh-copy-id` for each host, installing the new public key for the `deploy` user.
3. Leave the old keys untouched – you can manually prune them later.

## Safety notes

- The script **does not** delete old keys; it only adds the new one.
- It uses `ssh-keygen` and `ssh-copy-id` under the hood, so ensure those utilities are installed on the machine running the script.
- For testing, the script respects the `PATH` order, allowing you to inject mock versions of `ssh-keygen` and `ssh-copy-id`.

## Testing

Run the bundled test suite with:

```bash
cd utils/nightly-ssh-key-rotator/tests
bash test_rotate_ssh_key.sh
```

The tests use mock binaries to verify behaviour without touching real hosts.
