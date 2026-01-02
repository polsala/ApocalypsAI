const fs = require('fs');
const path = require('path');
const { generateMessage } = require('./messageGenerator');

const watchPath = process.argv[2];
const configFilePath = process.argv[3];

if (!watchPath) {
  console.error('Usage: node src/index.js <path_to_watch> [config_file_path]');
  process.exit(1);
}

let customConfig = null;
if (configFilePath) {
  try {
    const resolvedConfigPath = path.resolve(configFilePath);
    const configContent = fs.readFileSync(resolvedConfigPath, 'utf8');
    customConfig = JSON.parse(configContent);
    console.log(`\n🔮 Cauldron configured with custom messages from: ${resolvedConfigPath}\n`);
  } catch (error) {
    console.error(`Error loading config file '${configFilePath}':`, error.message);
    process.exit(1);
  }
}

try {
  fs.accessSync(watchPath, fs.constants.R_OK);
} catch (error) {
  console.error(`Error: Cannot access path '${watchPath}'. Please ensure it exists and is readable.`);
  process.exit(1);
}

console.log(`\n✨ The Nightly Code Cauldron is now watching '${path.resolve(watchPath)}' for shifts in the ether...\n`);

// fs.watch can emit 'rename' for both file creation and deletion.
// It can also emit 'change' for modifications.
// The exact behavior can vary slightly across platforms.
// We'll try to infer add/delete based on file existence.
const watchedFiles = new Set();

// Initialize watchedFiles with existing files
try {
  const initialFiles = fs.readdirSync(watchPath);
  for (const file of initialFiles) {
    const fullPath = path.join(watchPath, file);
    try {
      if (fs.statSync(fullPath).isFile()) {
        watchedFiles.add(file);
      }
    } catch (statError) {
      // Ignore files that might disappear between readdirSync and statSync
    }
  }
} catch (readDirError) {
  console.error(`Warning: Could not read initial directory contents for '${watchPath}':`, readDirError.message);
}

fs.watch(watchPath, { recursive: true }, (eventType, filename) => {
  if (filename) {
    const fullPath = path.join(watchPath, filename);
    let inferredEventType = eventType;

    // Attempt to infer 'add' or 'delete' from 'rename' event
    if (eventType === 'rename') {
      try {
        fs.accessSync(fullPath, fs.constants.F_OK);
        // If file exists after 'rename', it's likely an 'add'
        if (!watchedFiles.has(filename)) {
          inferredEventType = 'add';
          watchedFiles.add(filename);
        } else {
          // If it existed before and still exists, it might be a rename of another file
          // or a 'change' that triggered 'rename' on some platforms. Default to change.
          inferredEventType = 'change';
        }
      } catch (e) {
        // If file does not exist after 'rename', it's likely a 'delete'
        if (watchedFiles.has(filename)) {
          inferredEventType = 'delete';
          watchedFiles.delete(filename);
        } else {
          // File didn't exist before and doesn't exist now, ignore (e.g., temp file cleanup)
          return;
        }
      }
    } else if (eventType === 'change') {
      // Ensure the file exists and was previously tracked or is new
      try {
        fs.accessSync(fullPath, fs.constants.F_OK);
        if (!watchedFiles.has(filename)) {
          // If a 'change' event occurs on a file not yet tracked, treat as add
          inferredEventType = 'add';
          watchedFiles.add(filename);
        }
      } catch (e) {
        // File changed but now doesn't exist, treat as delete
        if (watchedFiles.has(filename)) {
          inferredEventType = 'delete';
          watchedFiles.delete(filename);
        } else {
          return; // Ignore change on non-existent or untracked file
        }
      }
    }

    const message = generateMessage(inferredEventType, filename, customConfig);
    console.log(`[${new Date().toLocaleTimeString()}] ${message}`);
  }
});

process.on('SIGINT', () => {
  console.log('\n🌌 The Cauldron\'s vigil ends. Until next time, seeker.');
  process.exit(0);
});
