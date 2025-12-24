import { EntanglementReport, QuantumState } from './types';

export class QuantumEntanglementSimulator {
  private readonly MAX_DISTANCE_KM = 10000;
  private readonly BASE_FIDELITY = 0.99;
  private readonly NOISE_FACTOR = 0.0001;

  /**
   * Check entanglement between two nodes
   */
  checkEntanglement(nodeA: string, nodeB: string, distance: number): EntanglementReport {
    // Generate random quantum state
    const quantumState = this.generateBellState();
    
    // Calculate entanglement metrics based on distance
    const distanceFactor = Math.min(distance / this.MAX_DISTANCE_KM, 1);
    const noiseLevel = distanceFactor * this.NOISE_FACTOR * distance;
    
    // Calculate entanglement fidelity (degrades with distance)
    const entanglementFidelity = Math.max(
      0,
      this.BASE_FIDELITY - (distanceFactor * 0.2) - noiseLevel
    );
    
    // Calculate Bell inequality violation (should be > 2 for entanglement)
    const bellInequalityViolation = 2 + (entanglementFidelity * 1.5);
    
    // Calculate correlation coefficient
    const correlationCoefficient = entanglementFidelity * 0.95;
    
    // Determine if entangled
    const isEntangled = entanglementFidelity > 0.5 && bellInequalityViolation > 2;
    
    // Generate recommendation
    const recommendation = this.generateRecommendation(
      entanglementFidelity,
      bellInequalityViolation,
      distance
    );

    return {
      nodeA,
      nodeB,
      distance,
      quantumState,
      entanglementFidelity,
      bellInequalityViolation,
      correlationCoefficient,
      isEntangled,
      recommendation
    };
  }

  /**
   * Generate correlation report for multiple nodes
   */
  generateCorrelationReport(nodes: string[]): EntanglementReport[] {
    const reports: EntanglementReport[] = [];
    
    // Generate reports for all node pairs
    for (let i = 0; i < nodes.length; i++) {
      for (let j = i + 1; j < nodes.length; j++) {
        const distance = this.calculateDistance(nodes[i], nodes[j]);
        const report = this.checkEntanglement(nodes[i], nodes[j], distance);
        reports.push(report);
      }
    }
    
    return reports;
  }

  /**
   * Verify if a quantum state is a valid Bell state
   */
  verifyBellState(state: string): boolean {
    // Mock Bell state patterns
    const bellPatterns = [
      '|00⟩ + |11⟩',
      '|00⟩ - |11⟩',
      '|01⟩ + |10⟩',
      '|01⟩ - |10⟩'
    ];
    
    return bellPatterns.includes(state.trim());
  }

  /**
   * Calculate state fidelity for a given quantum state
   */
  calculateStateFidelity(state: string): number {
    if (this.verifyBellState(state)) {
      // High fidelity for valid Bell states
      return 0.95 + Math.random() * 0.05;
    } else {
      // Lower fidelity for invalid states
      return 0.3 + Math.random() * 0.4;
    }
  }

  /**
   * Generate a random Bell state
   */
  private generateBellState(): string {
    const states = ['|00⟩ + |11⟩', '|00⟩ - |11⟩', '|01⟩ + |10⟩', '|01⟩ - |10⟩'];
    return states[Math.floor(Math.random() * states.length)];
  }

  /**
   * Calculate mock distance between nodes based on their names
   */
  private calculateDistance(nodeA: string, nodeB: string): number {
    // Mock distance calculation based on node names
    const hashA = this.hashString(nodeA);
    const hashB = this.hashString(nodeB);
    const distance = Math.abs(hashA - hashB) % 5000;
    return distance;
  }

  /**
   * Generate recommendation based on entanglement metrics
   */
  private generateRecommendation(
    fidelity: number,
    bellViolation: number,
    distance: number
  ): string {
    if (fidelity > 0.8 && bellViolation > 2.5) {
      return 'Quantum link stable for distributed operations';
    } else if (fidelity > 0.5 && bellViolation > 2.0) {
      return 'Quantum link acceptable with minor corrections recommended';
    } else if (distance > 8000) {
      return 'Distance too great for reliable entanglement; consider quantum repeaters';
    } else {
      return 'Quantum link unstable; requires recalibration';
    }
  }

  /**
   * Simple string hash function for mock distance calculation
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
}
