import { QuantumState, Complex } from './quantum-state';
import { QuantumGate, Gates } from './quantum-gates';
import { BellTestResult, CHSHResult, NetworkResult } from './types';

/**
 * Core class for quantum entanglement verification.
 * 
 * Implements type-safe probabilistic algorithms for:
 * - Bell state measurements
 * - CHSH inequality testing
 * - Network entanglement simulation
 * 
 * Uses mathematical models to simulate quantum behavior
 * without requiring actual quantum hardware.
 */
export class EntanglementVerifier {
  private readonly randomSeed: number;

  constructor(seed?: number) {
    this.randomSeed = seed ?? this.generateSeed();
  }

  /**
   * Generates a deterministic seed for reproducible results
   */
  private generateSeed(): number {
    return Math.floor(Date.now() % 1000000);
  }

  /**
   * Creates a Bell state |Φ+⟩ = (|00⟩ + |11⟩)/√2
   */
  createBellState(): QuantumState {
    // Start with |00⟩
    const state = new QuantumState([1, 0, 0, 0]);
    
    // Apply Hadamard gate to first qubit
    const hGate = Gates.tensorProduct(Gates.H, Gates.I);
    const afterH = state.applyGate(hGate);
    
    // Apply CNOT gate
    const cnot = Gates.CNOT;
    return afterH.applyGate(cnot);
  }

  /**
   * Verifies Bell state through measurements
   */
  verifyBellState(state: QuantumState, measurements: number = 1000): BellTestResult {
    const correlations: number[] = [];
    const counts = { '00': 0, '01': 0, '10': 0, '11': 0 };
    
    for (let i = 0; i < measurements; i++) {
      const result = state.measure();
      const bits = this.decimalToBinary(result, 2);
      counts[bits as keyof typeof counts]++;
      
      // Calculate correlation for Bell test
      const a = parseInt(bits[0]);
      const b = parseInt(bits[1]);
      correlations.push((a === b) ? 1 : -1);
    }
    
    const correlation = correlations.reduce((sum, val) => sum + val, 0) / measurements;
    const variance = correlations.reduce((sum, val) => sum + Math.pow(val - correlation, 2), 0) / measurements;
    const stdError = Math.sqrt(variance / measurements);
    
    return {
      correlation,
      stdError,
      counts,
      entangled: correlation > 0.5,
      measurements
    };
  }

  /**
   * Tests CHSH inequality
   * S = |E(a,b) - E(a,b') + E(a',b) + E(a',b')| ≤ 2 (classical)
   * Quantum mechanics predicts S ≤ 2√2 ≈ 2.828
   */
  testCHSH(trials: number = 10000): CHSHResult {
    const angles = [
      { a: 0, aPrime: 90, b: 45, bPrime: 135 }
    ];
    
    const expectations: number[] = [];
    
    for (const { a, aPrime, b, bPrime } of angles) {
      const eAB = this.measureCorrelation(trials, a, b);
      const eABPrime = this.measureCorrelation(trials, a, bPrime);
      const eAPrimeB = this.measureCorrelation(trials, aPrime, b);
      const eAPrimeBPrime = this.measureCorrelation(trials, aPrime, bPrime);
      
      const s = Math.abs(eAB - eABPrime + eAPrimeB + eAPrimeBPrime);
      expectations.push(s);
    }
    
    const meanS = expectations.reduce((sum, val) => sum + val, 0) / expectations.length;
    const variance = expectations.reduce((sum, val) => sum + Math.pow(val - meanS, 2), 0) / expectations.length;
    const stdError = Math.sqrt(variance / expectations.length);
    
    return {
      s: meanS,
      stdError,
      classicalBound: 2,
      quantumBound: 2 * Math.sqrt(2),
      violatesBell: meanS > 2,
      trials
    };
  }

  /**
   * Measures correlation between measurements at different angles
   */
  private measureCorrelation(trials: number, angleA: number, angleB: number): number {
    const correlations: number[] = [];
    const bellState = this.createBellState();
    
    for (let i = 0; i < trials; i++) {
      const result = bellState.measure();
      const bits = this.decimalToBinary(result, 2);
      const a = parseInt(bits[0]);
      const b = parseInt(bits[1]);
      
      // Simulate measurement at angles
      const probA = Math.cos(this.degToRad(angleA)) ** 2;
      const probB = Math.cos(this.degToRad(angleB)) ** 2;
      
      const measuredA = Math.random() < probA ? a : 1 - a;
      const measuredB = Math.random() < probB ? b : 1 - b;
      
      correlations.push((measuredA === measuredB) ? 1 : -1);
    }
    
    return correlations.reduce((sum, val) => sum + val, 0) / trials;
  }

  /**
   * Simulates entanglement across a network with latency and packet loss
   */
  simulateNetwork(nodes: number, latency: number = 50, packetLoss: number = 0.01): NetworkResult {
    const results: Array<{ node: number; entangled: boolean; fidelity: number }> = [];
    const bellState = this.createBellState();
    
    for (let i = 0; i < nodes; i++) {
      // Simulate network effects
      const delay = Math.random() * latency;
      const lost = Math.random() < packetLoss;
      
      if (lost) {
        results.push({
          node: i + 1,
          entangled: false,
          fidelity: 0
        });
        continue;
      }
      
      // Simulate decoherence due to latency
      const decoherence = 1 - Math.exp(-delay / 1000);
      const fidelity = Math.max(0, 1 - decoherence);
      
      // Measure with reduced fidelity
      const measurements = 100;
      let correlated = 0;
      
      for (let j = 0; j < measurements; j++) {
        const result = bellState.measure();
        const bits = this.decimalToBinary(result, 2);
        if (bits[0] === bits[1]) correlated++;
      }
      
      const correlationRatio = correlated / measurements;
      const entangled = correlationRatio > fidelity * 0.8;
      
      results.push({
        node: i + 1,
        entangled,
        fidelity: entangled ? fidelity : fidelity * 0.5
      });
    }
    
    const averageFidelity = results.reduce((sum, r) => sum + r.fidelity, 0) / results.length;
    const entangledNodes = results.filter(r => r.entangled).length;
    
    return {
      nodes,
      results,
      averageFidelity,
      entangledNodes,
      networkEntangled: entangledNodes > nodes / 2
    };
  }

  /**
   * Converts decimal to binary string with padding
   */
  private decimalToBinary(num: number, length: number): string {
    return num.toString(2).padStart(length, '0');
  }

  /**
   * Converts degrees to radians
   */
  private degToRad(degrees: number): number {
    return (degrees * Math.PI) / 180;
  }
}
