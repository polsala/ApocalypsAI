# Nightly Echo-Text Distorter

## Overview

The `nightly-echo-text-distorter` is a whimsical utility designed to simulate the transmission of text through a noisy, temporal void. It applies various distortions like character omission, duplication, word echoing, and the insertion of 'void static' to your input text, making it sound like a message barely making it through the cosmic ether.

This tool is perfect for adding a touch of apocalyptic flavor to your messages, generating creative writing prompts, or simply having fun with text manipulation.

## Features

*   **Character Omission**: Randomly removes characters.
*   **Character Duplication**: Randomly duplicates characters.
*   **Word Echo**: Repeats parts of words to simulate an echo.
*   **Void Static Insertion**: Inserts atmospheric, meaningless fragments into the text.
*   **Configurable**: Adjust distortion chances and static content to fine-tune the 'void' effect.

## Installation

To use this utility, you'll need Node.js and npm (or yarn) installed.

1.  Navigate to the `typescript-utils/nightly-echo-text-distorter` directory.
2.  Install dependencies:
    ```bash
    npm install
    # or
    yarn install
    ```

## Usage

### Command Line Interface (CLI)

Run the utility directly and type your text. Press `Ctrl+D` (Unix/Linux/macOS) or `Ctrl+Z` then `Enter` (Windows) to signal end-of-input.

```bash
npm start
# or
yarn start
```

**Example:**

```
$ npm start
ApocalypsAI Nightly Echo-Text Distorter
Enter text to send through the void (Ctrl+D or Ctrl+C to finish):
Hello, brave survivor. The signal is weak, but hope remains.
<Ctrl+D>

--- Transmitted through the void ---
Helllo, brave...bra survivo. The signal is weak, but hope...hop remains.
------------------------------------
```

### Programmatic Usage (as a module)

You can also import and use the `distortText` function in your own TypeScript/JavaScript projects.

```typescript
import { distortText } from './src/index';

const originalMessage = "Seek shelter immediately. The storm approaches.";

// Using default distortion options
const distortedDefault = distortText(originalMessage);
console.log("Default Distortion:", distortedDefault);

// Using custom distortion options
const customOptions = {
  charOmissionChance: 0.05,
  charDuplicationChance: 0.03,
  wordEchoChance: 0.1,
  staticInsertionChance: 0.08,
  staticContent: ['[...flicker...]', '[...lost data...]', '[...static burst...]'],
  minEchoLength: 4,
};
const distortedCustom = distortText(originalMessage, customOptions);
console.log("Custom Distortion:", distortedCustom);
```

## Development

### Build

To compile the TypeScript code to JavaScript:

```bash
npm run build
# or
yarn build
```

### Tests

To run the automated tests:

```bash
npm test
# or
yarn test
```
