export enum RelicCategory {
  AncientRelic = 'Ancient Relic',
  ForgottenArtifact = 'Forgotten Artifact',
  RecentFind = 'Recent Find',
  ActiveData = 'Active Data',
}

export interface FileMetadata {
  path: string;
  size: number; // in bytes
  createdAt: Date;
  modifiedAt: Date;
  accessedAt: Date;
  isDirectory: boolean;
}

export interface RelicConfig {
  ancientDays: number; // Files older than this are Ancient Relics
  forgottenDays: number; // Files older than this (but newer than ancientDays) are Forgotten Artifacts
  minSizeKB: number; // Minimum size in KB for a file to be considered
}

export interface RelicReportEntry {
  path: string;
  category: RelicCategory;
  reason: string[];
}

/**
 * Classifies a single file based on its metadata and the provided relic configuration.
 * @param metadata The file's metadata.
 * @param config The configuration for relic classification.
 * @returns An object containing the relic category and reasons for classification.
 */
export function classifyFile(metadata: FileMetadata, config: RelicConfig): RelicReportEntry {
  const now = new Date();
  const ageDays = Math.floor((now.getTime() - metadata.createdAt.getTime()) / (1000 * 60 * 60 * 24));
  const modifiedDaysAgo = Math.floor((now.getTime() - metadata.modifiedAt.getTime()) / (1000 * 60 * 60 * 24));
  const accessedDaysAgo = Math.floor((now.getTime() - metadata.accessedAt.getTime()) / (1000 * 60 * 60 * 24));

  const reasons: string[] = [];

  if (metadata.isDirectory) {
    return { path: metadata.path, category: RelicCategory.ActiveData, reason: ['Is a directory, not classified as a relic.'] };
  }

  if (metadata.size < config.minSizeKB * 1024) {
    return { path: metadata.path, category: RelicCategory.ActiveData, reason: [`File size (${(metadata.size / 1024).toFixed(2)} KB) is below minimum threshold (${config.minSizeKB} KB).`] };
  }

  // Ancient Relic: Very old and untouched
  if (ageDays >= config.ancientDays && modifiedDaysAgo >= config.ancientDays && accessedDaysAgo >= config.ancientDays) {
    reasons.push(`File is very old (${ageDays} days) and has not been modified or accessed recently.`);
    return { path: metadata.path, category: RelicCategory.AncientRelic, reason: reasons };
  }

  // Forgotten Artifact: Old but perhaps recently accessed or modified (but still old overall)
  // This category applies if the file is older than forgottenDays, but not necessarily ancient, and has not been recently active.
  if (ageDays >= config.forgottenDays && (modifiedDaysAgo >= config.forgottenDays || accessedDaysAgo >= config.forgottenDays)) {
    reasons.push(`File is old (${ageDays} days) but not ancient, and has not been modified or accessed recently.`);
    return { path: metadata.path, category: RelicCategory.ForgottenArtifact, reason: reasons };
  }

  // Recent Find: Relatively new but not actively used (e.g., not modified/accessed in last 30 days)
  // This applies to files newer than forgottenDays, but still showing some inactivity.
  if (ageDays < config.forgottenDays && (modifiedDaysAgo >= 30 || accessedDaysAgo >= 30)) { // Arbitrary 30 days for 'not actively used'
    reasons.push(`File is relatively new (${ageDays} days) but has not been actively modified or accessed in the last 30 days.`);
    return { path: metadata.path, category: RelicCategory.RecentFind, reason: reasons };
  }

  // Active Data: Recently modified or accessed
  reasons.push(`File is recent (${ageDays} days) and actively used.`);
  return { path: metadata.path, category: RelicCategory.ActiveData, reason: reasons };
}
