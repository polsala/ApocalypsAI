export interface FileInfo {
  path: string;
  name: string;
  isDir: boolean;
  lastModified: Date;
  ageDays: number;
}

export interface DustBunnyReport {
  scannedPath: string;
  thresholdDays: number;
  ignoredPatterns: string[];
  dustBunnyCount: number;
  dustBunnyFiles: FileInfo[];
}

export interface Config {
  path: string;
  thresholdDays: number;
  ignorePatterns: string[];
  outputFormat: 'json' | 'text';
}
