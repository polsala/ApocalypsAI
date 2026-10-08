# Nightly Mood Ring CLI

A whimsical command-line utility that helps you identify and reflect on your current emotional state. Just tell the Mood Ring how you're feeling, and it will reveal your inner aura with a color-coded mood and a corresponding whimsical insight.

## Features

*   **Interactive Prompt**: Easily describe your current feelings.
*   **Whimsical Mood Classification**: Translates your input into a unique, color-coded mood.
*   **Insightful Reflections**: Provides a short, whimsical message tailored to your mood.
*   **Type-Safe**: Built with TypeScript for robust and predictable behavior.

## Installation

1.  Navigate to the `typescript-utils/nightly-mood-ring-cli` directory.
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Build the TypeScript project:
    ```bash
    npm run build
    ```

## Usage

Run the utility from your terminal:

```bash
npm start
```

The utility will prompt you to describe how you're feeling. Type your response and press Enter.

### Example Interaction

```
$ npm start

✨ The Nightly Mood Ring hums softly... ✨
How are you feeling right now, wanderer of the digital wastes? (e.g., 'calm', 'stressed', 'happy')
> I feel quite peaceful and relaxed today.

Your aura glows with Serene Sapphire!
"The tranquil depths of the sapphire reflect the calm within your soul. Embrace this stillness, for it is a wellspring of strength."
```

## Development

To run tests:

```bash
npm test
```

To build the project:

```bash
npm run build
```

## Moods & Auras

The Mood Ring recognizes several core emotional states, each with its own unique aura and insight:

*   **Serene Sapphire**: Calm, peaceful, relaxed.
*   **Vibrant Verdant**: Energetic, happy, joyful, excited.
*   **Golden Glow**: Hopeful, optimistic, content.
*   **Amethyst Aura**: Thoughtful, introspective, curious.
*   **Crimson Ember**: Frustrated, angry, annoyed.
*   **Azure Abyss**: Sad, melancholic, tired.
*   **Obsidian Shadow**: Anxious, worried, stressed.
*   **Rainbow Shimmer**: Confused, mixed feelings, uncertain.
