export interface Regret {
  id: string;
  description: string;
  timestamp: string; // ISO 8601 string
  resolvedAt?: string; // ISO 8601 string
}

export interface RegretData {
  active: Regret[];
  resolved: Regret[];
}
