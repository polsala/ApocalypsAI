import * as fs from 'fs/promises';
import * as path from 'path';
import { FileInfo, DustificationOptions } from './types';

export async function scanAndIdentifyDust(options: DustificationOptions): Promise<FileInfo[]> {
  const { path: targetPath, thresholdDays } = options;
  const dustThresholdMs = Date.now() - thresholdDays * 24 * 60 * 60 * 1000;
  const dustFiles: FileInfo[] = [];

  try {
    const entries = await fs.readdir(targetPath, { withFileTypes: true });

    for (const entry of entries) {
      const fullPath = path.join(targetPath, entry.name);
      if (entry.isFile()) {
        try {
          const stats = await fs.stat(fullPath);
          // Using mtimeMs (last modified time) as it's more relevant for "clutter" than birthtimeMs
          if (stats.mtimeMs < dustThresholdMs) {
            const ageDays = Math.floor((Date.now() - stats.mtimeMs) / (24 * 60 * 60 * 1000));
            dustFiles.push({
              path: fullPath,
              name: entry.name,
              birthtimeMs: stats.birthtimeMs,
              mtimeMs: stats.mtimeMs,
              ageDays: ageDays,
            });
          }
        } catch (statErr) {
          console.warn(`🌌 Could not stat file ${fullPath}: ${statErr instanceof Error ? statErr.message : String(statErr)}`);
        }
      } else if (entry.isDirectory()) {
        // For V1, we keep it non-recursive to simplify. A --recursive option could be added later.
      }
    }
  } catch (readDirErr) {
    console.error(`☄️ Failed to read directory ${targetPath}: ${readDirErr instanceof Error ? readDirErr.message : String(readDirErr)}`);
    throw readDirErr;
  }

  return dustFiles;
}

export async function performDustification(file: FileInfo, options: DustificationOptions): Promise<string> {
  const { action, archiveDir, dryRun } = options;
  const fileName = path.basename(file.path);

  if (dryRun) {
    return `[DRY RUN] Would ${action} ${file.path}`;
  }

  try {
    switch (action) {
      case 'archive':
        if (!archiveDir) {
          throw new Error("Archive directory not specified for 'archive' action.");
        }
        await fs.mkdir(archiveDir, { recursive: true });
        const newPath = path.join(archiveDir, fileName);
        await fs.rename(file.path, newPath);
        return `🌠 Archived '${file.path}' to '${newPath}'`;
      case 'delete':
        await fs.unlink(file.path);
        return `💥 Deleted '${file.path}'`;
      case 'list':
      default:
        return `✨ Identified '${file.path}' (modified ${file.ageDays} days ago)`;
    }
  } catch (err) {
    return `⚠️ Failed to ${action} '${file.path}': ${err instanceof Error ? err.message : String(err)}`;
  }
}
