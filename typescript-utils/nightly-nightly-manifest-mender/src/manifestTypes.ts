export interface ManifestItem {
  name: string;
  quantity: number;
  category?: string;
  tags?: string[];
  expiryDate?: string; // ISO 8601 date string
}

export interface Manifest {
  items: ManifestItem[];
  location?: string;
  lastUpdated?: string; // ISO 8601 date-time string
}

export type MendingSeverity = 'critical' | 'warning' | 'info';

export interface MendingSuggestion {
  type: 'add' | 'remove' | 'adjust' | 'rename' | 'info' | 'consolidate';
  item?: string; // Name of the item related to the suggestion
  suggestion: string;
  rationale: string;
  severity: MendingSeverity;
}
