import { loadConfig, QuantumConfig } from './config';
import { QuantumEntanglementChecker } from './checker';
import { QuantumMetrics } from './metrics';
import * as readline from 'readline';

export interface MonitoringResult {
  timestamp: Date;
  systemFidelity: number;
  coherence: number;
  entanglementQuality: string;
  decoherenceEvents: number;
  superpositionStates: number;
  recommendations: string[];
}

export class QuantumMonitor {
  private config: QuantumConfig;
  private checker: QuantumEntanglementChecker;
  private metrics: QuantumMetrics;
  private isMonitoring: boolean = false;
  private monitoringInterval: NodeJS.Timeout | null = null;

  constructor(config?: QuantumConfig) {
    this.config = config || loadConfig();
    this.checker = new QuantumEntanglementChecker(this.config);
    this.metrics = new QuantumMetrics(this.config);
  }

  async startMonitoring(
    components: string[], 
    interval: number = 30000
  ): Promise<void> {
    this.isMonitoring = true;
    
    // Set up graceful shutdown
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });
    
    const shutdown = () => {
      this.stopMonitoring();
      rl.close();
      process.exit(0);
    };
    
    process.on('SIGINT', shutdown);
    process.on('SIGTERM', shutdown);
    
    console.log(`Monitoring started. Press Ctrl+C to stop.\n`);
    
    // Initial check
    await this.performMonitoringCheck(components);
    
    // Set up interval
    this.monitoringInterval = setInterval(async () => {
      if (this.isMonitoring) {
        await this.performMonitoringCheck(components);
      }
    }, interval);
  }

  private async performMonitoringCheck(components: string[]): Promise<void> {
    try {
      const result = await this.analyzeSystemState(components);
      
      console.log('='.repeat(60));
      console.log(`🌌 Quantum Monitoring Report`);
      console.log(`Timestamp: ${result.timestamp.toISOString()}`);
      console.log(`System Fidelity: ${result.systemFidelity.toFixed(3)}`);
      console.log(`Quantum Coherence: ${result.coherence.toFixed(3)}`);
      console.log(`Entanglement Quality: ${result.entanglementQuality}`);
      console.log(`Decoherence Events: ${result.decoherenceEvents}`);
      console.log(`Superposition States: ${result.superpositionStates}`);
      
      if (result.recommendations.length > 0) {
        console.log('\n💡 Recommendations:');
        result.recommendations.forEach(rec => console.log(`   • ${rec}`));
      }
      
      console.log('='.repeat(60));
      console.log();
      
    } catch (error) {
      console.error('❌ Monitoring error:', error.message);
    }
  }

  private async analyzeSystemState(components: string[]): Promise<MonitoringResult> {
    // Check entanglement
    const entanglementResult = await this.checker.checkEntanglement(components);
    
    // Generate additional metrics
    const systemMetrics = await this.metrics.analyzeSystem([
      'cpu', 'memory', 'network', 'latency'
    ], 0.8);
    
    // Calculate coherence
    const coherence = this.calculateCoherence(entanglementResult.correlationMatrix);
    
    // Determine entanglement quality
    const entanglementQuality = this.determineEntanglementQuality(
      entanglementResult.fidelity,
      coherence
    );
    
    // Count decoherence events (simplified)
    const decoherenceEvents = this.countDecoherenceEvents(
      entanglementResult.correlationMatrix
    );
    
    // Count superposition states
    const superpositionStates = entanglementResult.superpositionStates;
    
    // Generate recommendations
    const recommendations = this.generateMonitoringRecommendations(
      entanglementResult,
      systemMetrics,
      coherence,
      entanglementQuality
    );
    
    return {
      timestamp: new Date(),
      systemFidelity: entanglementResult.fidelity,
      coherence,
      entanglementQuality,
      decoherenceEvents,
      superpositionStates,
      recommendations
    };
  }

  private calculateCoherence(correlationMatrix: number[][]): number {
    const n = correlationMatrix.length;
    if (n === 0) return 0;

    let totalCoherence = 0;
    let pairs = 0;

    for (let i = 0; i < n; i++) {
      for (let j = i + 1; j < n; j++) {
        const correlation = Math.abs(correlationMatrix[i][j]);
        // Coherence is high when correlations are strong and stable
        totalCoherence += correlation * correlation; // Squared for non-linearity
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
        // Decoherence occurs when correlation drops below threshold
        if (correlation < 0.3) {
          decoherenceCount++;
        }
      }
    }

    return decoherenceCount;
  }

  private generateMonitoringRecommendations(
    entanglementResult: any,
    systemMetrics: any,
    coherence: number,
    entanglementQuality: string
  ): string[] {
    const recommendations: string[] = [];

    if (entanglementResult.fidelity >= 0.9) {
      recommendations.push('System operating at quantum optimal levels.');
    } else if (entanglementResult.fidelity >= 0.7) {
      recommendations.push('Good entanglement. Monitor for potential decoherence.');
    } else {
      recommendations.push('Critical entanglement failure detected.');
      recommendations.push('Immediate quantum state reinitialization required.');
    }

    if (coherence >= 0.8) {
      recommendations.push('High quantum coherence maintained.');
    } else if (coherence >= 0.6) {
      recommendations.push('Moderate coherence. Watch for environmental interference.');
    } else {
      recommendations.push('Low coherence detected. System vulnerable to decoherence.');
    }

    if (entanglementQuality === 'Excellent') {
      recommendations.push('Quantum system in optimal state.');
    } else if (entanglementQuality === 'Critical') {
      recommendations.push('System in quantum crisis. Emergency protocols recommended.');
    }

    if (systemMetrics.decoherenceEvents > 0) {
      recommendations.push(`Detected ${systemMetrics.decoherenceEvents} decoherence events.`);
      recommendations.push('Consider implementing quantum error correction.');
    }

    return recommendations;
  }

  stopMonitoring(): void {
    this.isMonitoring = false;
    
    if (this.monitoringInterval) {
      clearInterval(this.monitoringInterval);
      this.monitoringInterval = null;
    }
    
    console.log('\n🛑 Quantum monitoring stopped.');
  }
}
