#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

/**
 * Recursively gets all file paths within a directory.
 * @param {string} dirPath - The directory to scan.
 * @param {string[]} arrayOfFiles - Accumulator for file paths.
 * @returns {string[]} An array of absolute file paths.
 */
function getFilesRecursively(dirPath, arrayOfFiles = []) {
  try {
    const files = fs.readdirSync(dirPath);

    files.forEach(file => {
      const filePath = path.join(dirPath, file);
      try {
        const stats = fs.statSync(filePath);
        if (stats.isDirectory()) {
          arrayOfFiles = getFilesRecursively(filePath, arrayOfFiles);
        } else {
          arrayOfFiles.push(filePath);
        }
      } catch (statErr) {
        console.warn(`[33mWarning: Could not stat file/directory [1m${filePath}[0m[33m. Skipping. Error: ${statErr.message}[0m`);
      }
    });
  } catch (readDirErr) {
    console.error(`[31mError: Could not read directory [1m${dirPath}[0m[31m. Skipping. Error: ${readDirErr.message}[0m`);
  }
  return arrayOfFiles;
}

/**
 * Calculates the age of a file in days based on its modification time.
 * @param {fs.Stats} stats - The fs.Stats object for the file.
 * @returns {number} The age of the file in days.
 */
function getFileAgeInDays(stats) {
  const now = new Date();
  const mtime = new Date(stats.mtime);
  const diffTime = Math.abs(now.getTime() - mtime.getTime());
  return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
}

/**
 * The main function to sweep for digital dust bunnies.
 * @param {string} targetPath - The path to sweep.
 * @param {number} ageThresholdDays - Files older than this will be targeted.
 * @param {boolean} dryRun - If true, only report, don't modify files.
 * @param {string | null} quarantinePath - If provided, move files here instead of deleting.
 * @param {boolean} deleteFiles - If true, delete files directly (overrides quarantine).
 */
async function sweepDigitalDust(targetPath, ageThresholdDays, dryRun, quarantinePath, deleteFiles) {
  console.log(`[36mInitiating Digital Dust Sweep in [1m${targetPath}[0m[36m for files older than [1m${ageThresholdDays}[0m[36m days...[0m`);

  if (dryRun) {
    console.log("[33m(Dry Run Mode: No files will be moved or deleted)[0m");
  } else if (deleteFiles) {
    console.log("[31m(Deletion Mode: Files will be permanently deleted!)[0m");
  } else if (quarantinePath) {
    console.log(`[32m(Quarantine Mode: Files will be moved to [1m${quarantinePath}[0m[32m)[0m`);
    if (!fs.existsSync(quarantinePath)) {
      try {
        fs.mkdirSync(quarantinePath, { recursive: true });
        console.log(`[32mCreated quarantine zone: [1m${quarantinePath}[0m`);
      } catch (err) {
        console.error(`[31mError creating quarantine directory [1m${quarantinePath}[0m[31m: ${err.message}. Aborting quarantine operation.[0m`);
        quarantinePath = null; // Disable quarantine if creation fails
      }
    }
  }

  const allFiles = getFilesRecursively(targetPath);
  const dustBunnies = [];

  for (const filePath of allFiles) {
    try {
      const stats = fs.statSync(filePath);
      const age = getFileAgeInDays(stats);

      if (age > ageThresholdDays) {
        dustBunnies.push({ filePath, age });
      }
    } catch (err) {
      console.warn(`[33mWarning: Could not get stats for [1m${filePath}[0m[33m. Skipping. Error: ${err.message}[0m`);
    }
  }

  if (dustBunnies.length === 0) {
    console.log("[32m🐰 No digital dust bunnies found! Your system is sparkling clean.[0m");
    return;
  }

  console.log(`[35mFound [1m${dustBunnies.length}[0m[35m digital dust bunnies:[0m`);
  for (const bunny of dustBunnies) {
    console.log(`  - [90m${bunny.filePath}[0m ([35m${bunny.age}[0m days old)`);

    if (!dryRun) {
      try {
        if (deleteFiles) {
          fs.unlinkSync(bunny.filePath);
          console.log(`    [31m🗑 Deleted: [1m${bunny.filePath}[0m`);
        } else if (quarantinePath) {
          const newPath = path.join(quarantinePath, path.basename(bunny.filePath));
          fs.renameSync(bunny.filePath, newPath);
          console.log(`    [32m🔒 Quarantined to: [1m${newPath}[0m`);
        }
      } catch (actionErr) {
        console.error(`[31mError processing [1m${bunny.filePath}[0m[31m: ${actionErr.message}[0m`);
      }
    }
  }

  console.log(`[36m
Digital Dust Sweep complete! Your system feels lighter.[0m`);
}

// --- CLI Argument Parsing ---
const args = process.argv.slice(2);

let targetPath = null;
let ageThresholdDays = null;
let dryRun = false;
let quarantineDir = null;
let deleteFiles = false;

for (let i = 0; i < args.length; i++) {
  const arg = args[i];
  if (arg.startsWith('--')) {
    switch (arg) {
      case '--age':
        ageThresholdDays = parseInt(args[++i], 10);
        break;
      case '--dry-run':
        dryRun = true;
        break;
      case '--quarantine':
        quarantineDir = args[++i];
        break;
      case '--delete':
        deleteFiles = true;
        break;
      case '--help':
        console.log(`
Usage: digital-dust-sweeper <path> --age <days> [options]

Arguments:
  <path>                 The root directory to start sweeping from.

Options:
  --age <days>           Files older than this many days will be considered 'digital dust bunnies'. (Required)
  --dry-run              Perform a scan and report findings without modifying files.
  --quarantine <dir>     Move identified files to this directory instead of deleting them.
  --delete               Directly delete identified files. Use with extreme caution! Overrides --quarantine.
  --help                 Display this help message.
        `);
        process.exit(0);
      default:
        console.warn(`[33mUnknown option: ${arg}[0m`);
    }
  } else if (!targetPath) {
    targetPath = arg;
  }
}

if (!targetPath || !ageThresholdDays) {
  console.error("[31mError: Missing required arguments. Please specify a target path and an age threshold (--age).[0m");
  console.log("Run 'digital-dust-sweeper --help' for more information.");
  process.exit(1);
}

// Resolve paths to be absolute for consistency
targetPath = path.resolve(targetPath);
if (quarantineDir) {
  quarantineDir = path.resolve(quarantineDir);
}

sweepDigitalDust(targetPath, ageThresholdDays, dryRun, quarantineDir, deleteFiles);
