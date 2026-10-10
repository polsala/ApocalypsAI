# Nightly Emoji Commit Replacer

A whimsical Bash utility that scans the most recent Git commit messages in a repository and replaces configured keywords with emojis. Great for adding a splash of fun to your commit logs without altering the actual history.

## Features
- Configurable keyword‑to‑emoji mapping (built‑in defaults or custom file)
- Choose how many recent commits to process
- Operates on any Git repository (specify path)
- Pure Bash, no external dependencies beyond Git

## Installation
```sh
# Clone the utility (or copy the files) into your project
mkdir -p utils/nightly-emoji-commit-replacer && cd utils/nightly-emoji-commit-replacer
# Place the files as provided in the repository structure
```
Make the script executable:
```sh
chmod +x src/main.sh
```

## Usage
```sh
./src/main.sh [-n NUM] [-m MAP_FILE] [-d REPO_PATH]
```
- `-n NUM` – Number of recent commits to process (default: 5)
- `-m MAP_FILE` – Path to a custom mapping file (default: built‑in mapping)
- `-d REPO_PATH` – Path to the Git repository (default: current directory)

### Mapping File Format
Each line defines a mapping in the form `keyword=emoji`:
```
fix=🔧
bug=🐞
feature=✨
```
Lines starting with `#` or empty lines are ignored.

## Example
```sh
# Create a simple mapping file
cat > mymap.txt <<EOF
fix=🔧
feature=✨
bug=🐞
EOF

# Run the replacer on the last 3 commits of the current repo
./src/main.sh -n 3 -m mymap.txt
```
The output will show the commit messages with the specified words replaced by their emojis.

## Testing
Run the provided test suite with:
```sh
bash tests/test_main.sh
```
The tests create a temporary Git repository, make a few commits, and verify that the script correctly substitutes the keywords.
