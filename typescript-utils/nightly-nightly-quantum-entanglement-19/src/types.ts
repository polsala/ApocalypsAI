export type QuantumState = 'superposition' | 'entangled' | 'decoherence' | 'tunneling';
export type OutputFormat = 'json' | 'yaml' | 'text';

export interface EntanglementResult {
  entangled: boolean;
  coherence: number;
  entanglementStrength: number;
  quantumFluctuations: number;
  timestamp: string;
}

export interface Report {
  timestamp: string;
  nodes: number;
  quantumState: QuantumState;
  entangled: boolean;
  coherence: number;
  entanglementStrength: number;
  quantumFluctuations: number;
  recommendations: string[];
}

export interface CoherenceResult {
  verified: boolean;
  coherence: number;
  verificationTime: number;
}
