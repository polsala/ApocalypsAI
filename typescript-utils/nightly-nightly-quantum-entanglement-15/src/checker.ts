import { loadConfig, QuantumConfig } from './config';
import { QuantumMetrics } from './metrics';

export interface EntanglementResult {
  fidelity: number;
  entangled: boolean;
  decoherenceRisk: string;
  recommendations: string;
  correlationMatrix: number[][];
  bellState: string;
  superpositionStates: number;
}

export class QuantumEntanglementChecker {
  private config: QuantumConfig;
  private metrics: QuantumMetrics;

  constructor(config?: QuantumConfig) {
    this.config = config || loadConfig();
    this.metrics = new QuantumMetrics(this.config);
  }

  async checkEntanglement(
    components: string[], 
    threshold: number = 0.8
  ): Promise<EntanglementResult> {
    if (components.length < 2) {
      throw new Error('At least 2 components required for entanglement check');
    }

    // Generate quantum-inspired metrics for each component
    const componentMetrics = await Promise.all(
      components.map(async (component) => {
        const weight = this.config.components?.[component]?.weight || 1.0;
        return {
          name: component,
          metrics: await this.metrics.generateMetrics(component, weight),
          weight
        };
      })
    );

    // Calculate correlation matrix
    const correlationMatrix = this.calculateCorrelationMatrix(componentMetrics);

    // Calculate Bell state fidelity
    const fidelity = this.calculateBellStateFidelity(correlationMatrix);

    // Determine entanglement status
    const entangled = fidelity >= threshold;

    // Calculate decoherence risk
    const decoherenceRisk = this.calculateDecoherenceRisk(correlationMatrix, fidelity);

    // Generate recommendations
    const recommendations = this.generateRecommendations(
      fidelity, 
      entangled, 
      decoherenceRisk,
      components
    );

    // Determine Bell state
    const bellState = this.determineBellState(fidelity);

    // Count superposition states
    const superpositionStates = this.countSuperpositionStates(correlationMatrix);

    return {
      fidelity,
      entangled,
      decoherenceRisk,
      recommendations,
      correlationMatrix,
      bellState,
      superpositionStates
    };
  }

  private calculateCorrelationMatrix(
    componentMetrics: Array<{name: string, metrics: number[], weight: number}>
  ): number[][] {
    const n = componentMetrics.length;
    const matrix: number[][] = [];

    for (let i = 0; i < n; i++) {
      matrix[i] = [];
      for (let j = 0; j < n; j++) {
        if (i === j) {
          matrix[i][j] = 1.0; // Perfect correlation with itself
        } else {
          const correlation = this.calculateCorrelation(
            componentMetrics[i].metrics,
            componentMetrics[j].metrics
          );
          // Apply weights
          const weight = (componentMetrics[i].weight + componentMetrics[j].weight) / 2;
          matrix[i][j] = correlation * weight;
        }
      }
    }

    return matrix;
  }

  private calculateCorrelation(metrics1: number[], metrics2: number[]): number {
    if (metrics1.length !== metrics2.length || metrics1.length === 0) {
      return 0;
    }

    const n = metrics1.length;
    const mean1 = metrics1.reduce((a, b) => a + b, 0) / n;
    const mean2 = metrics2.reduce((a, b) => a + b, 0) / n;

    let numerator = 0;
    let denominator1 = 0;
    let denominator2 = 0;

    for (let i = 0; i < n; i++) {
      const diff1 = metrics1[i] - mean1;
      const diff2 = metrics2[i] - mean2;
      numerator += diff1 * diff2;
      denominator1 += diff1 * diff1;
      denominator2 += diff2 * diff2;
    }

    const denominator = Math.sqrt(denominator1 * denominator2);
    return denominator === 0 ? 0 : numerator / denominator;
  }

  private calculateBellStateFidelity(correlationMatrix: number[][]): number {
    const n = correlationMatrix.length;
    if (n < 2) return 0;

    // Calculate average correlation (simplified Bell state fidelity)
    let totalCorrelation = 0;
    let pairs = 0;

    for (let i = 0; i < n; i++) {
      for (let j = i + 1; j < n; j++) {
        totalCorrelation += Math.abs(correlationMatrix[i][j]);
        pairs++;
      }
    }

    const averageCorrelation = pairs > 0 ? totalCorrelation / pairs : 0;

    // Apply quantum-inspired fidelity calculation
    // Perfect entanglement would have correlations of ±1
    const fidelity = Math.min(1.0, averageCorrelation + 0.1 * Math.random());

    return Math.max(0.0, Math.min(1.0, fidelity));
  }

  private calculateDecoherenceRisk(
    correlationMatrix: number[][], 
    fidelity: number
  ): string {
    const n = correlationMatrix.length;
    let lowCorrelations = 0;

    for (let i = 0; i < n; i++) {
      for (let j = i + 1; j < n; j++) {
        if (Math.abs(correlationMatrix[i][j]) < 0.5) {
          lowCorrelations++;
        }
      }
    }

    const totalPairs = (n * (n - 1)) / 2;
    const lowCorrelationRatio = totalPairs > 0 ? lowCorrelations / totalPairs : 0;

    if (fidelity >= 0.9) return 'Low';
    if (fidelity >= 0.7 || lowCorrelationRatio < 0.3) return 'Medium';
    return 'High';
  }

  private generateRecommendations(
    fidelity: number,
    entangled: boolean,
    decoherenceRisk: string,
    components: string[]
  ): string {
    if (entangled && fidelity >= 0.9) {
      return 'Excellent entanglement detected! System is operating at quantum optimal levels.';
    }

    if (entangled && fidelity >= 0.7) {
      return 'Good entanglement. Monitor for potential decoherence events.';
    }

    if (decoherenceRisk === 'High') {
      return `High decoherence risk detected. Consider implementing quantum error correction protocols for ${components.join(', ')}.`;
    }

    if (fidelity < 0.5) {
      return `Critical entanglement failure. Immediate quantum state reinitialization required for all components.`;
    }

    return 'System requires attention. Review component synchronization protocols.';
  }

  private determineBellState(fidelity: number): string {
    if (fidelity >= 0.95) return '|Φ⁺⟩ (Phi Plus)';
    if (fidelity >= 0.85) return '|Φ⁻⟩ (Phi Minus)';
    if (fidelity >= 0.75) return '|Ψ⁺⟩ (Psi Plus)';
    return '|Ψ⁻⟩ (Psi Minus)';
  }

  private countSuperpositionStates(correlationMatrix: number[][]): number {
    const n = correlationMatrix.length;
    let superpositionCount = 0;

    for (let i = 0; i < n; i++) {
      for (let j = i + 1; j < n; j++) {
        const correlation = Math.abs(correlationMatrix[i][j]);
        if (correlation > 0.3 && correlation < 0.9) {
          superpositionCount++;
        }
      }
    }

    return superpositionCount;
  }
}
