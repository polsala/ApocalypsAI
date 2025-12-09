import { QuantumState } from './quantum-state';

/**
 * Result of a Bell state verification test
 */
export interface BellTestResult {
  /** Correlation coefficient between measurement outcomes */
  correlation: number;
  /** Standard error of the correlation measurement */
  stdError: number;
  /** Count of measurement outcomes */
  counts: {
    '00': number;
    '01': number;
    '10': number;
    '11': number;
  };
  /** Whether the state is entangled based on correlation threshold */
  entangled: boolean;
  /** Number of measurements performed */
  measurements: number;
}

/**
 * Result of a CHSH inequality test
 */
export interface CHSHResult {
  /** CHSH parameter S = |E(a,b) - E(a,b') + E(a',b) + E(a',b')| */
  s: number;
  /** Standard error of the CHSH parameter */
  stdError: number;
  /** Classical bound: |S| ≤ 2 */
  classicalBound: number;
  /** Quantum bound: |S| ≤ 2√2 */
  quantumBound: number;
  /** Whether Bell inequality is violated */
  violatesBell: boolean;
  /** Number of trials performed */
  trials: number;
}

/**
 * Result of network entanglement simulation
 */
export interface NetworkResult {
  /** Number of network nodes */
  nodes: number;
  /** Results for each individual node */
  results: Array<{
    /** Node identifier */
    node: number;
    /** Whether the node maintains entanglement */
    entangled: boolean;
    /** Fidelity of the quantum state at this node */
    fidelity: number;
  }>;
  /** Average fidelity across all nodes */
  averageFidelity: number;
  /** Number of nodes that maintain entanglement */
  entangledNodes: number;
  /** Whether the overall network maintains entanglement */
  networkEntangled: boolean;
}

/**
 * Configuration for network simulation
 */
export interface NetworkConfig {
  /** Network latency in milliseconds */
  latency: number;
  /** Packet loss probability (0-1) */
  packetLoss: number;
  /** Number of nodes to simulate */
  nodes: number;
}

/**
 * Configuration for Bell state measurement
 */
export interface BellConfig {
  /** Number of measurements to perform */
  measurements: number;
  /** Type of Bell state to measure */
  stateType: 'phi_plus' | 'phi_minus' | 'psi_plus' | 'psi_minus';
}

/**
 * Configuration for CHSH test
 */
export interface CHSHConfig {
  /** Number of trials to perform */
  trials: number;
  /** Measurement angles in degrees */
  angles: {
    a: number;
    aPrime: number;
    b: number;
    bPrime: number;
  };
}

/**
 * Quantum measurement outcome
 */
export interface MeasurementResult {
  /** Measured state as integer */
  state: number;
  /** Probability of this outcome */
  probability: number;
  /** Binary representation of the state */
  bits: string;
}

/**
 * Quantum circuit representation
 */
export interface QuantumCircuit {
  /** Number of qubits */
  numQubits: number;
  /** Gates applied to the circuit */
  gates: Array<{
    /** Gate name */
    name: string;
    /** Target qubit(s) */
    targets: number[];
    /** Control qubit(s) */
    controls?: number[];
    /** Gate parameters */
    params?: Record<string, number>;
  }>;
}

/**
 * Simulation statistics
 */
export interface SimulationStats {
  /** Total simulation time in milliseconds */
  duration: number;
  /** Number of quantum operations performed */
  operations: number;
  /** Memory usage estimate */
  memoryUsage: {
    /** Amplitude vectors */
    amplitudes: number;
    /** Gates stored */
    gates: number;
    /** Total estimated bytes */
    totalBytes: number;
  };
  /** Random seed used for reproducibility */
  seed: number;
}
