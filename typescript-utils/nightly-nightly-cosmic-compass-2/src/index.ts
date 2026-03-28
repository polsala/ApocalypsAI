import * as fs from 'fs';
import * as path from 'path';
import { CelestialBody, CosmicAtlas, SearchResult } from './types';

export class CosmicCompass {
  private atlas: CosmicAtlas = {};
  private rootPath: string;

  constructor(rootPath: string) {
    this.rootPath = path.resolve(rootPath);
  }

  /**
   * Scans the root path and recursively builds the cosmic atlas.
   * @param currentPath The path to scan, defaults to rootPath.
   */
  public async buildAtlas(currentPath: string = this.rootPath): Promise<void> {
    let entries;
    try {
      entries = await fs.promises.readdir(currentPath, { withFileTypes: true });
    } catch (error: any) {
      // Ignore permission errors or other read errors for robustness, but log them
      console.warn(`
🌌 Cosmic Compass Warning: Could not read stellar path '${currentPath}'. Skipping. Error: ${error.message}`);
      return;
    }

    for (const entry of entries) {
      const fullPath = path.join(currentPath, entry.name);
      const relativePath = path.relative(this.rootPath, fullPath);

      if (entry.isDirectory()) {
        this.atlas[relativePath] = {
          path: relativePath,
          name: entry.name,
          type: 'directory',
        };
        await this.buildAtlas(fullPath); // Recurse into subdirectories
      } else if (entry.isFile()) {
        // For simplicity, we'll only store path and name for now.
        // Content reading can be added here if full text search is desired.
        this.atlas[relativePath] = {
          path: relativePath,
          name: entry.name,
          type: 'file',
        };
      }
    }
  }

  /**
   * Searches the cosmic atlas for celestial bodies matching keywords.
   * Currently searches by path/name.
   * @param keywords Keywords to search for.
   * @returns An array of search results.
   */
  public searchAtlas(keywords: string[]): SearchResult[] {
    const results: SearchResult[] = [];
    const lowerCaseKeywords = keywords.map(k => k.toLowerCase());

    for (const relativePath in this.atlas) {
      const celestialBody = this.atlas[relativePath];
      const targetString = `${celestialBody.name} ${celestialBody.path}`.toLowerCase();

      const matches = lowerCaseKeywords.filter(keyword => targetString.includes(keyword));

      if (matches.length > 0) {
        results.push({
          celestialBody,
          matches: matches.map(m => `Found '${m}' in path/name`), // Placeholder for more detailed matches
        });
      }
    }
    return results;
  }

  /**
   * Returns the entire cosmic atlas.
   */
  public getAtlas(): CosmicAtlas {
    return this.atlas;
  }
}
