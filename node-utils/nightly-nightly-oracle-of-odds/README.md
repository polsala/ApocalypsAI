# Nightly Oracle of Odds

A whimsical CLI tool designed to assist indecisive survivors in the wasteland by providing a 'prophecy' – a randomly selected option from a given list. When the choices are many and the path is unclear, let the Oracle guide your way with a touch of post-apocalyptic wisdom.

## Installation

1.  Navigate to the `node-utils/nightly-oracle-of-odds` directory.
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Make the script executable (optional, but good practice for CLI tools):
    ```bash
    chmod +x src/index.js
    ```

## Usage

Run the utility from the command line, passing your options as arguments. Each argument will be treated as a separate choice.

```bash
node src/index.js "Scavenge Sector 7" "Repair the Water Purifier" "Trade with the Nomads"
```

### Example Output

```
$ node src/index.js "Eat the last can of beans" "Risk a raid for more" "Starve nobly"

[36m[1m
--- The Oracle of Odds has spoken ---
[22m[39m
[33mThe flickering neon sign of destiny blinks, settling on: [1mEat the last can of beans[22m. Follow its glow.
[36m[1m
-------------------------------------
[22m[39m
```

## Whimsy

The Oracle's pronouncements are imbued with the cryptic wisdom of the post-apocalypse, offering guidance that is both random and strangely profound. Each run offers a fresh perspective from the digital ether.
