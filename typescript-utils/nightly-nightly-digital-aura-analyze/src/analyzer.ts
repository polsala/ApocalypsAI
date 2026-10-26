import * as path from 'path';
import { DigitalAura, KeywordMap } from './types';
import { keywordToAuraMap } from './keywords';
import { promises as fsPromises } from 'fs';

/**
 * Interface for a simplified file system interaction, allowing for mocking.
 */
interface FileSystem {
  stat(path: string): Promise<{ isDirectory(): boolean; isFile(): boolean }>;
  readdir(path: string): Promise<string[]>;
}

/**
 * Analyzes a given file or directory path to assign a Digital Aura.
 * It first checks the path's name for keywords, then (if it's a directory
 * and no direct name match) it checks its immediate contents.
 * @param targetPath The path to analyze.
 * @param fs An optional FileSystem implementation for dependency injection (useful for testing).
 * @returns An object containing the path and its assigned DigitalAura.
 */
export async function analyzePathForAura(
  targetPath: string,
  fs: FileSystem = fsPromises // Default to actual fsPromises for production
): Promise<{ path: string; aura: DigitalAura }> {
  const pathSegments = targetPath.split(path.sep);
  const name = pathSegments[pathSegments.length - 1];

  let detectedAura: DigitalAura = DigitalAura.MysteriousMuddle; // Default aura

  // 1. Check for direct keyword matches in the path's name
  for (const [keyword, aura] of Object.entries(keywordToAuraMap)) {
    if (name.toLowerCase().includes(keyword.toLowerCase())) {
      detectedAura = aura;
      break; // Found a strong match, prioritize it
    }
  }

  // 2. If still a 'Mysterious Muddle', try to infer from directory contents
  if (detectedAura === DigitalAura.MysteriousMuddle) {
    try {
      const stats = await fs.stat(targetPath);
      if (stats.isDirectory()) {
        const entries = await fs.readdir(targetPath);
        for (const entry of entries) {
          for (const [keyword, aura] of Object.entries(keywordToAuraMap)) {
            if (entry.toLowerCase().includes(keyword.toLowerCase())) {
              // Found a hint in contents, use this aura and stop searching
              return { path: targetPath, aura: aura };
            }
          }
        }
      }
    } catch (error) {
      // Path might not exist or permissions issue, gracefully fall back to default aura.
      // console.error(`Error accessing path ${targetPath}:`, error);
    }
  }

  return { path: targetPath, aura: detectedAura };
}
