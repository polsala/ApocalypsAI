import * as fs from 'fs';
import * as path from 'path';
import { ScanOptions, ResidueItem } from './types';

export class TemporalResidueScanner {
  constructor(private options: ScanOptions) {}

  async scan(): Promise<ResidueItem[]> {
    const residues: ResidueItem[] = [];
    const now = new Date();
    const minAgeMs = this.options.minAgeDays * 24 * 60 * 60 * 1000;

    await this.traverseDirectory(this.options.path, now, minAgeMs, residues);

    return residues;
  }

  private async traverseDirectory(
    currentPath: string,
    now: Date,
    minAgeMs: number,
    residues: ResidueItem[]
  ): Promise<void> {
    try {
      const entries = await fs.promises.readdir(currentPath, { withFileTypes: true });

      for (const entry of entries) {
        const fullPath = path.join(currentPath, entry.name);

        // Check ignore patterns
        if (this.options.ignorePatterns.some(pattern => fullPath.includes(pattern))) {
          continue;
        }

        const stats = await fs.promises.stat(fullPath);
        const lastModified = stats.mtime;
        const ageMs = now.getTime() - lastModified.getTime();

        if (entry.isDirectory()) {
          // Check if directory is old
          if (ageMs > minAgeMs) {
            residues.push({
              path: fullPath,
              type: 'directory',
              lastModified,
              reason: `Directory older than ${this.options.minAgeDays} days.`
            });
          }
          // Recursively scan subdirectories
          await this.traverseDirectory(fullPath, now, minAgeMs, residues);
        } else if (entry.isFile()) {
          // Check if file is old
          if (ageMs > minAgeMs) {
            residues.push({
              path: fullPath,
              type: 'file',
              lastModified,
              reason: `File older than ${this.options.minAgeDays} days.`
            });
          }
          // Optionally, add checks for includePatterns if they define "residue"
          // For now, only age is the primary residue criterion.
        }
      }
    } catch (error: any) {
      // console.warn(`Could not read directory ${currentPath}: ${error.message}`);
      // Ignore permission errors or non-existent paths for robustness
      // For example, if a directory is deleted during scan or permissions change.
    }
  }
}
