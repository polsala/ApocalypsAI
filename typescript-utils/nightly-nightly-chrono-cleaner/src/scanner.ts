import { promises as fs } from 'fs';
import * as path from 'path';
import { ChronoCleanerConfig, TemporalEcho } from './types';

const DEPRECATED_MARKERS = [
  '// DEPRECATED', '# DEPRECATED', '/* DEPRECATED */',
  '// ARCHIVED', '# ARCHIVED', '/* ARCHIVED */',
  '@deprecated' // common JSDoc/TSDoc marker
];

export async function scanForTemporalEchoes(config: ChronoCleanerConfig): Promise<TemporalEcho[]> {
  const echoes: TemporalEcho[] = [];
  const now = new Date();
  const cutoffDate = new Date(now.getTime() - config.staleDays * 24 * 60 * 60 * 1000);

  async function traverse(currentPath: string) {
    let entries;
    try {
      entries = await fs.readdir(currentPath, { withFileTypes: true });
    } catch (error: any) {
      // console.warn(`Could not read directory ${currentPath}: ${error.message}`); // Suppress for cleaner test output
      return;
    }

    for (const entry of entries) {
      const fullPath = path.join(currentPath, entry.name);

      // Check ignore patterns
      if (config.ignorePatterns.some(pattern => fullPath.includes(pattern))) {
        continue;
      }

      if (entry.isDirectory()) {
        await traverse(fullPath);
      } else if (entry.isFile()) {
        let stats;
        try {
          stats = await fs.stat(fullPath);
        } catch (error: any) {
          // console.warn(`Could not stat file ${fullPath}: ${error.message}`); // Suppress for cleaner test output
          continue;
        }

        // Check for staleness
        if (stats.mtime < cutoffDate) {
          const ageDays = Math.floor((now.getTime() - stats.mtime.getTime()) / (1000 * 60 * 60 * 24));
          echoes.push({
            filePath: fullPath,
            reason: 'stale',
            lastModified: stats.mtime,
            ageDays: ageDays,
          });
        }

        // Check for deprecated markers (only for text files)
        if (isTextFile(fullPath)) {
          try {
            const content = await fs.readFile(fullPath, 'utf-8');
            for (const marker of DEPRECATED_MARKERS) {
              if (content.includes(marker)) {
                echoes.push({
                  filePath: fullPath,
                  reason: 'deprecated-marker',
                  markerContent: marker,
                });
                break; // Found one marker, no need to check others for this file
              }
            }
          } catch (error: any) {
            // Ignore binary files or files that can't be read as text
          }
        }
      }
    }
  }

  await traverse(config.scanPath);
  return echoes;
}

function isTextFile(filePath: string): boolean {
  const ext = path.extname(filePath).toLowerCase();
  // Simple heuristic: assume common code/text file extensions are text
  const textExtensions = [
    '.js', '.ts', '.jsx', '.tsx', '.json', '.md', '.txt', '.yml', '.yaml',
    '.html', '.css', '.scss', '.less', '.vue', '.svelte', '.php', '.py', '.java',
    '.go', '.rs', '.c', '.cpp', '.h', '.hpp', '.sh', '.xml', '.log', '.ini',
    '.conf', '.env', '.gitignore', '.editorconfig', '.prettierrc', '.eslintrc'
  ];
  return textExtensions.includes(ext) || !ext; // No extension might be a text file too
}
