export type CosmicFocus = 'Deep Dive' | 'Collaborative Current' | 'Reflective Ripple' | 'Chaotic Creativity' | 'Strategic Scavenge' | 'Harmonic Integration' | 'Void Exploration';

export interface CosmicGuidance {
  date: string; // YYYY-MM-DD
  focus: CosmicFocus;
  message: string;
  colorPalette: string[]; // Array of hex color codes
}
