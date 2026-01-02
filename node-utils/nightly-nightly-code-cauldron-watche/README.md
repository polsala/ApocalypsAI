# Nightly Code Cauldron Watcher

## Summary
The `nightly-code-cauldron-watcher` is a whimsical utility that monitors a specified directory for file system changes (creations, modifications, deletions) and, instead of mundane logs, 'brews' and outputs cryptic, context-aware messages to your terminal. It's like having a mystical oracle observing your project's evolution, offering poetic insights into the shifting sands of your codebase.

## Usage

### Installation
1. Ensure you have Node.js installed.
2. Navigate to the `node-utils/nightly-code-cauldron-watcher` directory.
3. This utility uses only built-in Node.js modules, so no `npm install` is strictly required for its core functionality.

### Running the Watcher
To start the watcher, provide the path to the directory you wish to observe:

```bash
node src/index.js <path_to_watch> [config_file_path]
```

- `<path_to_watch>`: The absolute or relative path to the directory you want to monitor.
- `[config_file_path]` (optional): Path to a JSON configuration file for custom messages. If not provided, default whimsical messages will be used.

**Example:**

```bash
# Watch the current directory with default messages
node src/index.js .

# Watch a specific project directory
node src/index.js /path/to/my/project

# Watch with a custom configuration file
node src/index.js . config/cauldron_messages.json
```

## Configuration (Optional)
You can customize the messages by providing a JSON configuration file. The file should contain an object with `change`, `add`, and `delete` keys, each holding an array of string templates. The placeholder `{filename}` will be replaced with the name of the affected file.

**Example `config/cauldron_messages.json`:**

```json
{
  "change": [
    "The ancient scrolls of '{filename}' have been re-inked, a new spell is brewing!",
    "A ripple in the fabric of reality: '{filename}' shifts its form."
  ],
  "add": [
    "A new star, '{filename}', ignites in the cosmic firmament!",
    "From the primordial soup, '{filename}' takes shape. A new entity is born."
  ],
  "delete": [
    "The echoes of '{filename}' fade into the abyss. Its purpose fulfilled, or perhaps, forgotten.",
    "A whisper of sorrow: '{filename}' returns to the void. May its memory linger."
  ]
}
```

## How it Works
The utility uses Node.js's built-in `fs.watch` to detect file system events. Due to cross-platform inconsistencies with `fs.watch` event types, it employs an inference mechanism based on file existence checks to distinguish between file additions, modifications, and deletions. When an event occurs, it consults its internal (or user-provided) lexicon of mystical phrases to generate a fitting pronouncement, injecting the name of the file involved for a personalized touch of arcane wisdom.

## Contributing
Feel free to add more whimsical messages or suggest new features to enhance the Cauldron's prophetic abilities!
