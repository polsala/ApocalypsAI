export interface FileInfo {
    name: string;
    path: string;
    isDirectory: boolean;
    modifiedAt: Date;
    size: number;
}

export interface ScanOptions {
    ageDays: number;
    patterns: string[];
    recursive: boolean;
    dryRun: boolean;
}
