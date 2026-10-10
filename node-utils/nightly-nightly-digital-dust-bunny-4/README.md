# Nightly Digital Dust Bunny Sweeper

A whimsical Node.js utility to help you declutter your digital workspace by finding and "composting" old, unused files and directories. Keep your projects sparkling clean and free up valuable disk space!

## How it Works

The Digital Dust Bunny Sweeper scans a specified directory (and its subdirectories, excluding common development folders like `node_modules` and `.git`) for files and folders that haven't been modified in a long time. Any digital artifact older than your specified age threshold is considered a "dust bunny."

Once identified, these dust bunnies can be moved to a designated "digital compost heap" – a special directory where they can reside until you decide their ultimate fate (deletion or revival).

## Installation

1.  **Ensure Node.js is installed**: You need Node.js (v14 or higher recommended) to run this utility.
    You can download it from [nodejs.org](https://nodejs.org/).

2.  **Clone the repository (or copy the utility)**:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/node-utils/nightly-digital-dust-bunny
    ```

3.  **Install dependencies**: 
    ```bash
    npm install
    ```
    (This will install `jest` for running tests.)

## Usage

Run the utility from your terminal, providing the target directory to scan, the age threshold in days, and the path to your digital compost directory.

```bash
node src/index.js <target_directory> <age_threshold_days> <compost_directory>
```

-   `<target_directory>`: The root directory where the sweeper will start looking for dust bunnies.
-   `<age_threshold_days>`: Files/directories older than this many days (based on last modification time) will be identified as dust bunnies.
-   `<compost_directory>`: The path to the directory where identified dust bunnies will be moved. This directory will be created if it doesn't exist.

### Example

To find all files and folders in your `~/my_old_project` directory that are older than 90 days and move them to `~/digital_compost`:

```bash
node src/index.js ~/my_old_project 90 ~/digital_compost
```

## Development & Testing

To run the automated tests:

```bash
npm test
```

This will execute the Jest tests to ensure the sweeper is functioning correctly.
