# Nightly Mood Ring CLI

A whimsical command-line utility that analyzes text input to determine its "mood" and displays a corresponding cosmic color and description. Ever wondered if your commit message is radiating joy or reflecting a touch of cosmic gloom? The Nightly Mood Ring CLI is here to give you a quick, lighthearted vibe check!

## Features

*   **Text Mood Analysis**: Simple keyword-based sentiment analysis to categorize text as positive, negative, neutral, or mixed.
*   **Whimsical Output**: Each mood is associated with a unique "cosmic gem" color and a playful description.
*   **CLI Integration**: Easily use it with direct arguments.

## Installation

1.  Navigate to the `node-utils/nightly-mood-ring-cli` directory.
2.  Install dependencies (this utility is self-contained and has no external npm dependencies):
    ```bash
    npm install
    ```
3.  Make the utility executable:
    ```bash
    chmod +x src/index.js
    ```
    For easier global access, you can use `npm link` after running `npm install` in the utility's root:
    ```bash
    npm link
    ```
    This will create a symlink in your global `node_modules` bin directory, allowing you to run `nightly-mood-ring` from anywhere.

## Usage

Run the `nightly-mood-ring` command followed by the text you want to analyze:

```bash
nightly-mood-ring "I am so happy with this new feature, it's wonderful!"
# Expected Output:
# Color: Rose Quartz
# Description: Radiant with optimism, a beacon of hope!
```

For negative sentiments:

```bash
nightly-mood-ring "This bug is a terrible problem, I feel sad about it."
# Expected Output:
# Color: Obsidian Black
# Description: Reflecting deep contemplation, perhaps a touch of cosmic gloom.
```

For neutral or ambiguous text:

```bash
nightly-mood-ring "The server is running at 80% capacity."
# Expected Output:
# Color: Moonstone Grey
# Description: Calm and collected, observing the cosmic dance with serene detachment.
```

For text with mixed positive and negative keywords:

```bash
nightly-mood-ring "I love the concept, but the implementation has difficult problems."
# Expected Output:
# Color: Amethyst Purple
# Description: A swirl of emotions, a truly complex cosmic tapestry.
```

If no text is provided, the utility will display usage instructions and exit:

```bash
nightly-mood-ring
# Expected Output:
# Usage: nightly-mood-ring <text> or echo "text" | nightly-mood-ring
```
