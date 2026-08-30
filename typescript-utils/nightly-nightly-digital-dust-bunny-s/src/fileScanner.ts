import * as fs from 'fs';
import * as path from 'path';
import { FileInfo } from './types';

export async function scanDirectory(
  dirPath: string,
  thresholdDays: number,
  ignorePatterns: string[]
): Promise<FileInfo[]> {
  const dustBunnyFiles: FileInfo[] = [];
  const now = new Date();
  const thresholdMs = thresholdDays * 24 * 60 * 60 * 1000;

  const shouldIgnore = (filePath: string): boolean => {
    return ignorePatterns.some(pattern => {
      const regex = new RegExp(pattern);
      return regex.test(filePath);
    });
  };

  async function traverse(currentPath: string) {
    if (shouldIgnore(currentPath)) {
      return;
    }

    let entries: fs.Dirent[];
    try {
      entries = await fs.promises.readdir(currentPath, { withFileTypes: true });
    } catch (error: any) {
      // console.warn(`Could not read directory ${currentPath}: ${error.message}`);
      return; // Skip unreadable directories
    }

    for (const entry of entries) {
      const fullPath = path.join(currentPath, entry.name);
      if (shouldIgnore(fullPath)) {
        continue;
      }

      let stats: fs.Stats;
      try {
        stats = await fs.promises.stat(fullPath);
      } catch (error: any) {
        // console.warn(`Could not stat file ${fullPath}: ${error.message}`);
        continue; // Skip unstat-able files/symlinks
      }

      const lastModified = stats.mtime;
      const ageMs = now.getTime() - lastModified.getTime();
      const ageDays = ageMs / (24 * 60 * 60 * 1000);

      if (ageMs > thresholdMs) {
        dustBunnyFiles.push({
          path: fullPath,
          name: entry.name,
          isDir: entry.isDirectory(),
          lastModified: lastModified,
          ageDays: parseFloat(ageDays.toFixed(2)),
        });
      }

      if (entry.isDirectory()) {
        await traverse(fullPath);
      }
    }
  }

  await traverse(dirPath);
  return dustBunnyFiles;
}
