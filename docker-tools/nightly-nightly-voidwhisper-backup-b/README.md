# nightly-voidwhisper-backup-buddy

A Dockerized utility to securely archive and encrypt your files.

## Features

- Archives directories into compressed tarballs
- Optional AES-256 encryption with user-provided passphrase
- Timestamped backups for easy identification
- Lightweight Alpine-based image

## Usage

```bash
# Without encryption
docker run --rm -v $(pwd):/data -v /path/to/backups:/backups voidwhisper-backup-buddy /data/mydir

# With encryption
docker run --rm -v $(pwd):/data -v /path/to/backups:/backups -e PASSPHRASE='secret123' voidwhisper-backup-buddy /data/mydir
```

Backups are saved to `/backups` inside the container.

## Build

```bash
docker build -t voidwhisper-backup-buddy .
```
