export interface EntanglementReport {
  nodeA: string;
  nodeB: string;
  distance: number;
  quantumState: string;
  entanglementFidelity: number;
  bellInequalityViolation: number;
  correlationCoefficient: number;
  isEntangled: boolean;
  recommendation: string;
}

export type QuantumState = 'entangled' | 'separated' | 'superposition';

export interface QuantumMetrics {
  fidelity: number;
  bellViolation: number;
  correlation: number;
  decoherenceRate: number;
}

export interface NodeConfiguration {
  nodeId: string;
  location: string;
  quantumCapability: 'basic' | 'advanced' | 'experimental';
  maxDistance: number;
}
