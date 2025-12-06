import * as fs from 'node:fs/promises';
import * as path from 'node:path';
import { classifyFile, FileMetadata, RelicCategory, RelicConfig, RelicReportEntry } from './relicClassifier';

const DEFAULT_ANCIENT_DAYS = 365;
const DEFAULT_FORGOTTEN_DAYS = 90;
const DEFAULT_MIN_SIZE_KB = 0;

/**
 * Recursively scans a directory and classifies files.
 * @param dirPath The path to the directory to scan.
 * @param config The relic classification configuration.
 * @returns A promise that resolves to an array of relic report entries.
 */
async function scanDirectory(dirPath: string, config: RelicConfig): Promise<RelicReportEntry[]> {
  const results: RelicReportEntry[] = [];
  let entries;

  try {
    entries = await fs.readdir(dirPath, { withFileTypes: true });
  } catch (error) {
    console.error(`Error reading directory ${dirPath}:`, error);
    return results;
  }

  for (const entry of entries) {
    const fullPath = path.join(dirPath, entry.name);
    if (entry.name === 'node_modules' || entry.name.startsWith('.')) {
      continue; // Skip common ignored directories and hidden files/folders
    }

    try {
      const stats = await fs.stat(fullPath);
      const metadata: FileMetadata = {
        path: fullPath,
        size: stats.size,
        createdAt: stats.birthtime,
        modifiedAt: stats.mtime,
        accessedAt: stats.atime,
        isDirectory: stats.isDirectory(),
      };

      const classification = classifyFile(metadata, config);
      results.push(classification);

      if (stats.isDirectory()) {
        results.push(...await scanDirectory(fullPath, config)); // Recurse into subdirectories
      }
    } catch (error) {
      console.warn(`Could not get stats for ${fullPath}:`, error);
    }
  }
  return results;
}

/**
 * Main function to parse arguments and run the relic identifier.
 */
async function main() {
  const args = process.argv.slice(2);
  let targetDir: string | undefined;
  let ancientDays = DEFAULT_ANCIENT_DAYS;
  let forgottenDays = DEFAULT_FORGOTTEN_DAYS;
  let minSizeKB = DEFAULT_MIN_SIZE_KB;

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg.startsWith('--')) {
      const value = parseInt(args[i + 1]);
      if (isNaN(value)) {
        console.error(`Error: Invalid value for ${arg}. Must be a number.`);
        process.exit(1);
      }
      switch (arg) {
        case '--ancient-days':
          ancientDays = value;
          i++;
          break;
        case '--forgotten-days':
          forgottenDays = value;
          i++;
          break;
        case '--min-size-kb':
          minSizeKB = value;
          i++;
          break;
        default:
          console.warn(`Unknown argument: ${arg}. Ignoring.`);
      }
    } else if (!targetDir) {
      targetDir = arg;
    } else {
      console.warn(`Multiple target directories specified. Using '${targetDir}'. Ignoring '${arg}'.`);
    }
  }

  if (!targetDir) {
    console.error('Usage: npx ts-node src/index.ts <directory> [--ancient-days N] [--forgotten-days N] [--min-size-kb N]');
    process.exit(1);
  }

  const config: RelicConfig = {
    ancientDays,
    forgottenDays,
    minSizeKB,
  };

  console.log(`Scanning directory: ${targetDir}`);
  console.log(`Configuration: Ancient > ${config.ancientDays} days, Forgotten > ${config.forgottenDays} days, Min Size > ${config.minSizeKB} KB`);
  console.log('\n--- Digital Relic Report ---\n');

  const report = await scanDirectory(targetDir, config);

  report.forEach(entry => {
    console.log(`[${entry.category}] ${entry.path}`);
    entry.reason.forEach(r => console.log(`    Reason: ${r}`));
  });

  console.log('\n--- Scan Complete ---');
}

if (require.main === module) {
  main();
}
