import * as fs from 'fs/promises';
import * as path from 'path';
import { PurifierConfig, DustBunnyReportItem } from './types';

/**
 * Recursively scans a directory for files matching the dust bunny criteria.
 * @param dirPath The directory to scan.
 * @param config The purifier configuration.
 * @returns A promise that resolves to an array of identified dust bunnies.
 */
export async function scanDirectory(
  dirPath: string,
  config: PurifierConfig
): Promise<DustBunnyReportItem[]> {
  const dustBunnies: DustBunnyReportItem[] = [];
  const now = new Date();
  const minAgeMs = config.minAgeDays * 24 * 60 * 60 * 1000; // Convert days to milliseconds

  async function traverse(currentPath: string) {
    let entries;
    try {
      entries = await fs.readdir(currentPath, { withFileTypes: true });
    } catch (error) {
      // Ignore directories we can't read, but log the error
      console.error(`Error reading directory ${currentPath}: ${error}`);
      return;
    }

    for (const entry of entries) {
      const fullPath = path.join(currentPath, entry.name);

      // Check against exclude patterns
      const isExcluded = config.excludePatterns.some(pattern => {
        // Simple substring match for directory/file names or full paths
        if (fullPath.includes(pattern)) return true;
        // Basic regex match for patterns like '*.log'
        if (pattern.startsWith('*') && entry.name.endsWith(pattern.substring(1))) return true;
        return false;
      });

      if (isExcluded) {
        continue;
      }

      if (entry.isDirectory()) {
        await traverse(fullPath);
      } else if (entry.isFile()) {
        let stats;
        try {
          stats = await fs.stat(fullPath);
        } catch (error) {
          console.error(`Error stating file ${fullPath}: ${error}`);
          continue;
        }

        let reason = '';
        // Check age criteria
        if (config.minAgeDays > 0 && now.getTime() - stats.mtime.getTime() > minAgeMs) {
          reason = `Older than ${config.minAgeDays} days`;
        }
        // Check size criteria
        if (config.minSizeBytes > 0 && stats.size > config.minSizeBytes) {
          reason = reason ? `${reason} and Larger than ${config.minSizeBytes} bytes` : `Larger than ${config.minSizeBytes} bytes`;
        }

        if (reason) {
          dustBunnies.push({
            filePath: fullPath,
            reason: reason,
            size: stats.size,
            lastModified: stats.mtime,
          });
        }
      }
    }
  }

  await traverse(dirPath);
  return dustBunnies;
}

/**
 * Performs actions (e.g., moving files) on identified dust bunnies.
 * @param dustBunnies The list of dust bunnies to act upon.
 * @param config The purifier configuration.
 */
export async function performActions(
  dustBunnies: DustBunnyReportItem[],
  config: PurifierConfig
): Promise<void> {
  if (config.dryRun) {
    console.log('\n--- Dry Run Mode ---');
    console.log('No files will be moved or deleted. To perform actions, omit --dry-run.');
    return;
  }

  if (!config.archiveDir) {
    console.error('Error: Archive directory not specified for non-dry-run mode. No actions performed.');
    return;
  }

  try {
    await fs.mkdir(config.archiveDir, { recursive: true });
  } catch (error) {
    console.error(`Error creating archive directory ${config.archiveDir}: ${error}`);
    return;
  }

  console.log(`\n--- Performing Actions (Moving to ${path.resolve(config.archiveDir)}) ---`);
  for (const item of dustBunnies) {
    const fileName = path.basename(item.filePath);
    const destPath = path.join(config.archiveDir, fileName);
    try {
      await fs.rename(item.filePath, destPath); // Move the file
      console.log(`Moved: ${item.filePath} -> ${destPath}`);
    } catch (error) {
      console.error(`Error moving ${item.filePath}: ${error}`);
    }
  }
}
