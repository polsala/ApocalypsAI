import * as fs from 'fs';
import * as path from 'path';
import { FileInfo, DustBunnyReport } from './types';

const DEFAULT_AGE_DAYS = 365; // 1 year
const DEFAULT_SIZE_MB = 100; // 100 MB

export function parseArgs(args: string[]): {
  targetDir: string;
  minAgeDays: number;
  minSizeBytes: number;
  dryRun: boolean; // Always true for this utility
} {
  let targetDir: string | undefined;
  let minAgeDays = DEFAULT_AGE_DAYS;
  let minSizeBytes = DEFAULT_SIZE_MB * 1024 * 1024; // Convert MB to bytes
  const dryRun = true; // This utility always operates in dry-run mode for safety

  for (let i = 2; i < args.length; i++) {
    const arg = args[i];
    const nextArg = args[i + 1];

    if (arg.startsWith('--')) {
      switch (arg) {
        case '--age':
          if (nextArg && !nextArg.startsWith('--')) {
            minAgeDays = parseInt(nextArg, 10);
            if (isNaN(minAgeDays) || minAgeDays < 0) {
              console.error('Error: --age must be a positive number of days.');
              process.exit(1);
            }
            i++;
          } else {
            console.error('Error: --age requires a number of days.');
            process.exit(1);
          }
          break;
        case '--size':
          if (nextArg && !nextArg.startsWith('--')) {
            const sizeMb = parseInt(nextArg, 10);
            if (isNaN(sizeMb) || sizeMb < 0) {
              console.error('Error: --size must be a positive number of MB.');
              process.exit(1);
            }
            minSizeBytes = sizeMb * 1024 * 1024;
            i++;
          } else {
            console.error('Error: --size requires a number of MB.');
            process.exit(1);
          }
          break;
        default:
          console.error(`Error: Unknown argument '${arg}'`);
          process.exit(1);
      }
    } else if (!targetDir) {
      targetDir = arg;
    } else {
      console.error(`Error: Multiple target directories specified or unexpected argument '${arg}'`);
      process.exit(1);
    }
  }

  if (!targetDir) {
    console.error('Error: No target directory specified. Usage: ts-node src/index.ts <directory> [--age <days>] [--size <MB>]');
    process.exit(1);
  }

  return { targetDir, minAgeDays, minSizeBytes, dryRun };
}

export function scanDirectory(
  dirPath: string,
  minAgeDays: number,
  minSizeBytes: number,
  currentTimestamp: number // For deterministic testing
): DustBunnyReport {
  const dustBunnies: FileInfo[] = [];
  let totalFilesScanned = 0;

  let filesAndDirs: fs.Dirent[] = [];
  try {
    filesAndDirs = fs.readdirSync(dirPath, { withFileTypes: true });
  } catch (error: any) {
    if (error.code === 'EACCES') {
      console.warn(`Warning: Permission denied for directory '${dirPath}'. Skipping.`);
      return { totalFilesScanned: 0, totalDustBunniesFound: 0, dustBunnies: [] };
    } else if (error.code === 'ENOENT') {
      console.error(`Error: Directory '${dirPath}' not found. Skipping.`);
      return { totalFilesScanned: 0, totalDustBunniesFound: 0, dustBunnies: [] };
    } else {
      console.error(`Error reading directory '${dirPath}': ${error.message}. Skipping.`);
      return { totalFilesScanned: 0, totalDustBunniesFound: 0, dustBunnies: [] };
    }
  }

  for (const entry of filesAndDirs) {
    const fullPath = path.join(dirPath, entry.name);

    try {
      const stats = fs.statSync(fullPath);
      totalFilesScanned++;

      if (entry.isDirectory()) {
        const subReport = scanDirectory(fullPath, minAgeDays, minSizeBytes, currentTimestamp);
        dustBunnies.push(...subReport.dustBunnies);
        totalFilesScanned += subReport.totalFilesScanned; // Accumulate scanned files from subdirectories
      } else if (entry.isFile()) {
        const ageMs = currentTimestamp - stats.mtimeMs;
        const ageDays = ageMs / (1000 * 60 * 60 * 24);

        const isOld = ageDays > minAgeDays;
        const isLarge = stats.size > minSizeBytes;

        if (isOld || isLarge) {
          dustBunnies.push({
            path: fullPath,
            name: entry.name,
            size: stats.size,
            mtimeMs: stats.mtimeMs,
            ageDays: parseFloat(ageDays.toFixed(2)),
          });
        }
      }
    } catch (error: any) {
      // Ignore permission errors or other file access issues for individual files
      if (error.code === 'EACCES' || error.code === 'ENOENT') {
        // console.warn(`Warning: Could not access ${fullPath} - ${error.message}`);
      } else {
        console.error(`Error processing ${fullPath}: ${error.message}`);
      }
    }
  }

  return {
    totalFilesScanned: totalFilesScanned,
    totalDustBunniesFound: dustBunnies.length,
    dustBunnies: dustBunnies,
  };
}

function run() {
  const { targetDir, minAgeDays, minSizeBytes, dryRun } = parseArgs(process.argv);

  if (!fs.existsSync(targetDir)) {
    console.error(`Error: Target directory '${targetDir}' does not exist.`);
    process.exit(1);
  }

  console.log(`\n🧹 Sweeping for Digital Dust Bunnies in: ${targetDir}`);
  console.log(`   Criteria: Older than ${minAgeDays} days OR larger than ${minSizeBytes / (1024 * 1024)} MB`);
  console.log(`   Mode: Dry Run (no changes will be made)\n`);

  const currentTimestamp = Date.now(); // Use actual current time for live runs

  const report = scanDirectory(targetDir, minAgeDays, minSizeBytes, currentTimestamp);

  if (report.totalDustBunniesFound === 0) {
    console.log('✨ No digital dust bunnies found! Your digital space is sparkling clean.');
  } else {
    console.log(`Found ${report.totalDustBunniesFound} digital dust bunnies (out of ${report.totalFilesScanned} files scanned):`);
    report.dustBunnies.sort((a, b) => b.size - a.size).forEach((bunny) => {
      const sizeMB = (bunny.size / (1024 * 1024)).toFixed(2);
      const ageYears = (bunny.ageDays / 365).toFixed(1);
      console.log(`  - ${bunny.path} (Size: ${sizeMB} MB, Age: ${bunny.ageDays} days / ~${ageYears} years)`);
    });
    console.log('\nSuggestions: Consider archiving or deleting these files to free up space and improve performance.');
    console.log('Remember: This utility always performs a dry run. No files have been touched.');
  }
  console.log('\nSweep complete!');
}

// Only run if this file is executed directly
if (require.main === module) {
  run();
}
