import { loadConfig, QuantumConfig } from './config';
import { QuantumMetrics } from './metrics';

export interface BellStateResult {
  fidelity: number;
  verified: boolean;
  bellInequality: number;
  correlation: number;
  recommendations: string[];
}

export class BellStateAnalyzer {
  private config: QuantumConfig;
  private metrics: QuantumMetrics;

  constructor(config?: QuantumConfig) {
    this.config = config || loadConfig();
    this.metrics = new QuantumMetrics(this.config);
  }

  async verifyBellStates(
    pairs: string[], 
    targetState: string = 'phi_plus'
  ): Promise<BellStateResult[]> {
    return await Promise.all(
      pairs.map(async (pair) => {
        const [component1, component2] = pair.split(':');
        
        if (!component1 || !component2) {
          throw new Error(`Invalid pair format: ${pair}. Use component1:component2`);
        }

        return this.verifyBellState(component1, component2, targetState);
      })
    );
  }

  private async verifyBellState(
    component1: string, 
    component2: string, 
    targetState: string
  ): Promise<BellStateResult> {
    // Generate metrics for both components
    const metrics1 = await this.metrics.generateMetrics(component1);
    const metrics2 = await this.metrics.generateMetrics(component2);

    // Calculate correlation
    const correlation = this.calculateCorrelation(metrics1, metrics2);

    // Calculate Bell inequality violation
    const bellInequality = this.calculateBellInequality(metrics1, metrics2);

    // Calculate fidelity based on target Bell state
    const fidelity = this.calculateBellStateFidelity(correlation, targetState);

    // Determine if Bell state is verified
    const verified = fidelity >= 0.8 && bellInequality > 2.0;

    // Generate recommendations
    const recommendations = this.generateBellRecommendations(
      fidelity, 
      bellInequality, 
      verified,
      targetState
    );

    return {
      fidelity,
      verified,
      bellInequality,
      correlation,
      recommendations
    };
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

  private calculateBellInequality(metrics1: number[], metrics2: number[]): number {
    // Simplified Bell inequality calculation
    // In quantum mechanics, Bell inequality violation indicates entanglement
    
    const n = Math.min(metrics1.length, metrics2.length);
    if (n < 4) return 0;

    // Calculate expectation values for different measurement settings
    const settings = [
      { a: 0, b: 0 },
      { a: 0, b: 45 },
      { a: 45, b: 0 },
      { a: 45, b: 45 }
    ];

    let sum = 0;
    for (const setting of settings) {
      let expectation = 0;
      for (let i = 0; i < n; i++) {
        // Simplified quantum measurement simulation
        const angle1 = (setting.a * Math.PI) / 180;
        const angle2 = (setting.b * Math.PI) / 180;
        
        const measurement1 = Math.sin(angle1) * metrics1[i % metrics1.length];
        const measurement2 = Math.sin(angle2) * metrics2[i % metrics2.length];
        
        expectation += measurement1 * measurement2;
      }
      sum += Math.abs(expectation / n);
    }

    return sum;
  }

  private calculateBellStateFidelity(
    correlation: number, 
    targetState: string
  ): number {
    // Different Bell states have different expected correlation patterns
    let expectedCorrelation: number;

    switch (targetState.toLowerCase()) {
      case 'phi_plus':
      case '|φ+⟩':
        expectedCorrelation = 1.0; // Perfect positive correlation
        break;
      case 'phi_minus':
      case '|φ-⟩':
        expectedCorrelation = -1.0; // Perfect negative correlation
        break;
      case 'psi_plus':
      case '|ψ+⟩':
        expectedCorrelation = 0.0; // Orthogonal
        break;
      case 'psi_minus':
      case '|ψ-⟩':
        expectedCorrelation = 0.0; // Orthogonal
        break;
      default:
        expectedCorrelation = 0.0;
    }

    // Calculate fidelity as similarity to expected correlation
    const fidelity = 1.0 - Math.abs(correlation - expectedCorrelation) / 2.0;
    return Math.max(0.0, Math.min(1.0, fidelity));
  }

  private generateBellRecommendations(
    fidelity: number,
    bellInequality: number,
    verified: boolean,
    targetState: string
  ): string[] {
    const recommendations: string[] = [];

    if (verified) {
      recommendations.push(`✅ Bell state ${targetState} successfully verified!`);
      recommendations.push('System exhibits quantum entanglement characteristics.');
    } else {
      recommendations.push(`❌ Bell state ${targetState} verification failed.`);
      
      if (fidelity < 0.8) {
        recommendations.push('Low fidelity detected. Components may not be properly synchronized.');
      }
      
      if (bellInequality <= 2.0) {
        recommendations.push('Bell inequality not violated. Classical correlations detected.');
      }
    }

    if (fidelity >= 0.9) {
      recommendations.push('Excellent quantum state fidelity achieved.');
    } else if (fidelity >= 0.7) {
      recommendations.push('Good fidelity. Monitor for decoherence.');
    } else {
      recommendations.push('Poor fidelity. Consider quantum error correction.');
    }

    if (bellInequality > 2.5) {
      recommendations.push('Strong quantum correlations detected.');
    } else if (bellInequality > 2.0) {
      recommendations.push('Marginal quantum behavior observed.');
    } else {
      recommendations.push('Classical behavior dominant. Quantum effects minimal.');
    }

    return recommendations;
  }
}
