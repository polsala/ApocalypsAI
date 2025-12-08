const fs = require('fs').promises;
const path = require('path');
const { getRandomWhimsySuffix } = require('./whimsy-names');

/**
 * Analyzes a given directory to identify old and large files.
 * @param {string} directory - The path to the directory to analyze.
 * @param {object} options - Configuration options.
 * @param {number} [options.ageThresholdDays=365] - Files older than this many days are 'Forgotten Relics'.
 * @param {number} [options.sizeThresholdBytes=104857600] - Files larger than this many bytes are 'Space Gobblers'.
 * @param {boolean} [options.whimsicalRename=false] - If true, suggests whimsical renames for old files.
 * @returns {Promise<object>} An object containing lists of forgottenRelics, spaceGobblers, and renamedFiles suggestions.
 */
async function analyzeHoard(directory, options = {}) {
  const {
    ageThresholdDays = 365, // 1 year
    sizeThresholdBytes = 100 * 1024 * 1024, // 100 MB
    whimsicalRename = false,
  } = options;

  const now = Date.now();
  const forgottenRelics = [];
  const spaceGobblers = [];
  const renamedFiles = [];

  async function walk(currentPath) {
    let entries;
    try {
      entries = await fs.readdir(currentPath, { withFileTypes: true });
    } catch (error) {
      // console.warn(`Could not read directory ${currentPath}: ${error.message}`); // Suppress for cleaner test output, handled by test spy
      return;
    }

    for (const entry of entries) {
      const fullPath = path.join(currentPath, entry.name);
      if (entry.isDirectory()) {
        await walk(fullPath);
      } else if (entry.isFile()) {
        let stats;
        try {
          stats = await fs.stat(fullPath);
        } catch (error) {
          // console.warn(`Could not stat file ${fullPath}: ${error.message}`); // Suppress for cleaner test output, handled by test spy
          continue;
        }

        const ageMs = now - stats.mtimeMs;
        const ageDays = ageMs / (1000 * 60 * 60 * 24);

        if (ageDays > ageThresholdDays) {
          forgottenRelics.push({
            path: fullPath,
            ageDays: Math.round(ageDays),
            sizeBytes: stats.size,
          });
          if (whimsicalRename) {
            const fileNameParts = entry.name.split('.');
            const extension = fileNameParts.length > 1 ? `.${fileNameParts.pop()}` : '';
            const baseName = fileNameParts.join('.');
            const newName = `${baseName}${getRandomWhimsySuffix()}${extension}`;
            const newPath = path.join(currentPath, newName);
            // In a real utility, this would be fs.rename. For this exercise, we just report the suggestion.
            renamedFiles.push({ oldPath: fullPath, newPath: newPath });
          }
        }

        if (stats.size > sizeThresholdBytes) {
          spaceGobblers.push({
            path: fullPath,
            sizeBytes: stats.size,
            sizeMB: (stats.size / (1024 * 1024)).toFixed(2),
          });
        }
      }
    }
  }

  await walk(directory);

  return {
    forgottenRelics,
    spaceGobblers,
    renamedFiles,
  };
}

// CLI execution
if (require.main === module) {
  const args = process.argv.slice(2);
  const directory = args[0] || '.';
  const ageThresholdDays = parseInt(args[1], 10) || 365;
  const sizeThresholdMB = parseInt(args[2], 10) || 100;
  const whimsicalRename = args.includes('--whimsical-rename');

  console.log(`Analyzing digital hoard in: ${directory}`);
  console.log(`Looking for files older than ${ageThresholdDays} days and larger than ${sizeThresholdMB} MB.`);
  if (whimsicalRename) {
    console.log("Whimsical renaming of old files is enabled (report only).");
  }

  analyzeHoard(directory, {
    ageThresholdDays,
    sizeThresholdBytes: sizeThresholdMB * 1024 * 1024,
    whimsicalRename,
  })
    .then(results => {
      console.log('\n--- Hoard Analysis Report ---');

      if (results.forgottenRelics.length > 0) {
        console.log('\nForgotten Relics (Older than ' + ageThresholdDays + ' days):');
        results.forgottenRelics.forEach(file => {
          console.log(`  - ${file.path} (Age: ${file.ageDays} days, Size: ${(file.sizeBytes / (1024 * 1024)).toFixed(2)} MB)`);
        });
      } else {
        console.log('\nNo Forgotten Relics found. Your digital garden is well-tended!');
      }

      if (results.spaceGobblers.length > 0) {
        console.log('\nSpace Gobblers (Larger than ' + sizeThresholdMB + ' MB):');
        results.spaceGobblers.forEach(file => {
          console.log(`  - ${file.path} (Size: ${file.sizeMB} MB)`);
        });
      } else {
        console.log('\nNo Space Gobblers found. Your storage is lean!');
      }

      if (whimsicalRename && results.renamedFiles.length > 0) {
        console.log('\nWhimsical Renaming Suggestions (for old files):');
        results.renamedFiles.forEach(file => {
          console.log(`  - ${file.oldPath} -> ${file.newPath}`);
        });
      } else if (whimsicalRename) {
        console.log('\nNo files suggested for whimsical renaming.');
      }

      console.log('\n--- End Report ---');
    })
    .catch(error => {
      console.error('An error occurred during hoard analysis:', error);
      process.exit(1);
    });
}

module.exports = { analyzeHoard };
