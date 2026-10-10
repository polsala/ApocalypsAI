export interface ChronoCleanerConfig {
  scanPath: string;
  staleDays: number;
  ignorePatterns: string[];
  reportFormat: 'json' | 'text';
}

export interface TemporalEcho {
  filePath: string;
  reason: 'stale' | 'deprecated-marker';
  lastModified?: Date;
  ageDays?: number;
  markerContent?: string; // e.g., the deprecated comment
}
