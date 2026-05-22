# Nightly Void Thought Re-Roller

## Summary

The `nightly-void-thought-re-roller` is a whimsical CLI utility designed to help community members process and reframe their anxieties, worries, or mundane thoughts. By submitting a thought to the 'void', users receive a playfully re-rolled version, often with a more positive, neutral, or absurd perspective, accompanied by a 'cosmic whisper'. It's a digital stress ball for the mind, offering a moment of lighthearted detachment.

## Usage

1.  **Installation:**
    Navigate to the `node-utils/nightly-void-thought-re-roller` directory.
    ```bash
    npm install
    ```

2.  **Run the utility:**
    ```bash
    node src/index.js
    ```

3.  **Interact:**
    The utility will prompt you to enter a thought. Type your thought and press Enter.
    ```
    Enter your thought to cast into the void: I'm worried about the dwindling water supply.
    ```

4.  **Receive your re-rolled thought:**
    ```
    Casting your thought into the void...
    The void says: I'm considering about the dwindling water supply. A cosmic giggle echoes: all is well.
    ```

## Development

### Project Structure

```
.gitignore
package.json
README.md
src/
  index.js      # Main CLI application
  reRoller.js   # Core thought re-rolling logic
tests/
  reRoller.test.js # Tests for the re-rolling logic
```

### Running Tests

```bash
npm test
```

## How it Works

The `reRoller.js` module contains the core logic. It applies a series of string transformations:

1.  **Keyword Replacement:** Common negative or stressful words are replaced with more neutral, positive, or whimsical alternatives (e.g., "worried" becomes "considering", "problem" becomes "puzzle").
2.  **Void Whisper:** A random, comforting, or absurd phrase (a "void whisper") is appended to the re-rolled thought, adding a touch of cosmic perspective.

This process aims to gently shift the user's perception of their original thought.
