# Nightly Resource Manifest Validator

A type-safe CLI tool to validate post-apocalyptic resource manifests against a predefined schema, ensuring inventory consistency for the coming night.

## 📜 Overview

In the desolate future, meticulous resource tracking is paramount for survival. The `Nightly Resource Manifest Validator` ensures that your scavenged inventory manifests adhere to a strict, type-safe schema. This prevents errors, miscounts, and ensures that your community's vital supplies are accurately recorded and ready for deployment or consumption.

It's built with TypeScript, leveraging its strong typing capabilities to define and enforce the structure of your resource data at runtime.

## ✨ Features

*   **Type-Safe Validation**: Enforces a strict schema for `Manifest` and `Resource` objects.
*   **Detailed Error Reporting**: Pinpoints exactly where validation fails, with descriptive messages.
*   **ISO 8601 Date Checks**: Validates `timestamp` and `expiryDate` fields for correct format.
*   **Perishability Logic**: Ensures `expiryDate` is present for perishable items.
*   **CLI Interface**: Easy to integrate into your nightly automation scripts.

## 🚀 Installation

1.  **Clone the repository (or navigate to the utility folder):**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/typescript-utils/nightly-resource-manifest-validator
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    # or
    yarn install
    ```

## 🛠️ Usage

To validate a manifest file, run the utility with the path to your JSON manifest:

```bash
npm start <path-to-your-manifest.json>
# or
yarn start <path-to-your-manifest.json>
```

### Example: Valid Manifest

Create a file named `my-base-manifest.json`:

```json
{
  "manifestName": "Alpha Base Supplies",
  "timestamp": "2024-07-20T10:00:00Z",
  "location": "Sector 7G",
  "resources": [
    {
      "name": "Water Bottle",
      "quantity": 15,
      "unit": "bottles",
      "perishable": true,
      "expiryDate": "2025-01-01T00:00:00Z"
    },
    {
      "name": "Canned Beans",
      "quantity": 30,
      "unit": "cans",
      "perishable": false
    },
    {
      "name": "Ammo (9mm)",
      "quantity": 200,
      "unit": "rounds",
      "perishable": false
    }
  ]
}
```

Then run the validator:

```bash
npm start my-base-manifest.json
```

**Expected Output:**

```
[32m[1m✅ Manifest "Alpha Base Supplies" at "Sector 7G" is VALID.[22m[39m
   Contains 3 unique resource types.
```

### Example: Invalid Manifest (Missing `location`)

Create a file named `invalid-manifest.json`:

```json
{
  "manifestName": "Beta Outpost Cache",
  "timestamp": "2024-07-20T11:30:00Z",
  "resources": [
    {
      "name": "Medical Kit",
      "quantity": 2,
      "unit": "kits",
      "perishable": false
    }
  ]
}
```

Then run the validator:

```bash
npm start invalid-manifest.json
```

**Expected Output:**

```
[31m[1mValidation Error: Manifest "location" must be a non-empty string.[22m[39m
[31m[1m❌ Manifest validation FAILED for file: invalid-manifest.json[22m[39m
```

### Example: Invalid Resource (Perishable without `expiryDate`)

Create a file named `perishable-error.json`:

```json
{
  "manifestName": "Gamma Bunker Stock",
  "timestamp": "2024-07-20T12:00:00Z",
  "location": "Underground Level 3",
  "resources": [
    {
      "name": "Fresh Rations",
      "quantity": 5,
      "unit": "packs",
      "perishable": true
      // Missing "expiryDate"
    }
  ]
}
```

Then run the validator:

```bash
npm start perishable-error.json
```

**Expected Output:**

```
[31m[1mValidation Error: Resource "Fresh Rations" is perishable but "expiryDate" is missing or not a string.[22m[39m
[31m[1mValidation Error: Invalid resource found at index 0 in manifest "Gamma Bunker Stock".[22m[39m
[31m[1m❌ Manifest validation FAILED for file: perishable-error.json[22m[39m
```

## 🧪 Running Tests

To ensure the validator is functioning correctly, run the provided tests:

```bash
npm test
# or
yarn test
```

## 🤝 Contributing

Feel free to suggest improvements or new validation rules!
