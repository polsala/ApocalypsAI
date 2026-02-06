# Nightly Digital Dust Bunny Sweeper

## 🧹 Unearthing the Forgotten Bits 🧹

This whimsical utility, the **Nightly Digital Dust Bunny Sweeper**, helps you discover those long-forgotten files lurking in the digital corners of your filesystem. Like a diligent digital archaeologist, it sifts through your directories, identifying "dust bunnies" – files older than a specified age – and gently reminds you of their melancholic existence.

It doesn't delete anything; it merely reports, allowing you to decide the fate of these digital relics.

## ✨ Features

*   **Recursive Scanning**: Delves deep into subdirectories.
*   **Age-Based Filtering**: Specify how old a file must be to be considered a "dust bunny".
*   **Whimsical Reporting**: Presents findings with a touch of digital melancholy.
*   **Cross-Platform**: Built with Node.js, it runs wherever Node.js does.

## 🚀 Installation

1.  **Ensure Node.js is installed**: If not, download it from [nodejs.org](https://nodejs.org/).
2.  **Clone the repository (or copy this utility)**:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/node-utils/nightly-digital-dust-bunny-sweeper
    ```
3.  **Install dependencies**:
    ```bash
    npm install
    ```

## 💡 Usage

Run the utility from your terminal:

```bash
node src/index.js <directory_path> <age_in_days>
```

*   `<directory_path>`: The path to the directory you want to scan.
*   `<age_in_days>`: The minimum age (in days) for a file to be considered a "digital dust bunny".

### Examples:

Scan your current directory for files older than 30 days:
```bash
node src/index.js . 30
```

Scan your `~/Documents` folder for files older than 365 days:
```bash
node src/index.js ~/Documents 365
```

## 🧪 Running Tests

To ensure the Digital Dust Bunny Sweeper is functioning correctly, run the automated tests:

```bash
npm test
```

The tests are self-contained and use mocks to ensure deterministic and offline execution.
