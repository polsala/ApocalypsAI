# nightly-digital-hoard-harvester

A whimsical Node.js CLI tool to help you unearth and manage your "digital artifacts" – those old, large, or forgotten files lurking in your file system. Think of it as a friendly digital archaeologist, helping you sort through your byte-sized burdens and treasures!

## Features

-   **Scan Directories**: Recursively scans a specified directory for files.
-   **Age Filtering**: Identify files older than a specified number of days.
-   **Size Filtering**: Pinpoint files larger than a given size in megabytes.
-   **Whimsical Output**: Presents findings with a touch of digital charm.

## Installation

1.  **Prerequisites**: Ensure you have Node.js (v14 or higher) installed.
2.  **Clone the repository**:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/node-utils/nightly-digital-hoard-harvester
    ```
3.  **Install dependencies**:
    ```bash
    npm install
    ```

## Usage

Run the harvester from the command line:

```bash
node src/index.js --path <directory_to_scan> [options]
```

### Options

-   `--path <path>`: **Required**. The root directory to start scanning from.
-   `--older-than-days <days>`: (Optional) Only show files last modified more than `days` ago.
-   `--larger-than-mb <mb>`: (Optional) Only show files larger than `mb` megabytes.
-   `--help`: Display help information.

### Examples

1.  **Find all files older than 365 days in your 'documents' folder**:
    ```bash
    node src/index.js --path ~/documents --older-than-days 365
    ```

2.  **Find all files larger than 100MB in your 'downloads' folder**:
    ```bash
    node src/index.js --path ~/downloads --larger-than-mb 100
    ```

3.  **Find large, old files in your entire home directory**:
    ```bash
    node src/index.js --path ~ --older-than-days 180 --larger-than-mb 50
    ```

## Development & Testing

To run the tests:

```bash
npm test
```

## Contributing

Feel free to contribute to the digital archaeology! Open issues or submit pull requests.
