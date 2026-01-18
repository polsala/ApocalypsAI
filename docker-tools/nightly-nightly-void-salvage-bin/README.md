# nightly-void-salvage-bin

A post-apocalyptic data obfuscation and archival utility, packaged in a Docker container. Perfect for securely "salvaging" sensitive files before deletion or long-term storage.

## Features

- Obfuscates file contents using a custom cipher
- Archives obfuscated files into a `.tar.gz` container
- Outputs a checksum for verification
- Fully containerized for portability

## Usage

```bash
# Build the container
docker build -t void-salvage-bin .

# Salvage a file
docker run --rm -v $(pwd):/data void-salvage-bin /data/sensitive.txt

# Output: sensitive.txt.salvaged.tar.gz
```

## Example

```bash
docker run --rm -v $(pwd):/data void-salvage-bin /data/launch_codes.txt
# Outputs: launch_codes.txt.salvaged.tar.gz
```
