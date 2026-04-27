# nightly-emoji-enhancer

**What it does**

`nightly-emoji-enhancer` reads a line of text (either from STDIN or as a command‑line argument) and prepends an emoji that matches the message’s intent.  It’s a tiny, fun way to make commit messages, chat snippets, or any short string a little more expressive.

**Supported keywords & emojis**

| Keyword (case‑insensitive) | Emoji |
|----------------------------|-------|
| `fix` / `bug`              | 🛠️   |
| `add` / `new` / `create`   | ➕   |
| `remove` / `delete` / `rm` | ➖   |
| `update` / `upgrade` / `change` | 🔄 |
| any other text             | 🎉   |

**Installation**

```bash
# Clone the repository (or copy the script into your PATH)
git clone https://github.com/polsala/ApocalypsAI.git
cp utils/bash-utils/nightly-emoji-enhancer/src/emoji_enhance.sh /usr/local/bin/emoji-enhance
chmod +x /usr/local/bin/emoji-enhance
```

**Usage**

```bash
# Pass the text as an argument
emoji-enhance "Add new feature to parser"
# Output: ➕ Add new feature to parser

# Pipe from another command or STDIN
git commit -m "$(git diff --cached --quiet || echo 'Fix typo in README')" | emoji-enhance
```

**Running the tests**

```bash
cd utils/bash-utils/nightly-emoji-enhancer
bash tests/test_emoji_enhance.sh
```

All tests should pass with a zero exit code.
