# nightly-void-salvage-bin

A Dockerized terminal command archival tool that encrypts and stores shell commands as 'salvaged artifacts'. Perfect for post-apocalyptic DevOps!

## Features

- Encrypts and stores terminal commands
- Retrieves and decrypts archived commands
- Dockerized for portability and containment
- Whimsical terminal UI with ASCII art

## Usage

### Archive a command

```bash
docker run --rm -it -v $(pwd)/salvage:/salvage ghcr.io/polsala/nightly-void-salvage-bin:latest archive "echo 'Hello, Wasteland!'"
```

### Retrieve a command

```bash
docker run --rm -it -v $(pwd)/salvage:/salvage ghcr.io/polsala/nightly-void-salvage-bin:latest retrieve <artifact_id>
```

## Example

```bash
$ docker run --rm -it -v $(pwd)/salvage:/salvage ghcr.io/polsala/nightly-void-salvage-bin:latest archive "ls -la"
[+] Command archived with ID: abc123

$ docker run --rm -it -v $(pwd)/salvage:/salvage ghcr.io/polsala/nightly-void-salvage-bin:latest retrieve abc123
[+] Retrieved command: ls -la
```
