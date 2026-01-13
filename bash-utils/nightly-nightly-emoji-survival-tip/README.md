# nightly-emoji-survival-tip

A whimsical Bash utility that delivers a random survival tip with an emoji.  Use the \`--seed\` option for deterministic output, useful for testing or reproducible logs.

## Usage

\`\`\`bash
./src/main.sh [--seed <int>] [-l]
\`\`\`

- \`--seed <int>\`: Provide a seed for deterministic tip selection.
- \`-l\`: List all available tips.

## Example

\`\`\`bash
$ ./src/main.sh --seed 42
🌟 Tip: Learn basic first-aid skills. 🩹
\`\`\`

## License

MIT
