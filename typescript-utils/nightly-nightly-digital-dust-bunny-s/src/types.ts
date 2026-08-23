export interface FileInfo {
  path: string;
  name: string;
  size: number; // in bytes
  mtimeMs: number; // last modified time in milliseconds since epoch
  ageDays: number;
}

export interface DustBunnyReport {
  totalFilesScanned: number;
  totalDustBunniesFound: number;
  dustBunnies: FileInfo[];
}
