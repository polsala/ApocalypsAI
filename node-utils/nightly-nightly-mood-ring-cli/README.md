# Nightly Mood Ring CLI

A whimsical command-line utility that interprets your current sentiment based on a short phrase and displays it as a "mood ring" color and description. Ever wonder what color your digital aura is? Now you can find out!

## Installation

1.  Ensure you have Node.js installed (v14 or higher recommended).
2.  Clone the repository or navigate to the `nightly-mood-ring-cli` directory.
3.  Install dependencies:
    ```bash
    npm install
    ```

## Usage

Run the utility from your terminal:

```bash
node src/index.js
```

You will be prompted to enter a phrase describing your current feeling or situation. The utility will then analyze your input and display a mood color and description.

### Examples

```
$ node src/index.js
✨ Nightly Mood Ring ✨
Enter a phrase describing your current feeling: I feel so happy today!
Your mood is: Radiant Ruby (Happy and energetic!)
```

```
$ node src/index.js
✨ Nightly Mood Ring ✨
Enter a phrase describing your current feeling: Feeling a bit down and blue.
Your mood is: Melancholy Sapphire (Feeling a bit sad or reflective.)
```

```
$ node src/index.js
✨ Nightly Mood Ring ✨
Enter a phrase describing your current feeling: Just chilling, nothing special.
Your mood is: Shifting Quartz (Neutral, adaptable, or uncertain.)
```

## How it Works

The utility uses a simple keyword-matching algorithm to detect sentiment. It looks for specific words in your input phrase and maps them to predefined mood colors and descriptions. If no specific keywords are found, it defaults to a "Shifting Quartz" mood.

## Development

To run tests:

```bash
npm test
```
