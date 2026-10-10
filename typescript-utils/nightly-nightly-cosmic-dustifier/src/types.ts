export type DustificationAction = 'list' | 'archive' | 'delete';

export interface DustificationOptions {
  path: string;
  thresholdDays: number;
  action: DustificationAction;
  archiveDir?: string;
  dryRun: boolean;
}

export interface FileInfo {
  path: string;
  name: string;
  birthtimeMs: number;
  mtimeMs: number;
  ageDays: number;
}
