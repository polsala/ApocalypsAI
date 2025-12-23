# Nightly Temporal Echo Triage

A type-safe CLI tool designed to help the community categorize those unsettling "temporal echoes" or "void whispers" and suggest whimsical, yet surprisingly effective, stabilization protocols or affirmations. Whether it's a strange feeling, a cryptic log message, or a sense of déjà vu, this tool offers a structured (and slightly absurd) approach to understanding and responding to the temporal anomalies of daily life.

## Features

*   **Echo Classification**: Analyzes input text to categorize temporal disturbances into predefined types like "Minor Glitch," "Chronal Ripple," "Void Whisper," or "Temporal Anomaly."
*   **Stabilization Protocols**: Provides a unique, whimsical protocol or affirmation tailored to each echo category.
*   **Type-Safe**: Built with TypeScript for robust and predictable echo handling.

## Installation

1.  Navigate to the utility directory:
    ```bash
    cd typescript-utils/nightly-temporal-echo-triage
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Build the TypeScript project:
    ```bash
    npm run build
    ```

## Usage

Run the triage tool from the command line, providing your temporal echo as an argument:

```bash
npm start -- "I'm experiencing a strange sense of déjà vu, like I've done this before."
```

Or, if you prefer to run the compiled JavaScript directly:

```bash
node dist/index.js --echo "The logs show an unusual discrepancy in the timestamps."
```

### Examples

*   **Minor Glitch**:
    ```bash
    npm start -- "Everything feels a bit laggy today."
    # Output:
    # Temporal Echo Detected: "Everything feels a bit laggy today."
    # Category: Minor Glitch
    # Stabilization Protocol: Recalibrate Chronometer: A brief moment of stillness can realign minor temporal discrepancies. Perhaps a cup of 'Temporal Tea'?
    ```

*   **Chronal Ripple**:
    ```bash
    npm start -- "I keep seeing the same number sequence everywhere, it's like an echo."
    # Output:
    # Temporal Echo Detected: "I keep seeing the same number sequence everywhere, it's like an echo."
    # Category: Chronal Ripple
    # Stabilization Protocol: Harmonize Resonance: Embrace the ripple. Sometimes, a gentle hum or a repetitive task can smooth out the temporal fabric. Try humming the 'Song of Infinite Loops'.
    ```

*   **Void Whisper**:
    ```bash
    npm start -- "There's an unsettling silence, an absence of expected noise."
    # Output:
    # Temporal Echo Detected: "There's an unsettling silence, an absence of expected noise."
    # Category: Void Whisper
    # Stabilization Protocol: Amplify Affirmation: Fill the void with positive resonance. 'I am present. I am whole. The void is merely a canvas for new beginnings.' Repeat thrice.
    ```

*   **Temporal Anomaly**:
    ```bash
    npm start -- "I just had a thought that felt like a paradox, completely out of sync."
    # Output:
    # Temporal Echo Detected: "I just had a thought that felt like a paradox, completely out of sync."
    # Category: Temporal Anomaly
    # Stabilization Protocol: Consult the Oracle of Now: This requires deeper introspection. Seek the wisdom of the present moment. 'What is truly happening, right here, right now?'
    ```

*   **Unknown Echo**:
    ```bash
    npm start -- "A peculiar sensation, hard to describe."
    # Output:
    # Temporal Echo Detected: "A peculiar sensation, hard to describe."
    # Category: Unknown Echo
    # Stabilization Protocol: Observe and Document: Not all echoes reveal their secrets immediately. Log this event for future analysis. 'The universe is full of surprises. I am ready to learn.'
    ```

## Development

To run tests:

```bash
npm test
```

To compile TypeScript:

```bash
npm run build
```
