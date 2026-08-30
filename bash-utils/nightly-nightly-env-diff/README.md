# nightly-env-diff

**nightly-env-diff** is a tiny Bash utility that compares two ```.env``` files and prints a friendly, emoji‑rich report of what changed.

## Features

- Detects **added**, **removed**, and **changed** environment variables.
- Ignores comments (`# …`) and blank lines.
- Outputs a whimsical, colour‑free report that can be piped or logged.
- Zero external dependencies – just Bash (>=4).

## Installation

```bash
# Clone the repository (or copy the utility into your project)
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/utils/nightly-env-diff
# Make the script executable
chmod +x src/diff_env.sh
```

You can also symlink it into a directory on your ``$PATH`` for global use.

## Usage

```bash
./src/diff_env.sh <old.env> <new.env>
```

### Example

```bash
cat >old.env <<EOF
# Old environment
VAR1=foo
VAR2=bar
EOF

cat >new.env <<EOF
# New environment
VAR2=baz
VAR3=qux
EOF

./src/diff_env.sh old.env new.env
```

**Output**

```
🚀 Added variables:
  + VAR3=qux
🗑️ Removed variables:
  - VAR1=foo
🔄 Changed variables:
  * VAR2: "bar" → "baz"
```

If there are no differences, you will see:

```
✅ No differences detected. Your env is in perfect harmony.
```

## Testing

Run the bundled test suite with Bash:

```bash
cd tests
bash test_diff_env.sh
```

The test creates temporary ```.env``` files, invokes the script, and asserts the exact output.

## License

This utility is released under the MIT License – see the root `LICENSE` file.
