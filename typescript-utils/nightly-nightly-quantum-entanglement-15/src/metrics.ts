import { loadConfig, QuantumConfig } from './config';

export interface SystemMetrics {
  systemFidelity: number;
  coherence: number;
  entanglementQuality: string;
  decoherenceEvents: number;
  superpositionStates: number;
  recommendations: string[];
}

export class QuantumMetrics {
  private config: QuantumConfig;

  constructor(config?: QuantumConfig) {
    this.config = config || loadConfig();
  }

  async generateMetrics(
    componentName: string, 
    weight: number = 1.0
  ): Promise<number[]> {
    // Generate quantum-inspired metrics using pseudo-random but deterministic patterns
    const baseMetrics = this.generateBaseMetrics(componentName, weight);
    
    // Apply quantum noise (small random variations)
    const noisyMetrics = baseMetrics.map(metric => 
      this.applyQuantumNoise(metric, weight)
    );
    
    // Apply quantum fluctuations
    const fluctuatedMetrics = this.applyQuantumFluctuations(noisyMetrics);
    
    return fluctuatedMetrics;
  }

  private generateBaseMetrics(componentName: string, weight: number): number[] {
    const metrics: number[] = [];
    const seed = this.hashString(componentName);
    
    // Generate 10 metrics per component
    for (let i = 0; i < 10; i++) {
      // Use quantum-inspired mathematical functions
      const phase = (seed + i) * 0.1;
      const amplitude = 0.5 + (weight * 0.5);
      
      // Quantum wave function simulation
      const metric = amplitude * Math.sin(phase) + 
                    0.3 * Math.cos(phase * 2) + 
                    0.2 * Math.sin(phase * 3);
      
      // Normalize to 0-1 range
      const normalized = (metric + 1) / 2;
      metrics.push(normalized);
    }
    
    return metrics;
  }

  private applyQuantumNoise(metric: number, weight: number): number {
    // Add quantum noise (Heisenberg uncertainty principle inspired)
    const noiseLevel = 0.1 * (1.0 - weight * 0.5);
    const noise = (Math.random() - 0.5) * noiseLevel;
    
    let result = metric + noise;
    
    // Ensure result stays in valid range
    result = Math.max(0.0, Math.min(1.0, result));
    
    return result;
  }

  private applyQuantumFluctuations(metrics: number[]): number[] {
    return metrics.map((metric, index) => {
      // Quantum fluctuations based on position
      const fluctuation = 0.05 * Math.sin(index * 0.5) * Math.cos(index * 0.3);
      let result = metric + fluctuation;
      
      // Keep in bounds
      return Math.max(0.0, Math.min(1.0, result));
    });
  }

  async analyzeSystem(
    metricTypes: string[], 
    threshold: number
  ): Promise<SystemMetrics> {
    // Generate metrics for all configured components
    const components = this.config.components ? Object.keys(this.config.components) : ['default'];
    
    const componentMetrics = await Promise.all(
      components.map(async (component) => {
        const weight = this.config.components?.[component]?.weight || 1.0;
        return {
          name: component,
          metrics: await this.generateMetrics(component, weight)
        };
      })
    );
    
    // Calculate system-wide metrics
    const correlationMatrix = this.calculateCorrelationMatrix(
      componentMetrics.map(cm => cm.metrics)
    );
    
    const systemFidelity = this.calculateSystemFidelity(correlationMatrix);
    const coherence = this.calculateCoherence(correlationMatrix);
    const entanglementQuality = this.determineEntanglementQuality(systemFidelity, coherence);
    const decoherenceEvents = this.countDecoherenceEvents(correlationMatrix);
    const superpositionStates = this.countSuperpositionStates(correlationMatrix);
    
    const recommendations = this.generateSystemRecommendations(
      systemFidelity,
      coherence,
      entanglementQuality,
      decoherenceEvents
    );
    
    return {
      systemFidelity,
      coherence,
      entanglementQuality,
      decoherenceEvents,
      superpositionStates,
      recommendations
    };
  }

  private calculateCorrelationMatrix(metricArrays: number[][]): number[][] {
    const n = metricArrays.length;
    const matrix: number[][] = [];

    for (let i = 0; i < n; i++) {
      matrix[i] = [];
      for (let j = 0; j < n; j++) {
        if (i === j) {
          matrix[i][j] = 1.0;
        } else {
          matrix[i][j] = this.calculateCorrelation(metricArrays[i], metricArrays[j]);
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

  private calculateSystemFidelity(correlationMatrix: number[][]): number {
    const n = correlationMatrix.length;
    if (n === 0) return 0;

    let totalCorrelation = 0;
    let pairs = 0;

    for (let i = 0; i < n; i++) {
      for (let j = i + 1; j < n; j++) {
        totalCorrelation += Math.abs(correlationMatrix[i][j]);
        pairs++;
      }
    }

    return pairs > 0 ? totalCorrelation / pairs : 0;
  }

  private calculateCoherence(correlationMatrix: number[][]): number {
    const n = correlationMatrix.length;
    if (n === 0) return 0;

    let totalCoherence = 0;
    let pairs = 0;

    for (let i = 0; i < n; i++) {
      for (let j = i + 1; j < n; j++) {
        const correlation = Math.abs(correlationMatrix[i][j]);
        totalCoherence += correlation * correlation;
        pairs++;
      }
    }

    return pairs > 0 ? totalCoherence / pairs : 0;
  }

  private determineEntanglementQuality(fidelity: number, coherence: number): string {
    const qualityScore = (fidelity + coherence) / 2;
    
    if (qualityScore >= 0.9) return 'Excellent';
    if (qualityScore >= 0.8) return 'Good';
    if (qualityScore >= 0.6) return 'Fair';
    if (qualityScore >= 0.4) return 'Poor';
    return 'Critical';
  }

  private countDecoherenceEvents(correlationMatrix: number[][]): number {
    const n = correlationMatrix.length;
    let decoherenceCount = 0;

    for (let i = 0; i < n; i++) {
      for (let j = i + 1; j < n; j++) {
        const correlation = Math.abs(correlationMatrix[i][j]);
        if (correlation < 0.3) {
          decoherenceCount++;
        }
      }
    }

    return decoherenceCount;
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

  private generateSystemRecommendations(
    fidelity: number,
    coherence: number,
    quality: string,
    decoherenceEvents: number
  ): string[] {
    const recommendations: string[] = [];

    if (fidelity >= 0.9) {
      recommendations.push('System exhibits excellent quantum entanglement.');
    } else if (fidelity >= 0.7) {
      recommendations.push('Good entanglement detected. Monitor for decoherence.');
    } else {
      recommendations.push('Poor entanglement. System requires quantum reinitialization.');
    }

    if (coherence >= 0.8) {
      recommendations.push('High quantum coherence maintained throughout system.');
    } else if (coherence >= 0.6) {
      recommendations.push('Moderate coherence. Watch for environmental interference.');
    } else {
      recommendations.push('Low coherence detected. System vulnerable to quantum noise.');
    }

    if (quality === 'Excellent') {
      recommendations.push('System operating at quantum optimal levels.');
    } else if (quality === 'Critical') {
      recommendations.push('CRITICAL: System in quantum crisis state.');
      recommendations.push('Emergency quantum error correction protocols required.');
    }

    if (decoherenceEvents > 0) {
      recommendations.push(`Detected ${decoherenceEvents} decoherence events.`);
      recommendations.push('Consider implementing quantum isolation protocols.');
    }

    return recommendations;
  }

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
