export type DistortionLevel = 'low' | 'medium' | 'high' | 'critical';
export type Urgency = 'low' | 'medium' | 'high' | 'immediate';

export interface ChronoShard {
  id: string; // Unique identifier for the shard
  timestamp: string; // ISO 8601 string (e.g., '2023-10-26T14:30:00Z')
  event: string; // Description of the temporal event
  distortionLevel: DistortionLevel; // Severity of temporal distortion
  urgency: Urgency; // Priority for immediate action
  tags: string[]; // Categorization tags (e.g., 'system', 'anomaly', 'resource')
}

// Defines the order for sorting DistortionLevel
export const distortionLevelOrder: Record<DistortionLevel, number> = {
  'low': 0,
  'medium': 1,
  'high': 2,
  'critical': 3
};

// Defines the order for sorting Urgency
export const urgencyOrder: Record<Urgency, number> = {
  'low': 0,
  'medium': 1,
  'high': 2,
  'immediate': 3
};
