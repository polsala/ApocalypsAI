# Nightly Dev Fortune Cookie

Dispenses whimsical and insightful developer fortune cookie messages directly to your terminal.

## Overview

Ever feel like you need a little digital pick-me-up or a moment of coding wisdom? The `nightly-dev-fortune-cookie` utility is here to provide just that! It's a simple command-line tool that delivers a random, development-themed fortune, sometimes witty, sometimes profound, always a little bit fun.

## Installation

To use this utility, you need Node.js and npm (or yarn) installed on your system.

1.  **Navigate to the utility directory:**

    ```bash
    cd typescript-utils/nightly-dev-fortune-cookie
    ```

2.  **Install dependencies and build:**

    ```bash
    npm install
    npm run build
    ```

3.  **Link the utility for global access (optional, but recommended for CLI use):**

    ```bash
    npm link
    ```

    Now you can run `nightly-dev-fortune-cookie` from any directory.

## Usage

Simply run the command to get a random fortune:

```bash
nightly-dev-fortune-cookie
```

### With Category

You can also request a fortune from a specific category using the `--category` flag:

```bash
nightly-dev-fortune-cookie --category debugging
```

**Available Categories:**

*   `wisdom`
*   `debugging`
*   `deployment`
*   `general`

### Examples

```bash
# Get a general developer fortune
nightly-dev-fortune-cookie

# Get a fortune related to coding wisdom
nightly-dev-fortune-cookie --category wisdom

# Get a fortune about debugging woes
nightly-dev-fortune-cookie --category debugging

# Get a fortune about deployment adventures
nightly-dev-fortune-cookie --category deployment
```

## Contributing Fortunes

Want to add your own developer wisdom or witty remarks? Contributions are welcome!

1.  Fork the repository.
2.  Edit `src/fortunes.ts` to add new `Fortune` objects to the `fortunes` array.
3.  Ensure your fortune has a `message` (string) and a valid `category` (`wisdom`, `debugging`, `deployment`, or `general`).
4.  Run `npm test` to ensure everything still works.
5.  Submit a pull request!
