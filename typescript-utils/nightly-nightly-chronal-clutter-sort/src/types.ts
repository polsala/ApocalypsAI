export interface Anomaly {
  id: string;
  description: string;
  timestamp: string; // ISO 8601 string
  tags: string[];
}

export interface Rule {
  pattern: string; // Regex pattern for description matching
  category: string;
  priority: string;
}

export interface PrioritizedAnomaly extends Anomaly {
  priority: string;
  category: string; // Add category to the anomaly itself for easier grouping
}

export interface CategorizedAnomalies {
  [category: string]: PrioritizedAnomaly[];
}
