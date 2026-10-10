# Nightly Digital Aura Analyzer

## 🌌 Unveil the Digital Aura of Your Files! 🌌

This whimsical CLI tool helps you bring a touch of personality to your digital landscape. It analyzes file and directory names, and in the case of directories, their immediate contents, to assign a 'Digital Aura' or 'Temporal Mood'. This can help you intuitively understand the purpose or state of your folders and files at a glance, aiding in organization, decluttering, and rediscovery.

### ✨ Features

*   **Whimsical Aura Assignment**: Maps keywords in names to predefined 'Digital Auras' like 'Ambitious Ascent', 'Serene Scroll', or 'Fleeting Whisper'.
*   **Directory Content Inference**: If a directory's name doesn't immediately suggest an aura, it peeks into its immediate children to infer a mood.
*   **Type-Safe**: Built with TypeScript for robust and predictable behavior.
*   **CLI Interface**: Easy to use from your terminal.

### 🚀 Installation

1.  **Prerequisites**: Ensure you have Node.js (which includes npm) installed.
    (Optional: `yarn` can be used instead of `npm`)

2.  **Clone the repository (if not already part of ApocalypsAI)**:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/typescript-utils/nightly-digital-aura-analyzer
    ```

3.  **Install dependencies**:
    ```bash
    npm install
    # or yarn install
    ```

4.  **Build the project**:
    ```bash
    npm run build
    # This compiles TypeScript to JavaScript in the 'dist' directory.
    ```

### 💡 Usage

Run the `aura-analyzer` command followed by the path you want to analyze.

```bash
# Using ts-node (for direct execution without prior build)
npm start -- <path/to/your/file_or_directory>

# Using the compiled JavaScript (after 'npm run build')
./dist/index.js <path/to/your/file_or_directory>
# Or, if you've linked it globally (e.g., npm link)
aura-analyzer <path/to/your/file_or_directory>
```

#### Examples:

```bash
# Analyze a project directory
npm start -- ./my-new-project
# Expected Output: Digital Aura: Vibrant Venture

# Analyze a documentation file
npm start -- ./docs/user-guide.md
# Expected Output: Digital Aura: Serene Scroll

# Analyze a temporary folder
npm start -- ./temp_files
# Expected Output: Digital Aura: Fleeting Whisper

# Analyze a folder whose name gives no clue, but contains 'src' and 'tests'
npm start -- ./unnamed-dev-folder
# Expected Output: Digital Aura: Vibrant Venture (inferred from 'src')

# Analyze a folder with no clear keywords in name or contents
npm start -- ./random-images
# Expected Output: Digital Aura: Mysterious Muddle
```

### 🛠️ Development

*   **Run Tests**: `npm test`
*   **Lint Code**: `npm run lint`

### 📜 Digital Auras Explained

Here's a quick guide to the auras this tool might reveal:

*   **Ambitious Ascent**: For projects, builds, releases – things moving forward.
*   **Serene Scroll**: For documentation, notes, guides – knowledge and learning.
*   **Fleeting Whisper**: For temporary files, drafts, scratchpads – transient thoughts.
*   **Mysterious Muddle**: For miscellaneous, unclassified data – a digital enigma.
*   **Reflective Archive**: For old, backup, legacy items – echoes of the past.
*   **Chaotic Cascade**: For bugs, fixes, errors – where things went awry.
*   **Harmonious Hub**: For shared, common, utility code – central points of collaboration.
*   **Silent Sentinel**: For configurations, environment variables, secrets – guarded information.
*   **Vibrant Venture**: For new features, source code, applications – fresh beginnings.
*   **Ephemeral Echo**: For logs, caches – traces of activity.
*   **Forgotten Fragment**: For very old, truly unclassified items – lost in the digital void.
