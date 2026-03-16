# Nightly Wasteland Barter Buddy

## A Fair Trade in the Fallout

This CLI utility, the `nightly-wasteland-barter-buddy`, helps survivors navigate the treacherous world of post-apocalyptic trade. Ever wondered if that rusty can of beans is worth two purified water rations or a handful of salvaged wires? This tool allows you to define resources, their base values, and adjust their scarcity and desirability factors to get a 'fair trade' estimate.

No more getting swindled by opportunistic scavengers! Make informed decisions and ensure your survival cache grows with every exchange.

## Installation

1.  **Ensure Node.js is installed:** If you don't have Node.js, download it from [nodejs.org](https://nodejs.org/).
2.  **Clone the repository:**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/node-utils/nightly-wasteland-barter-buddy
    ```
3.  **Install dependencies:**
    ```bash
    npm install
    ```

## Usage

Run the tool from the utility's directory:

```bash
node src/index.js <command> [options]
```

### Commands:

*   `list`: Lists all available resources and their current calculated values.
    ```bash
    node src/index.js list
    ```

*   `trade <haveResource> <haveAmount> <wantResource>`: Suggests a fair amount of `wantResource` for your `haveAmount` of `haveResource`.
    ```bash
    node src/index.js trade Water 5 'Canned Food'
    # Output: For 5 units of Water, you should expect approximately X units of Canned Food.
    ```

*   `add <name> <baseValue> <scarcity> <desirability>`: Adds a new resource or updates an existing one. Scarcity and desirability are factors (e.g., 0.1 for very scarce/undesirable, 2.0 for abundant/highly desirable).
    ```bash
    node src/index.js add 'Mutant Fungus' 1 0.1 0.5
    ```

*   `remove <name>`: Removes a resource.
    ```bash
    node src/index.js remove 'Mutant Fungus'
    ```

### Configuration

Resources are stored in `src/resources.json`. You can directly edit this file or use the `add` and `remove` commands. The `baseValue` is a nominal starting point. `scarcity` (lower = more scarce, higher = more abundant) and `desirability` (lower = less desired, higher = more desired) are multipliers that influence the final calculated value.

**Example `resources.json` entry:**

```json
{
  "name": "Water",
  "baseValue": 10,
  "scarcity": 0.8,  // Relatively abundant in some areas
  "desirability": 1.5 // Always highly desired
}
```

## Development & Testing

To run the tests:

```bash
npm test
```
