export enum CosmicAlignment {
  StellarConvergence = "Stellar Convergence",
  NebulaDrift = "Nebula Drift",
  VoidResonance = "Void Resonance",
  TemporalFlux = "Temporal Flux",
  GalacticHarmony = "Galactic Harmony",
  QuantumEntanglement = "Quantum Entanglement"
}

export interface CosmicEntity {
  id: string; // Unique identifier for the entity
  name: string; // Display name or path
  type: 'file' | 'task' | 'tab';
  lastModified?: Date; // For files, or creation date for tasks/tabs
  sizeBytes?: number; // For files, or conceptual 'weight' for tasks/tabs
  keywords?: string[]; // For tasks/tabs, to influence priority
  priority?: number; // 1 (high) to 5 (low), if applicable
}

export interface AlignedEntity {
  entity: CosmicEntity;
  alignment: CosmicAlignment;
  score: number;
  recommendation: string;
}
