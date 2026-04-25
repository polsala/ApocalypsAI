import os
import sys
import subprocess
from pathlib import Path

def _write_index_html(emojis: list[str], dest: Path) -> None:
    """Write a minimal HTML page that displays the given emojis."""
    html_content = """<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <title>Emoji Archive</title>
    <style>
        body {font-family: sans-serif; text-align: center; margin-top: 2rem;}
        .emoji {font-size: 4rem; margin: 0.5rem;}
    </style>
</head>
<body>
    <h1>My Emoji Archive</h1>
    <div class=\"emoji\">{emoji_line}</div>
</body>
</html>
""".format(emoji_line=" ".join(emojis))
    (dest / "index.html").write_text(html_content, encoding="utf-8")

def _write_dockerfile(dest: Path) -> None:
    """Write a Dockerfile that serves the generated index.html via nginx."""
    dockerfile = """FROM nginx:alpine
COPY index.html /usr/share/nginx/html/index.html
"""
    (dest / "Dockerfile").write_text(dockerfile, encoding="utf-8")

def _build_image(build_dir: Path, tag: str) -> None:
    """Invoke `docker build` to create the image.
    This function is deliberately thin so it can be mocked in tests.
    """
    subprocess.run(["docker", "build", "-t", tag, "."], cwd=str(build_dir), check=True)

def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        print("Usage: python generate.py [EMOJI ...] <image-tag>")
        return 1
    # The last argument is the image tag; everything before are emojis
    *emoji_args, tag = argv
    emojis = emoji_args if emoji_args else ["😀", "🚀", "🌟", "🐍", "🤖"]
    script_dir = Path(__file__).resolve().parent
    build_dir = script_dir / "build"
    # Clean previous build if exists
    if build_dir.exists():
        for child in build_dir.iterdir():
            child.unlink()
    else:
        build_dir.mkdir()
    _write_index_html(emojis, build_dir)
    _write_dockerfile(build_dir)
    print(f"Building Docker image '{tag}' with emojis: {' '.join(emojis)}")
    _build_image(build_dir, tag)
    print(f"Docker image '{tag}' built successfully.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
