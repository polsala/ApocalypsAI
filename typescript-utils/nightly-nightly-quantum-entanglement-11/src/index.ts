import { QuantumState, EntanglementResult, VerificationOptions } from './types';

/**
 * Quantum Entanglement Checker
 * 
 * Simulates quantum entanglement verification for distributed systems.
 * Uses pseudo-random quantum state generation with deterministic outcomes
 * for testing and verification purposes.
 */
export class QuantumEntanglementChecker {
  private readonly MAX_DISTANCE_KM = 10000;
  private readonly DECAY_FACTOR = 0.0001;
  
  /**
   * Verify entanglement between two nodes
   */
  async verifyEntanglement(options: VerificationOptions): Promise<EntanglementResult> {
    const { nodeA, nodeB, distance, timestamp } = options;
    
    // Validate inputs
    if (!nodeA || !nodeB) {
      throw new Error('Both nodeA and nodeB must be specified');
    }
    
    if (distance < 0 || distance > this.MAX_DISTANCE_KM) {
      throw new Error(`Distance must be between 0 and ${this.MAX_DISTANCE_KM} km`);
    }
    
    // Generate quantum states for both nodes
    const stateA = this.generateQuantumState(nodeA, timestamp);
    const stateB = this.generateQuantumState(nodeB, timestamp);
    
    // Calculate entanglement probability based on distance
    const baseProbability = 0.95;
    const distanceDecay = Math.min(distance * this.DECAY_FACTOR, 0.5);
    const entanglementProbability = Math.max(baseProbability - distanceDecay, 0.1);
    
    // Determine if nodes are entangled
    const isEntangled = this.calculateEntanglement(stateA, stateB, entanglementProbability);
    
    // Calculate coherence score
    const coherenceScore = this.calculateCoherence(stateA, stateB, distance);
    
    return {
      nodeA,
      nodeB,
      distance,
      timestamp,
      entangled: isEntangled,
      coherenceScore,
      quantumStateA: stateA,
      quantumStateB: stateB,
      entanglementProbability,
      measurementTimestamp: Date.now()
    };
  }
  
  /**
   * Generate a quantum state for a given node and timestamp
   */
  private generateQuantumState(nodeId: string, timestamp: number): QuantumState {
    // Create a deterministic seed based on node ID and timestamp
    const seed = this.hashString(`${nodeId}-${timestamp}`);
    
    return {
      spin: this.randomFromSeed(seed, 0, 1) > 0.5 ? 'up' : 'down',
      phase: this.randomFromSeed(seed, 1, 1),
      amplitude: this.randomFromSeed(seed, 2, 0.5, 1.5),
      coherence: this.randomFromSeed(seed, 3, 0.7, 1.0),
      timestamp,
      nodeId
    };
  }
  
  /**
   * Calculate if two quantum states are entangled
   */
  private calculateEntanglement(stateA: QuantumState, stateB: QuantumState, probability: number): boolean {
    // States are more likely to be entangled if they have opposite spins
    const spinCorrelation = stateA.spin !== stateB.spin ? 0.3 : 0;
    
    // Higher coherence increases entanglement probability
    const coherenceBoost = (stateA.coherence + stateB.coherence) / 2 * 0.2;
    
    // Phase alignment affects entanglement
    const phaseDifference = Math.abs(stateA.phase - stateB.phase);
    const phaseAlignment = Math.cos(phaseDifference * Math.PI) * 0.1;
    
    const adjustedProbability = Math.min(
      probability + spinCorrelation + coherenceBoost + phaseAlignment,
      0.99
    );
    
    return Math.random() < adjustedProbability;
  }
  
  /**
   * Calculate coherence score between two quantum states
   */
  private calculateCoherence(stateA: QuantumState, stateB: QuantumState, distance: number): number {
    // Base coherence from individual states
    const baseCoherence = (stateA.coherence + stateB.coherence) / 2;
    
    // Distance affects coherence
    const distanceFactor = Math.max(0, 1 - (distance / this.MAX_DISTANCE_KM));
    
    // Phase alignment affects coherence
    const phaseDifference = Math.abs(stateA.phase - stateB.phase);
    const phaseCoherence = 1 - (phaseDifference * 0.5);
    
    // Spin correlation affects coherence
    const spinCoherence = stateA.spin === stateB.spin ? 0.8 : 1.0;
    
    const finalCoherence = (
      baseCoherence * 0.4 +
      distanceFactor * 0.3 +
      phaseCoherence * 0.2 +
      spinCoherence * 0.1
    );
    
    return Math.max(0, Math.min(1, finalCoherence));
  }
  
  /**
   * Generate a hash from a string
   */
  private hashString(str: string): number {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash; // Convert to 32-bit integer
    }
    return Math.abs(hash);
  }
  
  /**
   * Generate a pseudo-random number from a seed
   */
  private randomFromSeed(seed: number, offset: number, min: number = 0, max: number = 1): number {
    // Simple pseudo-random number generator using seed
    let x = Math.sin(seed * (offset + 1)) * 10000;
    x = x - Math.floor(x);
    return x * (max - min) + min;
  }
  
  /**
   * Generate a report for multiple entanglement verifications
   */
  async generateReport(nodePairs: Array<{nodeA: string, nodeB: string, distance: number}>): Promise<string> {
    const results = await Promise.all(
      nodePairs.map(async pair => {
        const result = await this.verifyEntanglement({
          ...pair,
          timestamp: Date.now()
        });
        return result;
      })
    );
    
    let report = '# Quantum Entanglement Verification Report\n\n';
    report += `Generated at: ${new Date().toISOString()}\n\n`;
    
    let entangledCount = 0;
    let totalCoherence = 0;
    
    results.forEach((result, index) => {
      report += `## Pair ${index + 1}: ${result.nodeA} ↔ ${result.nodeB}\n`;
      report += `- Distance: ${result.distance} km\n`;
      report += `- Entangled: ${result.entangled ? '✓ YES' : '✗ NO'}\n`;
      report += `- Coherence Score: ${(result.coherenceScore * 100).toFixed(1)}%\n`;
      report += `- Quantum States: ${result.quantumStateA.spin}/${result.quantumStateB.spin}\n`;
      report += `- Entanglement Probability: ${(result.entanglementProbability * 100).toFixed(1)}%\n\n`;
      
      if (result.entangled) entangledCount++;
      totalCoherence += result.coherenceScore;
    });
    
    const avgCoherence = totalCoherence / results.length;
    const successRate = (entangledCount / results.length) * 100;
    
    report += '## Summary\n';
    report += `- Total Pairs: ${results.length}\n`;
    report += `- Entangled Pairs: ${entangledCount}\n`;
    report += `- Success Rate: ${successRate.toFixed(1)}%\n`;
    report += `- Average Coherence: ${(avgCoherence * 100).toFixed(1)}%\n`;
    
    return report;
  }
}

// Export default instance for convenience
export default new QuantumEntanglementChecker();
