# Nightly Wasteland Mood Ring

A whimsical Node.js CLI utility that helps you tune into the 'mood' of the post-apocalyptic wasteland and receive a corresponding survival suggestion.

Ever wonder if the desolate winds are whispering 'adventure' or 'introspection'? This tool will tell you!

## Features

*   **Mood Classification**: Input a word or phrase, and the utility will attempt to classify the wasteland's mood.
*   **Random Moods**: No input? No problem! Get a completely random mood and suggestion.
*   **Whimsical Suggestions**: Each mood comes with a unique, thematic survival tip.

## Installation

1.  Ensure you have Node.js (v14 or higher) installed.
2.  Navigate to the `node-utils/nightly-wasteland-mood-ring` directory.
3.  No `npm install` is needed as it uses only built-in Node.js modules.

## Usage

Run the utility from your terminal:

### With Input (for a specific mood)

Provide a word or short phrase that describes what you're feeling or observing in the wasteland:

```bash
node src/index.js "dark clouds on the horizon"
```

```bash
node src/index.js "feeling energetic today"
```

### Without Input (for a random mood)

If you don't provide any arguments, the utility will prompt you for input. Press `Enter` without typing anything to get a completely random wasteland mood:

```bash
node src/index.js
```

```
What's the wasteland whispering to you today? (Press Enter for a random mood)
```

### Example Output

```
--- The Wasteland's Mood Ring ---
Mood: Gloomy
Description: The air hangs heavy, like forgotten memories. A time for introspection.
Suggestion: Seek shelter in the ruins of old libraries. Perhaps a forgotten tome holds a clue, or at least a dry place to nap.
---------------------------------
```

```
--- The Wasteland's Mood Ring ---
Mood: Energetic
Description: A restless wind whips through the dust, urging action and exploration.
Suggestion: Today is for scavenging! Head towards the shimmering mirage on the horizon. It might be water, or just a very shiny rock.
---------------------------------
```

## Development

To run the tests:

```bash
node tests/index.test.js
```
