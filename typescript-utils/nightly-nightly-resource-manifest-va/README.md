# Nightly Resource Manifest Validator (NRMV)

In the chaotic aftermath, maintaining a coherent inventory of vital resources is paramount. The `Nightly Resource Manifest Validator` (`nrmv`) is a type-safe CLI utility designed to bring order to your post-apocalyptic stockpiles. Define strict schemas for your resources, including allowed units, quantity ranges, and descriptions, then validate your manifests to ensure no 'inventory paradoxes' or critical miscounts jeopardize your survival.

## Features

*   **Type-Safe Schema Definition**: Define your resources with explicit types, units, and constraints using TypeScript interfaces.
*   **Manifest Validation**: Check your resource manifests against a predefined schema to catch errors like unknown resources, incorrect units, or quantities outside allowed ranges.
*   **CLI Interface**: Easily validate manifest files from your command line.
*   **Whimsical yet Practical**: Ensures your 'irradiated beans' are always counted in 'cans' and never 'gallons'.

## Installation

To use `nrmv` globally, you'll need Node.js and npm installed.

```bash
npm install -g nightly-resource-manifest-val
```

Alternatively, you can use `npx` to run it without global installation:

```bash
npx nightly-resource-manifest-val validate <schema-file.json> <manifest-file.json>
```

## Usage

First, create your resource schema file (e.g., `schema.json`) and your resource manifest file (e.g., `manifest.json`).

### 1. Define Your Schema (`schema.json`)

This JSON file describes the types of resources you track, their allowed units, and optional quantity constraints.

```json
{
  "version": "1.0",
  "name": "ApocalypticEssentials",
  "description": "Schema for critical survival resources in a post-collapse world.",
  "resources": [
    {
      "name": "Water",
      "description": "Potable water, purified or collected.",
      "units": ["liter", "ml"],
      "minQuantity": 0.5,
      "maxQuantity": 100,
      "tags": ["hydration", "essential"]
    },
    {
      "name": "Canned Food",
      "description": "Non-perishable canned goods.",
      "units": ["can", "box"],
      "minQuantity": 1,
      "maxQuantity": 50,
      "tags": ["sustenance", "food"]
    },
    {
      "name": "First Aid Kit",
      "description": "Basic medical supplies.",
      "units": ["piece"],
      "minQuantity": 0,
      "maxQuantity": 5,
      "tags": ["medical", "essential"]
    },
    {
      "name": "Barbed Wire",
      "description": "For perimeter defense.",
      "units": ["meter", "foot"],
      "minQuantity": 10,
      "maxQuantity": 500,
      "tags": ["defense", "construction"]
    },
    {
      "name": "Irradiated Beans",
      "description": "A staple, if you don't mind the glow.",
      "units": ["can"],
      "minQuantity": 1,
      "maxQuantity": 100,
      "tags": ["food", "radioactive"]
    }
  ]
}
```

### 2. Create Your Manifest (`manifest.json`)

This JSON file represents your actual inventory at a specific location and time.

```json
{
  "manifestId": "shelter-alpha-storage-001",
  "location": "Underground Bunker A-7",
  "timestamp": "2077-10-23T13:37:00Z",
  "items": [
    {
      "resourceName": "Water",
      "quantity": 15,
      "unit": "liter"
    },
    {
      "resourceName": "Canned Food",
      "quantity": 30,
      "unit": "can"
    },
    {
      "resourceName": "First Aid Kit",
      "quantity": 1,
      "unit": "piece"
    },
    {
      "resourceName": "Barbed Wire",
      "quantity": 150,
      "unit": "meter"
    },
    {
      "resourceName": "Irradiated Beans",
      "quantity": 5,
      "unit": "can"
    }
  ]
}
```

### 3. Validate Your Manifest

Run the validator from your terminal:

```bash
nrmv validate schema.json manifest.json
```

**Example of a successful validation:**

```
✅ Manifest "shelter-alpha-storage-001" at "Underground Bunker A-7" is valid according to schema "ApocalypticEssentials".
```

**Example of a failed validation:**

If `manifest.json` had an item like `{"resourceName": "Water", "quantity": 5, "unit": "gallon"}`, the output would be:

```
❌ Manifest "shelter-alpha-storage-001" at "Underground Bunker A-7" is INVALID.
  - Item 1 ("Water"): Unit "gallon" is not allowed for resource "Water" by the schema. Allowed units: liter, ml.
```

## Development

1.  Clone the repository.
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Build the TypeScript code:
    ```bash
    npm run build
    ```
4.  Run tests:
    ```bash
    npm test
    ```
5.  To test the CLI locally without global install:
    ```bash
    npm run start -- validate schema.json manifest.json
    ```

## License

MIT
