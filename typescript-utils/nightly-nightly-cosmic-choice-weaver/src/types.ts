export interface Choice {
  id: string;
  name: string;
  description?: string;
  tags?: string[];
  weight?: number; // Base weight for selection
}

export interface CosmicInfluence {
  tag: string;
  multiplier: number; // Multiplier for choices with this tag
}

export interface WeaverConfig {
  choices: Choice[];
  influences?: CosmicInfluence[];
  seed?: string; // For deterministic randomness
}
