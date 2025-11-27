# Nightly Emoji Annotator

A tiny utility that reads text line‑by‑line (from **stdin** or a file) and prefixes each line with a random emoji from a curated list. Perfect for adding a splash of personality to logs, commit messages, or any stream of text.

## Features

* **Zero external dependencies** – pure Python 3.11 standard library.
* Deterministic behavior in tests via mocking `random.choice`.
* Can be used as a pipe:

```sh
cat mylog.txt | python -m nightly_emoji_annotator
```

* Or as a module:

```python
from nightly_emoji_annotator import annotate_line
print(annotate_line("Hello world"))
```

## Installation

Copy the `utils/nightly-emoji-annotator` folder into your project or add it to your `PYTHONPATH`.

## Usage

```sh
python -m nightly_emoji_annotator < input.txt
```

or

```sh
python -m nightly_emoji_annotator input.txt
```

If a filename is supplied, the file is read; otherwise, stdin is used.

## License

MIT – see the root LICENSE file.
