// Type definitions for Quantum Entanglement Checker

export interface QuantumState {
  componentName: string;
  dependencies: string[];
  quantumSignature: number[];
  coherenceLevel: number;
  entanglementHistory: string[];
}

export interface EntanglementResult {
  targetPath: string;
  timestamp: string;
  analysisTime: number;
  totalFiles: number;
  totalComponents: number;
  entanglementScore: number;
  entangledPairs: Array<{
    component1: string;
    component2: string;
    score: number;
    type: 'high' | 'medium' | 'low';
  }>;
  recommendations: string[];
}

export interface AnalysisOptions {
  threshold: number;
  reportType: ReportType;
}

export type ReportType = 'simple' | 'detailed' | 'json';

export interface CLIOptions {
  targetPath: string;
  threshold: number;
  reportType: ReportType;
  watch: boolean;
}

export interface FileAnalysis {
  files: string[];
  components: ComponentAnalysis[];
}

export interface ComponentAnalysis {
  name: string;
  filePath: string;
  dependencies: string[];
  linesOfCode: number;
  complexity: number;
}

export interface DependencyGraph {
  nodes: Map<string, ComponentNode>;
  edges: Array<{ from: string; to: string; weight: number }>;
}

export interface ComponentNode {
  id: string;
  name: string;
  dependencies: string[];
  dependents: string[];
  metrics: ComponentMetrics;
}

export interface ComponentMetrics {
  coupling: number;
  cohesion: number;
  complexity: number;
  linesOfCode: number;
}

export interface QuantumSimulationConfig {
  coherenceDecayRate: number;
  entanglementThreshold: number;
  superpositionFactor: number;
  interferenceSensitivity: number;
}

export const DEFAULT_SIMULATION_CONFIG: QuantumSimulationConfig = {
  coherenceDecayRate: 0.1,
  entanglementThreshold: 0.3,
  superpositionFactor: 0.5,
  interferenceSensitivity: 0.2
};
