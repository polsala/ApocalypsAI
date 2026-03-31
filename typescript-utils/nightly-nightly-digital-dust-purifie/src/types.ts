export interface PurifierConfig {
  targetPath: string;
  minAgeDays: number; // Files older than this will be flagged
  minSizeBytes: number; // Files larger than this will be flagged
  excludePatterns: string[]; // Glob patterns or regex for files/dirs to ignore
  dryRun: boolean;
  archiveDir?: string; // Directory to move files to if not dry-run
}

export interface DustBunnyReportItem {
  filePath: string;
  reason: string; // e.g., "Older than 90 days", "Larger than 10MB"
  size: number; // in bytes
  lastModified: Date;
}
