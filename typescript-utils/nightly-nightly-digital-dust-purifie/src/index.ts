import { loadConfig } from './config';
import { scanDirectory, performActions } from './purifier';
import { PurifierConfig } from './types';
import * as path from 'path';

/**
 * Parses command-line arguments into a partial PurifierConfig object.
 * @param args Raw command-line arguments (e.g., process.argv.slice(2)).
 * @returns A partial configuration object.
 */
function parseArgs(args: string[]): Partial<PurifierConfig> {
  const cliConfig: Partial<PurifierConfig> = {};
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === '--age' && args[i + 1]) {
      cliConfig.minAgeDays = parseInt(args[++i], 10);
    } else if (arg === '--size' && args[i + 1]) {
      cliConfig.minSizeBytes = parseInt(args[++i], 10);
    } else if (arg === '--exclude' && args[i + 1]) {
      // Append to existing exclude patterns if any, otherwise create new array
      cliConfig.excludePatterns = (cliConfig.excludePatterns || []).concat(args[++i].split(','));
    } else if (arg === '--dry-run') {
      cliConfig.dryRun = true;
    } else if (arg === '--archive-dir' && args[i + 1]) {
      cliConfig.archiveDir = args[++i];
      cliConfig.dryRun = false; // If archive-dir is specified, assume not dry-run unless --dry-run is also present
    } else if (!arg.startsWith('--') && !cliConfig.targetPath) {
      // The first non-flag argument is considered the target path
      cliConfig.targetPath = arg;
    }
  }
  return cliConfig;
}

/**
 * Main function to run the Digital Dust Purifier CLI.
 */
async function main() {
  const cliArgs = parseArgs(process.argv.slice(2));
  const config = loadConfig(cliArgs);

  console.log(`\nScanning for digital dust bunnies in: ${path.resolve(config.targetPath)}`);
  console.log(`Configuration:`);
  console.log(`  Min Age: ${config.minAgeDays} days`);
  console.log(`  Min Size: ${config.minSizeBytes} bytes`);
  console.log(`  Exclude Patterns: ${config.excludePatterns.join(', ')}`);
  console.log(`  Dry Run: ${config.dryRun}`);
  if (config.archiveDir) {
    console.log(`  Archive Directory: ${path.resolve(config.archiveDir)}`);
  }

  const dustBunnies = await scanDirectory(config.targetPath, config);

  if (dustBunnies.length === 0) {
    console.log('\n✨ No digital dust bunnies found! Your digital space is sparkling clean. ✨');
  } else {
    console.log(`\nFound ${dustBunnies.length} digital dust bunnies:`);
    dustBunnies.forEach((item, index) => {
      console.log(`  ${index + 1}. ${item.filePath} (Size: ${item.size} bytes, Last Modified: ${item.lastModified.toLocaleDateString()}, Reason: ${item.reason})`);
    });

    await performActions(dustBunnies, config);
  }
}

main().catch(console.error);
