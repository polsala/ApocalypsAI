import * as fs from 'fs';
import * as path from 'path';
import { program } from 'commander';

interface EntanglementResult {
  score: number;
  status: EntanglementStatus;
  analysis: AnalysisDetails;
  files: { file1: string; file2: string };
}

type EntanglementStatus = 'QUANTUM_ENTANGLED' | 'PARTIALLY_ENTANGLED' | 'NO_ENTANGLEMENT';

interface AnalysisDetails {
  structuralSimilarity: number;
  functionPatterns: number;
  variableNaming: number;
  logicFlow: number;
  detailedAnalysis?: string[];
}

interface CodeStructure {
  functions: FunctionInfo[];
  classes: ClassInfo[];
  variables: VariableInfo[];
  imports: string[];
  complexity: number;
}

interface FunctionInfo {
  name: string;
  parameters: string[];
  returnType: string;
  bodyLength: number;
  complexity: number;
}

interface ClassInfo {
  name: string;
  methods: FunctionInfo[];
  properties: VariableInfo[];
}

interface VariableInfo {
  name: string;
  type: string;
  scope: 'global' | 'function' | 'class';
}

class QuantumEntanglementChecker {
  private threshold: number;
  private verbose: boolean;

  constructor(threshold: number = 0.5, verbose: boolean = false) {
    this.threshold = threshold;
    this.verbose = verbose;
  }

  async checkEntanglement(
    file1Path: string,
    file2Path: string,
    options: { threshold?: number; verbose?: boolean } = {}
  ): Promise<EntanglementResult> {
    const threshold = options.threshold ?? this.threshold;
    const verbose = options.verbose ?? this.verbose;

    // Read files
    const file1Content = this.readFile(file1Path);
    const file2Content = this.readFile(file2Path);

    // Parse code structure
    const structure1 = this.parseCodeStructure(file1Content);
    const structure2 = this.parseCodeStructure(file2Content);

    // Calculate similarity scores
    const structuralSimilarity = this.calculateStructuralSimilarity(structure1, structure2);
    const functionPatterns = this.calculateFunctionPatterns(structure1, structure2);
    const variableNaming = this.calculateVariableNaming(structure1, structure2);
    const logicFlow = this.calculateLogicFlow(structure1, structure2);

    // Calculate overall score
    const score = this.calculateOverallScore(
      structuralSimilarity,
      functionPatterns,
      variableNaming,
      logicFlow
    );

    // Determine status
    const status = this.determineStatus(score);

    // Create analysis details
    const analysis: AnalysisDetails = {
      structuralSimilarity,
      functionPatterns,
      variableNaming,
      logicFlow,
    };

    if (verbose) {
      analysis.detailedAnalysis = this.generateDetailedAnalysis(structure1, structure2, score);
    }

    return {
      score,
      status,
      analysis,
      files: { file1: file1Path, file2: file2Path },
    };
  }

  private readFile(filePath: string): string {
    if (!fs.existsSync(filePath)) {
      throw new Error(`File not found: ${filePath}`);
    }
    return fs.readFileSync(filePath, 'utf-8');
  }

  private parseCodeStructure(content: string): CodeStructure {
    const lines = content.split('\n');
    const functions: FunctionInfo[] = [];
    const classes: ClassInfo[] = [];
    const variables: VariableInfo[] = [];
    const imports: string[] = [];

    let currentClass: ClassInfo | null = null;
    let complexity = 0;

    for (const line of lines) {
      const trimmed = line.trim();

      // Parse imports
      if (trimmed.startsWith('import ') || trimmed.startsWith('from ')) {
        imports.push(trimmed);
      }
      // Parse classes
      else if (trimmed.startsWith('class ')) {
        const className = this.extractClassName(trimmed);
        currentClass = { name: className, methods: [], properties: [] };
        classes.push(currentClass);
      }
      // Parse functions
      else if (trimmed.includes('function ') || trimmed.includes('=>') || trimmed.includes('(') && trimmed.includes(')') && !trimmed.startsWith('}')) {
        const funcInfo = this.parseFunction(trimmed, currentClass ? 'class' : 'global');
        if (funcInfo) {
          if (currentClass) {
            currentClass.methods.push(funcInfo);
          } else {
            functions.push(funcInfo);
          }
        }
      }
      // Parse variables
      else if (this.isVariableDeclaration(trimmed)) {
        const varInfo = this.parseVariable(trimmed);
        variables.push(varInfo);
      }

      // Calculate complexity
      if (this.isComplexityIndicator(trimmed)) {
        complexity++;
      }
    }

    return {
      functions,
      classes,
      variables,
      imports,
      complexity,
    };
  }

  private extractClassName(line: string): string {
    const match = line.match(/class\s+(\w+)/);
    return match ? match[1] : 'UnknownClass';
  }

  private parseFunction(line: string, scope: 'global' | 'class'): FunctionInfo | null {
    // Simple function parsing - this is a simplified version
    const nameMatch = line.match(/(?:function\s+|const\s+|let\s+|var\s+)(\w+)/);
    if (!nameMatch) return null;

    const name = nameMatch[1];
    const paramsMatch = line.match(/\(([^)]*)\)/);
    const parameters = paramsMatch ? paramsMatch[1].split(',').map(p => p.trim()).filter(p => p) : [];

    return {
      name,
      parameters,
      returnType: 'unknown',
      bodyLength: 1, // Simplified
      complexity: 1, // Simplified
    };
  }

  private parseVariable(line: string): VariableInfo {
    const nameMatch = line.match(/(?:const|let|var)\s+(\w+)/);
    const name = nameMatch ? nameMatch[1] : 'unknown';
    const type = this.extractType(line);

    return {
      name,
      type,
      scope: 'global', // Simplified
    };
  }

  private extractType(line: string): string {
    const typeMatch = line.match(/:\s*(\w+)/);
    return typeMatch ? typeMatch[1] : 'any';
  }

  private isVariableDeclaration(line: string): boolean {
    return /^(const|let|var)\s+\w+/.test(line);
  }

  private isComplexityIndicator(line: string): boolean {
    return /(?:if|for|while|switch|try)/.test(line);
  }

  private calculateStructuralSimilarity(structure1: CodeStructure, structure2: CodeStructure): number {
    const totalElements = Math.max(structure1.functions.length + structure1.classes.length + structure1.variables.length,
                                  structure2.functions.length + structure2.classes.length + structure2.variables.length);

    if (totalElements === 0) return 0;

    const commonFunctions = this.findCommonElements(structure1.functions, structure2.functions, 'name');
    const commonClasses = this.findCommonElements(structure1.classes, structure2.classes, 'name');
    const commonVariables = this.findCommonElements(structure1.variables, structure2.variables, 'name');

    const totalCommon = commonFunctions + commonClasses + commonVariables;
    return totalCommon / totalElements;
  }

  private calculateFunctionPatterns(structure1: CodeStructure, structure2: CodeStructure): number {
    if (structure1.functions.length === 0 && structure2.functions.length === 0) return 1;

    const totalFunctions = Math.max(structure1.functions.length, structure2.functions.length);
    let matchingPatterns = 0;

    for (const func1 of structure1.functions) {
      for (const func2 of structure2.functions) {
        if (this.similarFunctionPattern(func1, func2)) {
          matchingPatterns++;
          break;
        }
      }
    }

    return matchingPatterns / totalFunctions;
  }

  private calculateVariableNaming(structure1: CodeStructure, structure2: CodeStructure): number {
    if (structure1.variables.length === 0 && structure2.variables.length === 0) return 1;

    const totalVariables = Math.max(structure1.variables.length, structure2.variables.length);
    let similarNames = 0;

    for (const var1 of structure1.variables) {
      for (const var2 of structure2.variables) {
        if (this.similarVariableName(var1.name, var2.name)) {
          similarNames++;
          break;
        }
      }
    }

    return similarNames / totalVariables;
  }

  private calculateLogicFlow(structure1: CodeStructure, structure2: CodeStructure): number {
    const complexity1 = structure1.complexity;
    const complexity2 = structure2.complexity;
    const maxComplexity = Math.max(complexity1, complexity2);

    if (maxComplexity === 0) return 1;

    const complexityDiff = Math.abs(complexity1 - complexity2);
    return 1 - (complexityDiff / maxComplexity);
  }

  private findCommonElements<T>(arr1: T[], arr2: T[], key: keyof T): number {
    const set1 = new Set(arr1.map(item => item[key]));
    const set2 = new Set(arr2.map(item => item[key]));
    const common = new Set([...set1].filter(x => set2.has(x)));
    return common.size;
  }

  private similarFunctionPattern(func1: FunctionInfo, func2: FunctionInfo): boolean {
    // Check if functions have similar parameter counts and names
    if (func1.parameters.length !== func2.parameters.length) return false;

    const paramSimilarity = this.calculateParameterSimilarity(func1.parameters, func2.parameters);
    return paramSimilarity > 0.5;
  }

  private calculateParameterSimilarity(params1: string[], params2: string[]): number {
    if (params1.length !== params2.length) return 0;

    let similar = 0;
    for (let i = 0; i < params1.length; i++) {
      if (this.similarVariableName(params1[i], params2[i])) {
        similar++;
      }
    }

    return similar / params1.length;
  }

  private similarVariableName(name1: string, name2: string): boolean {
    // Simple string similarity check
    const lower1 = name1.toLowerCase();
    const lower2 = name2.toLowerCase();

    // Check for exact match
    if (lower1 === lower2) return true;

    // Check for similar patterns (e.g., sum vs total, calculate vs compute)
    const similarPatterns = [
      ['sum', 'total', 'calculate'],
      ['get', 'fetch', 'retrieve'],
      ['set', 'update', 'modify'],
      ['user', 'person', 'entity'],
      ['data', 'info', 'details']
    ];

    for (const pattern of similarPatterns) {
      if (pattern.includes(lower1) && pattern.includes(lower2)) {
        return true;
      }
    }

    // Check for substring match
    return lower1.includes(lower2) || lower2.includes(lower1);
  }

  private calculateOverallScore(
    structural: number,
    functions: number,
    variables: number,
    logic: number
  ): number {
    // Weighted average
    return (
      structural * 0.4 +
      functions * 0.3 +
      variables * 0.2 +
      logic * 0.1
    );
  }

  private determineStatus(score: number): EntanglementStatus {
    if (score >= 0.8) return 'QUANTUM_ENTANGLED';
    if (score >= 0.5) return 'PARTIALLY_ENTANGLED';
    return 'NO_ENTANGLEMENT';
  }

  private generateDetailedAnalysis(
    structure1: CodeStructure,
    structure2: CodeStructure,
    score: number
  ): string[] {
    const analysis: string[] = [];

    analysis.push('🔬 Detailed Quantum Analysis:');
    analysis.push('==============================');

    analysis.push(`\nFile 1 Structure:`);
    analysis.push(`- Functions: ${structure1.functions.length}`);
    analysis.push(`- Classes: ${structure1.classes.length}`);
    analysis.push(`- Variables: ${structure1.variables.length}`);
    analysis.push(`- Complexity: ${structure1.complexity}`);

    analysis.push(`\nFile 2 Structure:`);
    analysis.push(`- Functions: ${structure2.functions.length}`);
    analysis.push(`- Classes: ${structure2.classes.length}`);
    analysis.push(`- Variables: ${structure2.variables.length}`);
    analysis.push(`- Complexity: ${structure2.complexity}`);

    analysis.push(`\nQuantum Entanglement Score: ${score.toFixed(2)}`);

    return analysis;
  }

  displayResult(result: EntanglementResult, jsonOutput: boolean = false): void {
    if (jsonOutput) {
      console.log(JSON.stringify(result, null, 2));
      return;
    }

    console.log('\n🔬 Quantum Entanglement Analysis');
    console.log('================================');
    console.log(`\nFile 1: ${result.files.file1}`);
    console.log(`File 2: ${result.files.file2}`);
    console.log(`\nEntanglement Score: ${result.score.toFixed(2)} ${this.getStarRating(result.score)}`);
    console.log(`Status: ${result.status}`);

    console.log('\nAnalysis:');
    console.log(`- Structural similarity: ${(result.analysis.structuralSimilarity * 100).toFixed(0)}%`);
    console.log(`- Function patterns: ${(result.analysis.functionPatterns * 100).toFixed(0)}%`);
    console.log(`- Variable naming: ${(result.analysis.variableNaming * 100).toFixed(0)}%`);
    console.log(`- Logic flow: ${(result.analysis.logicFlow * 100).toFixed(0)}%`);

    if (result.analysis.detailedAnalysis) {
      console.log('\nDetailed Analysis:');
      result.analysis.detailedAnalysis.forEach(line => console.log(line));
    }

    console.log(`\nConclusion: ${this.getConclusion(result.status)}`);
  }

  private getStarRating(score: number): string {
    const stars = Math.ceil(score * 5);
    return '⭐'.repeat(stars) + '⚪'.repeat(5 - stars);
  }

  private getConclusion(status: EntanglementStatus): string {
    switch (status) {
      case 'QUANTUM_ENTANGLED':
        return 'These pieces of code are highly entangled!';
      case 'PARTIALLY_ENTANGLED':
        return 'Moderate entanglement detected.';
      case 'NO_ENTANGLEMENT':
        return 'No quantum entanglement detected.';
    }
  }
}

// CLI Interface
async function main() {
  program
    .name('quantum-entanglement')
    .description('Check if two pieces of code are quantum entangled')
    .version('1.0.0')
    .argument('<file1>', 'First file to compare')
    .argument('<file2>', 'Second file to compare')
    .option('-t, --threshold <number>', 'Minimum entanglement score (0-1)', parseFloat, 0.5)
    .option('-j, --json', 'Output in JSON format')
    .option('-v, --verbose', 'Show detailed analysis')
    .action(async (file1, file2, options) => {
      try {
        const checker = new QuantumEntanglementChecker(options.threshold, options.verbose);
        const result = await checker.checkEntanglement(file1, file2, options);
        checker.displayResult(result, options.json);
      } catch (error) {
        console.error('Error:', error.message);
        process.exit(1);
      }
    });

  await program.parseAsync();
}

if (require.main === module) {
  main().catch(console.error);
}

export { QuantumEntanglementChecker, EntanglementResult, EntanglementStatus };
