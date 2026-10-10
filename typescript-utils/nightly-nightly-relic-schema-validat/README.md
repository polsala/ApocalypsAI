# Nightly Relic Schema Validator

A type-safe CLI tool for validating scavenged data files against predefined 'relic' schemas. In the chaotic post-apocalyptic data landscape, ensuring the structural integrity of your precious findings is paramount. This utility helps you verify that your JSON data conforms to expected patterns, preventing data corruption and misinterpretation.

## Features

*   **Type-Safe Validation**: Leverage TypeScript interfaces to define clear data structures.
*   **CLI Interface**: Easily validate files from your terminal.
*   **Extensible Schemas**: Define your own 'relic' schemas to fit various data types.
*   **Clear Error Reporting**: Get detailed feedback on what went wrong during validation.

## Installation

1.  **Prerequisites**: Ensure you have Node.js (v14 or higher) and npm installed.
2.  **Clone the repository (or navigate to the utility's directory)**:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/typescript-utils/nightly-relic-schema-validat
    ```
3.  **Install dependencies**:
    ```bash
    npm install
    ```
4.  **Build the utility**:
    ```bash
    npm run build
    ```
5.  **Link the CLI tool (optional, for global access)**:
    ```bash
    npm link
    # Now 'relic-validate' command is available globally
    ```

## Usage

To validate a data file, run the `relic-validate` command followed by the schema name and the path to your JSON data file.

```bash
relic-validate <schema-name> <data-file-path>
```

### Example Schemas

This utility comes with a few built-in relic schemas:

*   `ScavengedLog`: For validating log entries from ancient systems.
*   `ResourceManifest`: For verifying inventories of scavenged resources.

### Examples

1.  **Validate a `ScavengedLog` file**:

    `data/log_entry.json`:
    ```json
    {
      "timestamp": "2077-10-23T14:30:00Z",
      "level": "INFO",
      "message": "Found a shiny new bolt.",
      "source": "Sector 7G"
    }
    ```

    ```bash
    relic-validate ScavengedLog data/log_entry.json
    ```
    Expected output:
    ```
    ✅ Data in 'data/log_entry.json' successfully validated against schema 'ScavengedLog'.
    ```

2.  **Validate a `ResourceManifest` file**:

    `data/resource_cache.json`:
    ```json
    {
      "resourceId": "scrap-metal-001",
      "quantity": 15,
      "location": {
        "sector": "Alpha",
        "grid": "A1"
      },
      "scavengerNotes": ["rusty", "heavy"]
    }
    ```

    ```bash
    relic-validate ResourceManifest data/resource_cache.json
    ```
    Expected output:
    ```
    ✅ Data in 'data/resource_cache.json' successfully validated against schema 'ResourceManifest'.
    ```

3.  **Validation Failure (missing field)**:

    `data/bad_log.json`:
    ```json
    {
      "timestamp": "2077-10-23T14:30:00Z",
      "level": "ERROR"
      // 'message' is missing
    }
    ```

    ```bash
    relic-validate ScavengedLog data/bad_log.json
    ```
    Expected output:
    ```
    ❌ Data in 'data/bad_log.json' failed validation against schema 'ScavengedLog':
      - Missing required property: message
    ```

## Development

### Running Tests

```bash
npm test
```

### Adding New Schemas

YouYou can extend the `src/schemas.ts` file with new TypeScript interfaces and add them to the `RELIC_SCHEMAS` object to define new validation rules.
