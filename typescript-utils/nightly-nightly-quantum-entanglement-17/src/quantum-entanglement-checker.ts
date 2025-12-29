export interface QuantumParticle {
  id: string;
  nodeId: string;
  spin: 'up' | 'down';
  entangledWith?: string;
  timestamp: number;
}

export interface EntanglementResult {
  isEntangled: boolean;
  correlation: number;
  spookyAction: boolean;
  measurementTime: number;
}

export class QuantumEntanglementChecker {
  private particles: Map<string, QuantumParticle> = new Map();
  private readonly MAX_CORRELATION = 0.95;
  private readonly MIN_CORRELATION = 0.8;

  /**
   * Creates a pair of entangled quantum particles
   * @param node1 First node identifier
   * @param node2 Second node identifier
   * @returns Object containing the entangled particle pair
   */
  createEntangledPair(node1: string, node2: string): {
    particle1: QuantumParticle;
    particle2: QuantumParticle;
  } {
    const spin = this.randomSpin();
    const antiSpin = spin === 'up' ? 'down' : 'up';

    const particle1: QuantumParticle = {
      id: this.generateId(),
      nodeId: node1,
      spin: spin,
      timestamp: Date.now()
    };

    const particle2: QuantumParticle = {
      id: this.generateId(),
      nodeId: node2,
      spin: antiSpin,
      timestamp: Date.now()
    };

    // Entangle the particles
    particle1.entangledWith = particle2.id;
    particle2.entangledWith = particle1.id;

    this.particles.set(particle1.id, particle1);
    this.particles.set(particle2.id, particle2);

    return { particle1, particle2 };
  }

  /**
   * Measures a quantum particle
   * @param particle The particle to measure
   * @returns The measured particle with updated state
   */
  measureParticle(particle: QuantumParticle): QuantumParticle {
    // Measurement causes wave function collapse
    const measuredParticle = { ...particle };
    measuredParticle.timestamp = Date.now();

    // Add some quantum noise to simulate measurement uncertainty
    if (Math.random() > 0.95) {
      measuredParticle.spin = measuredParticle.spin === 'up' ? 'down' : 'up';
    }

    return measuredParticle;
  }

  /**
   * Verifies entanglement between two particles
   * @param particle1 First particle
   * @param particle2 Second particle
   * @returns Entanglement verification result
   */
  verifyEntanglement(
    particle1: QuantumParticle,
    particle2: QuantumParticle
  ): EntanglementResult {
    const startTime = Date.now();

    // Check if particles are entangled
    const isEntangled = 
      particle1.entangledWith === particle2.id &&
      particle2.entangledWith === particle1.id;

    if (!isEntangled) {
      return {
        isEntangled: false,
        correlation: 0,
        spookyAction: false,
        measurementTime: Date.now() - startTime
      };
    }

    // Calculate correlation based on spin states
    const correlation = this.calculateCorrelation(particle1.spin, particle2.spin);
    const spookyAction = correlation > this.MAX_CORRELATION;

    return {
      isEntangled: true,
      correlation: correlation,
      spookyAction: spookyAction,
      measurementTime: Date.now() - startTime
    };
  }

  /**
   * Generates a spooky entanglement report
   * @param results Array of entanglement results
   * @returns Formatted report
   */
  generateReport(results: EntanglementResult[]): string {
    const totalTests = results.length;
    const entangledCount = results.filter(r => r.isEntangled).length;
    const spookyCount = results.filter(r => r.spookyAction).length;
    const avgCorrelation = results.reduce((sum, r) => sum + r.correlation, 0) / totalTests;
    const avgMeasurementTime = results.reduce((sum, r) => sum + r.measurementTime, 0) / totalTests;

    return `
=== QUANTUM ENTANGLEMENT REPORT ===

Total Tests: ${totalTests}
Entangled Pairs: ${entangledCount}
Spooky Action Detected: ${spookyCount}

Average Correlation: ${avgCorrelation.toFixed(3)}
Average Measurement Time: ${avgMeasurementTime.toFixed(2)}ms

Spooky Action Probability: ${(spookyCount / totalTests * 100).toFixed(1)}%

"If you think you understand quantum mechanics,
 you don't understand quantum mechanics." - Feynman
    `;
  }

  /**
   * Private helper methods
   */
  private randomSpin(): 'up' | 'down' {
    return Math.random() > 0.5 ? 'up' : 'down';
  }

  private generateId(): string {
    return 'particle_' + Math.random().toString(36).substr(2, 9);
  }

  private calculateCorrelation(spin1: 'up' | 'down', spin2: 'up' | 'down'): number {
    // Perfect anti-correlation should be 1.0
    // Add some quantum noise
    const baseCorrelation = spin1 !== spin2 ? 1.0 : 0.0;
    const noise = (Math.random() - 0.5) * 0.1;
    return Math.max(0, Math.min(1, baseCorrelation + noise));
  }
}

// Convenience function for quick entanglement testing
export function quickEntanglementTest(): string {
  const checker = new QuantumEntanglementChecker();
  const results: EntanglementResult[] = [];

  // Create and test 10 entangled pairs
  for (let i = 0; i < 10; i++) {
    const { particle1, particle2 } = checker.createEntangledPair(
      `node-${i % 3}`, 
      `node-${(i + 1) % 3}`
    );

    const measured1 = checker.measureParticle(particle1);
    const measured2 = checker.measureParticle(particle2);

    const result = checker.verifyEntanglement(measured1, measured2);
    results.push(result);
  }

  return checker.generateReport(results);
}
