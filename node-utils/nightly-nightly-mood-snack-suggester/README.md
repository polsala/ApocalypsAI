# Nightly Mood Snack Suggester

A whimsical command-line utility that suggests a post-apocalyptic snack based on your current mood. Because even after the end of the world, your feelings are valid, and your stomach deserves a themed treat!

## Features

*   **Mood-Based Suggestions**: Get a snack tailored to your emotional state (grumpy, energetic, contemplative, etc.).
*   **Whimsical Descriptions**: Each snack comes with a unique, post-apocalyptic backstory.
*   **Cross-Platform**: Built with Node.js, runs anywhere Node.js is supported.

## Installation

1.  **Ensure Node.js is installed**: If you don't have Node.js, download it from [nodejs.org](https://nodejs.org/).
2.  **Clone the repository (or download this utility)**:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/node-utils/nightly-mood-snack-suggester
    ```
3.  **Install dependencies**:
    ```bash
    npm install
    ```
4.  **Make the CLI tool executable (optional, but recommended for global use)**:
    ```bash
    npm link
    ```
    This will create a `mood-snack` command available in your terminal.

## Usage

Run the `mood-snack` command followed by your mood:

```bash
mood-snack <your-mood>
```

### Examples

*   **Feeling grumpy?**
    ```bash
    mood-snack grumpy
    ```
    Output:
    ```
    Mood: grumpy
    Suggested Snack: Irradiated Twinkie
    Description: A classic for a reason. Its eternal shelf-life mirrors your eternal grumpiness. Best served with a side of existential dread.
    ```

*   **Need some energy?**
    ```bash
    mood-snack energetic
    ```
    Output:
    ```
    Mood: energetic
    Suggested Snack: Mutant Berry Blend
    Description: Harvested from the glowing wilds, these berries provide a questionable but potent burst of energy. May cause temporary bioluminescence.
    ```

*   **Lost in thought?**
    ```bash
    mood-snack contemplative
    ```
    Output:
    ```
    Mood: contemplative
    Suggested Snack: Dusty Can of Beans (vintage 2042)
    Description: Perfect for quiet reflection by the flickering barrel fire. Each bean a tiny universe of thought. Best consumed slowly, one bean at a time.
    ```

*   **What if your mood isn't recognized?**
    ```bash
    mood-snack confused
    ```
    Output:
    ```
    Mood: confused
    Suggested Snack: Dehydrated Nutrient Paste
    Description: When your mood is beyond classification, or simply 'meh', this universal sustenance will do. It's... food.
    ```

*   **For help and available options:**
    ```bash
    mood-snack --help
    ```

## Development

### Running Tests

To run the automated tests, navigate to the utility's directory and execute:

```bash
npm test
```

Tests are deterministic and offline, using mocks for `console.log` and `process.exit` to ensure consistent output capture and prevent side effects during testing.
