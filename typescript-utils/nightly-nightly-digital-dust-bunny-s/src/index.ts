import * as fs from 'fs';
import * as path from 'path';
import { FileMetadata, DustBunnyConfig } from './types';

export class DigitalDustBunnySweeper {
  constructor(private config: DustBunnyConfig) {}

  private calculateDustScore(filename: string): number {
    let score = 0;
    for (const pattern of this.config.dustPatterns) {
      if (filename.includes(pattern)) { // Simple substring match for whimsy
        score += 1;
      }
    }
    return score;
  }

  private async scanDirectory(dir: string): Promise<FileMetadata[]> {
    let dustyFiles: FileMetadata[] = [];
    const now = Date.now();

    try {
      const entries = await fs.promises.readdir(dir, { withFileTypes: true });

      for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);
        let stats: fs.Stats;
        try {
          stats = await fs.promises.stat(fullPath);
        } catch (statErr) {
          // Ignore files we can't stat (e.g., broken symlinks, permission issues)
          console.warn(`Skipping file/directory '${fullPath}' due to stat error: ${statErr instanceof Error ? statErr.message : String(statErr)}`);
          continue;
        }

        if (entry.isDirectory()) {
          if (this.config.recursive) {
            dustyFiles = dustyFiles.concat(await this.scanDirectory(fullPath));
          }
        } else if (entry.isFile()) {
          const lastModifiedMs = stats.mtimeMs;
          const ageDays = Math.floor((now - lastModifiedMs) / (1000 * 60 * 60 * 24));
          const dustScore = this.calculateDustScore(entry.name);

          if (ageDays >= this.config.ageThresholdDays || dustScore >= this.config.minDustScore) {
            dustyFiles.push({
              path: fullPath,
              name: entry.name,
              isDirectory: false,
              lastModifiedMs,
              ageDays,
              dustScore,
              suggestion: ageDays >= this.config.ageThresholdDays ? 'Consider archiving or deleting due to age.' : 'Filename suggests potential clutter.'
            });
          }
        }
      }
    } catch (readDirErr) {
      console.error(`Error reading directory '${dir}': ${readDirErr instanceof Error ? readDirErr.message : String(readDirErr)}`);
    }
    return dustyFiles;
  }

  public async sweep(): Promise<FileMetadata[]> {
    const files = await this.scanDirectory(this.config.targetDir);
    // Sort by dust score descending, then age descending
    return files.sort((a, b) => {
      if (b.dustScore !== a.dustScore) {
        return b.dustScore - a.dustScore;
      }
      return b.ageDays - a.ageDays;
    });
  }
}
