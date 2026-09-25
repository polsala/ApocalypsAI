export interface FileMetadata {
  path: string;
  name: string;
  isDirectory: boolean;
  lastModifiedMs: number;
  ageDays: number;
  dustScore: number;
  suggestion: string;
}

export interface DustBunnyConfig {
  targetDir: string;
  ageThresholdDays: number;
  dustPatterns: string[]; // Substring patterns to match in filenames
  recursive: boolean;
  outputFormat: 'json' | 'text';
  minDustScore: number;
}
