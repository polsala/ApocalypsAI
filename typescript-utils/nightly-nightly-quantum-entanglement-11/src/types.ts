export interface QuantumState {
  spin: 'up' | 'down';
  phase: number;
  amplitude: number;
  coherence: number;
  timestamp: number;
  nodeId: string;
}

export interface EntanglementResult {
  nodeA: string;
  nodeB: string;
  distance: number;
  timestamp: number;
  entangled: boolean;
  coherenceScore: number;
  quantumStateA: QuantumState;
  quantumStateB: QuantumState;
  entanglementProbability: number;
  measurementTimestamp: number;
}

export interface VerificationOptions {
  nodeA: string;
  nodeB: string;
  distance: number;
  timestamp: number;
}
