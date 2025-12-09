export interface EntanglementResult {
  nodeA: string;
  nodeB: string;
  entanglementProbability: number;
  quantumState: 'Coherent' | 'Decoherent' | 'Superposition';
  superpositionStatus: 'Stable' | 'Unstable' | 'Collapsing';
  timestamp: Date;
  quantumSignature: string;
}

export interface SystemCheckResult {
  nodes: string[];
  totalPairs: number;
  entangledPairs: number;
  averageProbability: number;
  systemStatus: 'Quantumly Stable' | 'Partially Entangled' | 'Quantumly Isolated';
  timestamp: Date;
  entanglementMatrix: EntanglementResult[];
}

class QuantumEntanglementChecker {
  private readonly QUANTUM_SEED: number = 42;
  private readonly MAX_ENTANGLEMENT_PROBABILITY: number = 99.9;
  private readonly MIN_ENTANGLEMENT_PROBABILITY: number = 10.0;

  /**
   * Checks the quantum entanglement between two nodes
   * @param nodeA First node identifier
   * @param nodeB Second node identifier
   * @returns EntanglementResult with quantum state information
   */
  public checkEntanglement(nodeA: string, nodeB: string): EntanglementResult {
    if (!nodeA || !nodeB) {
      throw new Error('Both node identifiers must be provided');
    }

    if (nodeA === nodeB) {
      throw new Error('Cannot check entanglement with the same node');
    }

    const probability = this.calculateEntanglementProbability(nodeA, nodeB);
    const quantumState = this.determineQuantumState(probability);
    const superpositionStatus = this.determineSuperpositionStatus(probability);
    const quantumSignature = this.generateQuantumSignature(nodeA, nodeB, probability);

    return {
      nodeA,
      nodeB,
      entanglementProbability: probability,
      quantumState,
      superpositionStatus,
      timestamp: new Date(),
      quantumSignature,
    };
  }

  /**
   * Runs a comprehensive entanglement check across all provided nodes
   * @param nodes Array of node identifiers
   * @returns SystemCheckResult with overall system quantum state
   */
  public runSystemCheck(nodes: string[]): SystemCheckResult {
    if (!nodes || nodes.length < 2) {
      throw new Error('At least 2 nodes are required for system check');
    }

    const uniqueNodes = [...new Set(nodes)];
    if (uniqueNodes.length < 2) {
      throw new Error('At least 2 unique nodes are required for system check');
    }

    const entanglementMatrix: EntanglementResult[] = [];
    let entangledPairs = 0;
    let totalProbability = 0;

    // Check all possible pairs
    for (let i = 0; i < uniqueNodes.length; i++) {
      for (let j = i + 1; j < uniqueNodes.length; j++) {
        const result = this.checkEntanglement(uniqueNodes[i], uniqueNodes[j]);
        entanglementMatrix.push(result);
        totalProbability += result.entanglementProbability;
        
        if (result.quantumState === 'Coherent') {
          entangledPairs++;
        }
      }
    }

    const totalPairs = entanglementMatrix.length;
    const averageProbability = totalProbability / totalPairs;
    const systemStatus = this.determineSystemStatus(entangledPairs, totalPairs);

    return {
      nodes: uniqueNodes,
      totalPairs,
      entangledPairs,
      averageProbability,
      systemStatus,
      timestamp: new Date(),
      entanglementMatrix,
    };
  }

  /**
   * Calculates entanglement probability based on node characteristics
   * @private
   */
  private calculateEntanglementProbability(nodeA: string, nodeB: string): number {
    // Create a deterministic hash based on node names
    const hash = this.hashNodes(nodeA, nodeB);
    
    // Apply quantum wave function simulation
    const waveComponent = Math.sin(hash / 100) * Math.cos(hash / 75);
    const probability = Math.abs(waveComponent) * 100;
    
    // Ensure bounds and add quantum fluctuation
    const baseProbability = this.clamp(
      probability, 
      this.MIN_ENTANGLEMENT_PROBABILITY, 
      this.MAX_ENTANGLEMENT_PROBABILITY
    );
    
    const quantumFluctuation = (Math.random() - 0.5) * 5; // ±2.5%
    return this.round(this.clamp(
      baseProbability + quantumFluctuation,
      this.MIN_ENTANGLEMENT_PROBABILITY,
      this.MAX_ENTANGLEMENT_PROBABILITY
    ), 1);
  }

  /**
   * Determines quantum state based on probability
   * @private
   */
  private determineQuantumState(probability: number): 'Coherent' | 'Decoherent' | 'Superposition' {
    if (probability >= 75) return 'Coherent';
    if (probability >= 40) return 'Superposition';
    return 'Decoherent';
  }

  /**
   * Determines superposition status based on probability
   * @private
   */
  private determineSuperpositionStatus(probability: number): 'Stable' | 'Unstable' | 'Collapsing' {
    if (probability >= 80) return 'Stable';
    if (probability >= 50) return 'Collapsing';
    return 'Unstable';
  }

  /**
   * Generates a unique quantum signature for the entanglement
   * @private
   */
  private generateQuantumSignature(nodeA: string, nodeB: string, probability: number): string {
    const hash = this.hashNodes(nodeA, nodeB);
    const timestamp = Date.now();
    const signature = `${hash.toString(16)}-${timestamp.toString(16)}-${probability.toString(16)}`;
    return signature.toUpperCase();
  }

  /**
   * Creates a deterministic hash from two node names
   * @private
   */
  private hashNodes(nodeA: string, nodeB: string): number {
    const combined = `${nodeA}:${nodeB}:${this.QUANTUM_SEED}`;
    let hash = 0;
    
    for (let i = 0; i < combined.length; i++) {
      const char = combined.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash; // Convert to 32-bit integer
    }
    
    return Math.abs(hash);
  }

  /**
   * Determines overall system status
   * @private
   */
  private determineSystemStatus(entangledPairs: number, totalPairs: number): 'Quantumly Stable' | 'Partially Entangled' | 'Quantumly Isolated' {
    const ratio = entangledPairs / totalPairs;
    
    if (ratio >= 0.7) return 'Quantumly Stable';
    if (ratio >= 0.3) return 'Partially Entangled';
    return 'Quantumly Isolated';
  }

  /**
   * Utility function to clamp a value between min and max
   * @private
   */
  private clamp(value: number, min: number, max: number): number {
    return Math.max(min, Math.min(max, value));
  }

  /**
   * Utility function to round to specified decimal places
   * @private
   */
  private round(value: number, decimals: number): number {
    const factor = Math.pow(10, decimals);
    return Math.round(value * factor) / factor;
  }
}

export { QuantumEntanglementChecker };

// Convenience function for easy usage
export function createQuantumChecker(): QuantumEntanglementChecker {
  return new QuantumEntanglementChecker();
}
