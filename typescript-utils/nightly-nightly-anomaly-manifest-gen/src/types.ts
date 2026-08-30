/**
 * Defines the possible severity levels for an anomaly.
 */
export type AnomalySeverity = "Minor" | "Moderate" | "Severe" | "Critical" | "Unknown";

/**
 * Defines the possible categories for an anomaly.
 */
export type AnomalyCategory = "Temporal Distortion" | "Reality Glitch" | "Spatial Displacement" | "Energy Fluctuation" | "Biological Mutation" | "Unknown";

/**
 * Represents the raw input data for an anomaly observation.
 */
export interface AnomalyInput {
  description: string;
  location?: string;
  observedBy?: string;
}

/**
 * Represents a fully classified and structured anomaly manifest entry.
 */
export interface AnomalyManifestEntry {
  id: string;
  timestamp: string; // ISO 8601 format
  description: string;
  location?: string;
  observedBy?: string;
  category: AnomalyCategory;
  severity: AnomalySeverity;
  notes?: string;
}
