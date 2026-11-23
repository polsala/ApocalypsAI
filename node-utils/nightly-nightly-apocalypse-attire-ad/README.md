# Nightly Apocalypse Attire Advisor

A whimsical utility to help you choose the perfect outfit for any post-apocalyptic scenario, whether you're scavenging through irradiated ruins or attending a formal bunker gathering. This tool provides sartorial guidance based on the prevailing "apocalyptic weather" and your "mood" or "occasion."

## Features

*   **Apocalyptic Attire Suggestions:** Get tailored clothing recommendations for various grim conditions.
*   **Whimsical Categories:** Navigate through "Irradiated Haze," "Acid Rain," "Mutant Downpour," and moods like "Scavenging," "Bunker Formal," or "Raid Prep."
*   **Random Suggestions:** Can't decide? Let the advisor pick a random weather and mood for you.
*   **List Options:** See all available weather conditions and moods.
*   **Cross-platform CLI:** Runs anywhere Node.js is installed.

## Installation

1.  **Navigate to the utility directory:**
    ```bash
    cd node-utils/nightly-apocalypse-attire-advisor
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    ```

## Usage

Run the utility from the command line:

```bash
node src/index.js [weather] [mood]
```

### Examples:

*   **Get a specific attire suggestion:**
    ```bash
    node src/index.js "Acid Rain" "Scavenging"
    # Output: For "Acid Rain" and "Scavenging", you should wear:
    # "Acid-proof slicker, full-face visor, rubber boots, acid-neutralizing spray."
    ```

*   **Get a random attire suggestion:**
    ```bash
    node src/index.js --random
    # Output: Randomly selected: Weather "Irradiated Haze", Mood "Bunker Formal"
    # For "Irradiated Haze" and "Bunker Formal", you should wear:
    # "Cleaned hazmat suit, polished respirator, emergency rations pouch."
    ```

*   **Get a suggestion for a specific weather, with a random mood:**
    ```bash
    node src/index.js "Dust Storm"
    # Output: No mood provided. Choosing a random one.
    # For "Dust Storm" and "Trading Post Visit", you should wear:
    # "Loose-fitting robes, wide-brimmed hat, dust-proof bag."
    ```

*   **List all available weather conditions and moods:**
    ```bash
    node src/index.js --list
    # Output:
    # Available Weather Conditions:
    # - Irradiated Haze
    # - Acid Rain
    # - Dust Storm
    # - Mutant Downpour
    # - Clear but Cold Void
    #
    # Available Moods/Occasions:
    # - Scavenging
    # - Bunker Formal
    # - Raid Prep
    # - Trading Post Visit
    # - Stargazing (if visible)
    ```

*   **Show help message:**
    ```bash
    node src/index.js --help
    ```

## Development

### Running Tests

To ensure everything is functioning correctly, run the provided test suite:

```bash
npm test
```

This will execute all tests using Jest.
