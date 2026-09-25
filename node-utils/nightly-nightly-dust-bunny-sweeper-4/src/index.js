const { program } = require('commander');
const { readdir, stat, unlink, mkdir, rename } = require('fs/promises');
const path = require('path');
const readline = require('readline');

// # Mock rationale: readline is mocked in tests to control user input.
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

async function prompt(query) {
  return new Promise(resolve => rl.question(query, resolve));
}

async function getDustBunnies(directory, ageThresholdDays) {
  const now = Date.now();
  const dustBunnies = [];

  try {
    const files = await readdir(directory, { withFileTypes: true });

    for (const file of files) {
      if (file.isFile()) {
        const filePath = path.join(directory, file.name);
        try {
          const stats = await stat(filePath);
          const fileAgeMs = now - stats.mtimeMs;
          const fileAgeDays = fileAgeMs / (1000 * 60 * 60 * 24);

          if (fileAgeDays > ageThresholdDays) {
            dustBunnies.push({
              name: file.name,
              path: filePath,
              size: stats.size,
              ageDays: fileAgeDays
            });
          }
        } catch (statErr) {
          console.warn(`Could not stat file ${filePath}: ${statErr.message}`);
        }
      }
    }
  } catch (readDirErr) {
    console.error(`Error reading directory ${directory}: ${readDirErr.message}`);
    process.exit(1);
  }

  return dustBunnies.sort((a, b) => b.ageDays - a.ageDays);
}

function formatBytes(bytes, decimals = 2) {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

async function main() {
  program
    .argument('<directory>', 'The directory to scan for digital dust bunnies')
    .option('-a, --age <days>', 'Minimum age in days for a file to be considered a dust bunny', '30')
    .option('-m, --mode <mode>', 'Operation mode: report (default), delete, or archive', 'report')
    .option('-o, --output <path>', '(Only for archive mode) The path to the archive directory')
    .option('-y, --yes', 'Skip confirmation prompts and proceed with the action', false)
    .action(async (directory, options) => {
      const ageThresholdDays = parseInt(options.age, 10);
      const mode = options.mode.toLowerCase();
      const skipConfirm = options.yes;
      const archivePath = options.output ? path.resolve(options.output) : path.join(directory, 'archive_dust_bunnies');

      if (isNaN(ageThresholdDays) || ageThresholdDays < 0) {
        console.error('Error: Age must be a non-negative number of days.');
        process.exit(1);
      }

      if (!['report', 'delete', 'archive'].includes(mode)) {
        console.error('Error: Invalid mode. Choose from "report", "delete", or "archive".');
        process.exit(1);
      }

      console.log(`\nScanning '${directory}' for digital dust bunnies older than ${ageThresholdDays} days...`);

      const dustBunnies = await getDustBunnies(directory, ageThresholdDays);

      if (dustBunnies.length === 0) {
        console.log('No digital dust bunnies found! Your digital space is sparkling clean.');
        rl.close();
        return;
      }

      console.log(`\nFound ${dustBunnies.length} digital dust bunnies:\n`);
      dustBunnies.forEach((bunny, index) => {
        console.log(`  ${index + 1}. ${bunny.name} (Fluffiness: ${formatBytes(bunny.size)}, Age: ${bunny.ageDays.toFixed(1)} days)`);
      });

      if (mode === 'report') {
        console.log('\nMode is "report". No actions taken. Use --mode delete or --mode archive to clean up.');
        rl.close();
        return;
      }

      let confirmAction = skipConfirm ? 'yes' : await prompt(`\nProceed to ${mode} these ${dustBunnies.length} dust bunnies? (yes/no): `);
      rl.close(); // Close readline interface after prompt

      if (confirmAction.toLowerCase() !== 'yes') {
        console.log('Operation cancelled.');
        return;
      }

      console.log(`\nInitiating ${mode} operation...`);

      for (const bunny of dustBunnies) {
        try {
          if (mode === 'delete') {
            await unlink(bunny.path);
            console.log(`  Swept away: ${bunny.name}`);
          } else if (mode === 'archive') {
            await mkdir(archivePath, { recursive: true });
            const newPath = path.join(archivePath, bunny.name);
            await rename(bunny.path, newPath);
            console.log(`  Archived: ${bunny.name} to ${archivePath}`);
          }
        } catch (actionErr) {
          console.error(`  Failed to ${mode} ${bunny.name}: ${actionErr.message}`);
        }
      }
      console.log('\nCleanup complete!');
    });

  program.parse(process.argv);
}

if (require.main === module) {
  main();
}

// Export for testing purposes
module.exports = {
  getDustBunnies,
  formatBytes,
  main, // Export main for testing CLI parsing and execution flow
  _rl: rl // Export readline interface for mocking in tests
};
