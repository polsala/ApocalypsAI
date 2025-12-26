import { QuantumState, QuantumSimulationConfig, DEFAULT_SIMULATION_CONFIG } from './types';
import { ComponentAnalysis } from './types';
import { DependencyGraph } from './dependency-graph';

export class QuantumSimulator {
  private config: QuantumSimulationConfig;

  constructor(config?: Partial<QuantumSimulationConfig>) {
    this.config = { ...DEFAULT_SIMULATION_CONFIG, ...config };
  }

  simulateStates(
    components: ComponentAnalysis[],
    dependencyGraph: DependencyGraph
  ): QuantumState[] {
    return components.map(component => {
      const quantumSignature = this.generateQuantumSignature(component);
      const coherenceLevel = this.calculateCoherence(component, dependencyGraph);
      const dependencies = this.extractDependencies(component, dependencyGraph);
      const entanglementHistory: string[] = [];

      return {
        componentName: component.name,
        dependencies,
        quantumSignature,
        coherenceLevel,
        entanglementHistory
      };
    });
  }

  private generateQuantumSignature(component: ComponentAnalysis): number[] {
    // Generate a quantum signature based on component characteristics
    const seed = this.hashString(component.name + component.filePath);
    const signature: number[] = [];

    // Create a 10-dimensional quantum state vector
    for (let i = 0; i < 10; i++) {
      const randomValue = this.pseudoRandom(seed + i);
      signature.push(randomValue);
    }

    return signature;
  }

  private calculateCoherence(
    component: ComponentAnalysis,
    dependencyGraph: DependencyGraph
  ): number {
    // Calculate quantum coherence based on component isolation
    const node = dependencyGraph.nodes.get(component.name);
    if (!node) return 1.0;

    const totalConnections = node.dependencies.length + node.dependents.length;
    const maxConnections = 20; // Normalization factor

    // Higher coherence = more isolated component
    const coherence = Math.max(0, 1 - (totalConnections / maxConnections));

    // Apply complexity penalty
    const complexityPenalty = component.complexity / 100;
    return Math.max(0, coherence - complexityPenalty);
  }

  private extractDependencies(
    component: ComponentAnalysis,
    dependencyGraph: DependencyGraph
  ): string[] {
    const node = dependencyGraph.nodes.get(component.name);
    return node ? node.dependencies : [];
  }

  calculateInterference(signature1: number[], signature2: number[]): number {
    // Calculate quantum interference between two state signatures
    let interference = 0;

    for (let i = 0; i < Math.min(signature1.length, signature2.length); i++) {
      const diff = Math.abs(signature1[i] - signature2[i]);
      interference += diff * this.config.interferenceSensitivity;
    }

    // Normalize interference to 0-1 range
    return Math.min(1, interference / 10);
  }

  simulateEntanglementDecay(
    quantumStates: QuantumState[],
    timeSteps: number
  ): QuantumState[] {
    return quantumStates.map(state => {
      const decayedCoherence = Math.max(
        0,
        state.coherenceLevel - (this.config.coherenceDecayRate * timeSteps)
      );

      return {
        ...state,
        coherenceLevel: decayedCoherence,
        entanglementHistory: [...state.entanglementHistory, `t=${timeSteps}`]
      };
    });
  }

  // Helper methods for quantum simulation
  private hashString(str: string): number {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash; // Convert to 32-bit integer
    }
    return Math.abs(hash);
  }

  private pseudoRandom(seed: number): number {
    // Simple pseudo-random number generator
    let x = Math.sin(seed) * 10000;
    return x - Math.floor(x);
  }
}
