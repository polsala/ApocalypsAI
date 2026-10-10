export interface ScanOptions {
  path: string;
  minAgeDays: number;
  ignorePatterns: string[];
  includePatterns: string[];
}

export interface ResidueItem {
  path: string;
  type: 'file' | 'directory';
  lastModified: Date;
  reason: string;
}
