# nightly-docker-emoji-archiver

**Purpose**: Generate a tiny Docker image (based on `nginx:alpine`) that serves a static HTML page showcasing a user‑provided list of emojis.

## How it works
1. `generate.py` receives a list of emojis (or uses a default set).
2. It creates a temporary `build/` directory containing:
   * `index.html` – a simple page that renders the emojis.
   * `Dockerfile` – copies `index.html` into the default Nginx web root.
3. The script invokes `docker build -t <tag> .` inside `build/`.
4. Run the image with `docker run -p 8080:80 <tag>` and visit `http://localhost:8080` to see the emojis.

## Prerequisites
- Docker Engine installed and the current user has permission to run Docker commands.
- Python 3.11 (standard library only).

## Usage
```bash
# Clone the repository (or copy the utility folder) and cd into it
cd nightly-docker-emoji-archiver

# Run the generator with custom emojis and a tag name
python src/generate.py 😀 🚀 🌟 my-emoji-image

# The script will build the image. Start it:
docker run -d -p 8080:80 my-emoji-image
```

If you omit emojis, a default set will be used.

## Testing
The utility includes a deterministic unit test that mocks Docker calls, ensuring the build artefacts are correctly generated without requiring a real Docker daemon.

```bash
python -m unittest discover -s tests
```

## License
MIT – see the root `LICENSE` file.
