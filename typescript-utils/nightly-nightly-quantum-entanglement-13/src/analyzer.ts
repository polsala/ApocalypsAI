import { QuantumState, EntanglementResult, AnalysisOptions } from './types';
import { FileAnalyzer } from './file-analyzer';
import { QuantumSimulator } from './quantum-simulator';
import { DependencyGraph } from './dependency-graph';

export class QuantumEntanglementAnalyzer {
  private fileAnalyzer: FileAnalyzer;
  private quantumSimulator: QuantumSimulator;
  private dependencyGraph: DependencyGraph;

  constructor() {
    this.fileAnalyzer = new FileAnalyzer();
    this.quantumSimulator = new QuantumSimulator();
    this.dependencyGraph = new DependencyGraph();
  }

  async analyze(
    targetPath: string,
    options: AnalysisOptions
  ): Promise<EntanglementResult> {
    const startTime = Date.now();

    // Step 1: Analyze files and extract dependencies
    const fileAnalysis = await this.fileAnalyzer.analyzeDirectory(targetPath);

    // Step 2: Build dependency graph
    this.dependencyGraph.buildGraph(fileAnalysis.files);

    // Step 3: Simulate quantum states for each component
    const quantumStates = this.quantumSimulator.simulateStates(
      fileAnalysis.components,
      this.dependencyGraph
    );

    // Step 4: Calculate entanglement scores
    const entanglementPairs = this.calculateEntanglement(
      quantumStates,
      options.threshold
    );

    // Step 5: Generate overall metrics
    const overallScore = this.calculateOverallScore(entanglementPairs);

    return {
      targetPath,
      timestamp: new Date().toISOString(),
      analysisTime: Date.now() - startTime,
      totalFiles: fileAnalysis.files.length,
      totalComponents: fileAnalysis.components.length,
      entanglementScore: overallScore,
      entangledPairs,
      recommendations: this.generateRecommendations(entanglementPairs, overallScore)
    };
  }

  private calculateEntanglement(
    quantumStates: QuantumState[],
    threshold: number
  ): Array<{
    component1: string;
    component2: string;
    score: number;
    type: 'high' | 'medium' | 'low';
  }> {
    const pairs: Array<{
      component1: string;
      component2: string;
      score: number;
      type: 'high' | 'medium' | 'low';
    }> = [];

    // Compare all pairs of quantum states
    for (let i = 0; i < quantumStates.length; i++) {
      for (let j = i + 1; j < quantumStates.length; j++) {
        const state1 = quantumStates[i];
        const state2 = quantumStates[j];

        // Calculate entanglement using quantum state overlap
        const entanglementScore = this.calculateStateOverlap(state1, state2);

        if (entanglementScore > threshold) {
          const type = this.categorizeEntanglement(entanglementScore);

          pairs.push({
            component1: state1.componentName,
            component2: state2.componentName,
            score: entanglementScore,
            type
          });
        }
      }
    }

    // Sort by score descending
    return pairs.sort((a, b) => b.score - a.score);
  }

  private calculateStateOverlap(state1: QuantumState, state2: QuantumState): number {
    // Simulate quantum state overlap calculation
    // This is a simplified version of quantum entanglement measurement

    const sharedDependencies = state1.dependencies.filter(dep => 
      state2.dependencies.includes(dep)
    ).length;

    const totalDependencies = new Set([...state1.dependencies, ...state2.dependencies]).size;

    // Calculate coupling coefficient
    const couplingCoefficient = sharedDependencies / Math.max(1, totalDependencies);

    // Apply quantum interference effects
    const interferenceFactor = this.quantumSimulator.calculateInterference(
      state1.quantumSignature,
      state2.quantumSignature
    );

    // Final entanglement score
    return Math.min(1.0, couplingCoefficient * (1 + interferenceFactor));
  }

  private categorizeEntanglement(score: number): 'high' | 'medium' | 'low' {
    if (score >= 0.8) return 'high';
    if (score >= 0.5) return 'medium';
    return 'low';
  }

  private calculateOverallScore(
    entangledPairs: Array<{ score: number }>
  ): number {
    if (entangledPairs.length === 0) return 0;

    const totalScore = entangledPairs.reduce((sum, pair) => sum + pair.score, 0);
    const averageScore = totalScore / entangledPairs.length;

    // Apply quantum superposition weighting
    const maxScore = Math.max(...entangledPairs.map(p => p.score));

    return Math.min(1.0, (averageScore * 0.7) + (maxScore * 0.3));
  }

  private generateRecommendations(
    entangledPairs: Array<{
      component1: string;
      component2: string;
      score: number;
      type: 'high' | 'medium' | 'low';
    }>,
    overallScore: number
  ): string[] {
    const recommendations: string[] = [];

    // High-level recommendations based on overall score
    if (overallScore > 0.7) {
      recommendations.push('⚠️  High entanglement detected - consider major refactoring');
      recommendations.push('💡 Implement dependency injection patterns');
      recommendations.push('🔧 Extract shared dependencies into separate modules');
    } else if (overallScore > 0.4) {
      recommendations.push('⚠️  Moderate entanglement - monitor closely');
      recommendations.push('💡 Review circular dependency chains');
    } else {
      recommendations.push('✅ Low entanglement - code structure looks good!');
    }

    // Specific recommendations for high-entanglement pairs
    const highPairs = entangledPairs.filter(p => p.type === 'high');
    if (highPairs.length > 0) {
      recommendations.push('\n🔍 High-entanglement pairs to review:');
      highPairs.slice(0, 3).forEach(pair => {
        recommendations.push(
          `   • ${pair.component1} ↔ ${pair.component2} (Score: ${pair.score.toFixed(2)})`
        );
      });
    }

    return recommendations;
  }
}
