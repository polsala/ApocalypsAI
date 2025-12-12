import * as fs from 'fs';
import * as path from 'path';

export interface QuantumState {
  type: 'superposition' | 'entanglement' | 'decoherence' | 'observer-effect';
  line: number;
  variable: string;
  description: string;
  suggestion: string;
}

export interface AnalysisResult {
  file: string;
  states: QuantumState[];
  totalIssues: number;
}

export class QuantumEntanglementChecker {
  private readonly patterns = {
    superposition: /let\s+(\w+)\s*=/g,
    entanglement: /(\w+)\s*=\s*(\w+)/g,
    decoherence: /(\w+)\s*=\s*[^\w]/g,
    observerEffect: /console\.log\((\w+)\)/g
  };

  /**
   * Analyze a single TypeScript/JavaScript file
   */
  analyzeFile(filePath: string): AnalysisResult {
    const content = fs.readFileSync(filePath, 'utf-8');
    const lines = content.split('\n');
    
    const states: QuantumState[] = [];

    lines.forEach((line, index) => {
      const lineNumber = index + 1;

      // Check for superposition (variables that could be multiple types)
      const superpositionMatches = [...line.matchAll(this.patterns.superposition)];
      superpositionMatches.forEach(match => {
        const variable = match[1];
        if (!this.isTypeAnnotated(line)) {
          states.push({
            type: 'superposition',
            line: lineNumber,
            variable,
            description: `Variable '${variable}' exists in quantum superposition (no explicit type)`,
            suggestion: `Add explicit type annotation: let ${variable}: Type = ...`
          });
        }
      });

      // Check for entanglement (variables sharing state)
      const entanglementMatches = [...line.matchAll(this.patterns.entanglement)];
      entanglementMatches.forEach(match => {
        const source = match[1];
        const target = match[2];
        if (source !== target && this.isValidVariable(source) && this.isValidVariable(target)) {
          states.push({
            type: 'entanglement',
            line: lineNumber,
            variable: target,
            description: `Variable '${target}' is quantumly entangled with '${source}'`,
            suggestion: `Consider deep cloning or immutable patterns to break entanglement`
          });
        }
      });

      // Check for decoherence (variables losing original state)
      const decoherenceMatches = [...line.matchAll(this.patterns.decoherence)];
      decoherenceMatches.forEach(match => {
        const variable = match[1];
        if (this.isValidVariable(variable)) {
          states.push({
            type: 'decoherence',
            line: lineNumber,
            variable,
            description: `Variable '${variable}' experiencing quantum decoherence`,
            suggestion: `Preserve original state or use immutable data structures`
          });
        }
      });

      // Check for observer effect (variables changing when accessed)
      const observerMatches = [...line.matchAll(this.patterns.observerEffect)];
      observerMatches.forEach(match => {
        const variable = match[1];
        if (this.isValidVariable(variable)) {
          states.push({
            type: 'observer-effect',
            line: lineNumber,
            variable,
            description: `Observer effect detected: '${variable}' changes when observed`,
            suggestion: `Avoid side effects in logging or use getter functions`
          });
        }
      });
    });

    return {
      file: filePath,
      states,
      totalIssues: states.length
    };
  }

  /**
   * Analyze code string directly
   */
  analyzeCode(code: string): AnalysisResult {
    const lines = code.split('\n');
    const states: QuantumState[] = [];

    lines.forEach((line, index) => {
      const lineNumber = index + 1;

      // Superposition check
      const superpositionMatches = [...line.matchAll(this.patterns.superposition)];
      superpositionMatches.forEach(match => {
        const variable = match[1];
        if (!this.isTypeAnnotated(line)) {
          states.push({
            type: 'superposition',
            line: lineNumber,
            variable,
            description: `Variable '${variable}' exists in quantum superposition`,
            suggestion: `Add explicit type annotation: let ${variable}: Type = ...`
          });
        }
      });

      // Entanglement check
      const entanglementMatches = [...line.matchAll(this.patterns.entanglement)];
      entanglementMatches.forEach(match => {
        const source = match[1];
        const target = match[2];
        if (source !== target && this.isValidVariable(source) && this.isValidVariable(target)) {
          states.push({
            type: 'entanglement',
            line: lineNumber,
            variable: target,
            description: `Variable '${target}' is quantumly entangled with '${source}'`,
            suggestion: `Consider deep cloning or immutable patterns to break entanglement`
          });
        }
      });
    });

    return {
      file: '<code-string>',
      states,
      totalIssues: states.length
    };
  }

  /**
   * Analyze entire directory
   */
  analyzeDirectory(dirPath: string): AnalysisResult[] {
    const results: AnalysisResult[] = [];
    const files = this.getFilesRecursively(dirPath, ['.ts', '.js', '.tsx', '.jsx']);

    files.forEach(file => {
      try {
        const result = this.analyzeFile(file);
        if (result.totalIssues > 0) {
          results.push(result);
        }
      } catch (error) {
        // Skip files that can't be read
      }
    });

    return results;
  }

  /**
   * Get summary of all quantum states found
   */
  getSummary(results: AnalysisResult[]): string {
    const totalIssues = results.reduce((sum, r) => sum + r.totalIssues, 0);
    const stateCounts = this.countStates(results);

    return `
Quantum Entanglement Analysis Summary:
========================================
Total Issues Found: ${totalIssues}

State Distribution:
- Superposition: ${stateCounts.superposition}
- Entanglement: ${stateCounts.entanglement}
- Decoherence: ${stateCounts.decoherence}
- Observer Effect: ${stateCounts.observerEffect}

Recommendation: ${this.getRecommendation(stateCounts)}
    `;
  }

  private isTypeAnnotated(line: string): boolean {
    return /:\s*\w+\s*=/.test(line);
  }

  private isValidVariable(name: string): boolean {
    return /^[a-zA-Z_][a-zA-Z0-9_]*$/.test(name);
  }

  private getFilesRecursively(dir: string, extensions: string[]): string[] {
    const files: string[] = [];
    
    try {
      const entries = fs.readdirSync(dir, { withFileTypes: true });
      
      entries.forEach(entry => {
        const fullPath = path.join(dir, entry.name);
        
        if (entry.isDirectory() && !entry.name.startsWith('.')) {
          files.push(...this.getFilesRecursively(fullPath, extensions));
        } else if (entry.isFile()) {
          const ext = path.extname(entry.name);
          if (extensions.includes(ext)) {
            files.push(fullPath);
          }
        }
      });
    } catch (error) {
      // Skip directories that can't be read
    }
    
    return files;
  }

  private countStates(results: AnalysisResult[]): Record<string, number> {
    const counts = {
      superposition: 0,
      entanglement: 0,
      decoherence: 0,
      'observer-effect': 0
    };

    results.forEach(result => {
      result.states.forEach(state => {
        counts[state.type]++;
      });
    });

    return counts;
  }

  private getRecommendation(counts: Record<string, number>): string {
    const maxState = Object.entries(counts).reduce((a, b) => a[1] > b[1] ? a : b)[0];
    
    switch (maxState) {
      case 'superposition':
        return 'Add explicit type annotations to collapse quantum states.';
      case 'entanglement':
        return 'Break entanglement with immutable data patterns.';
      case 'decoherence':
        return 'Preserve quantum coherence with immutable structures.';
      case 'observer-effect':
        return 'Eliminate observer effects by avoiding side effects.';
      default:
        return 'Maintain quantum harmony with clean code practices.';
    }
  }
}

// CLI interface
if (require.main === module) {
  const args = process.argv.slice(2);
  const checker = new QuantumEntanglementChecker();

  if (args.length === 0) {
    console.log('Usage: npx nightly-quantum-entanglement-checker <file-or-directory>');
    process.exit(1);
  }

  const target = args[0];
  let results: AnalysisResult[];

  try {
    if (fs.statSync(target).isDirectory()) {
      results = checker.analyzeDirectory(target);
    } else {
      results = [checker.analyzeFile(target)];
    }

    console.log(checker.getSummary(results));
    
    if (results.length > 0) {
      results.forEach(result => {
        console.log(`\nFile: ${result.file}`);
        result.states.forEach(state => {
          console.log(`  Line ${state.line}: ${state.type.toUpperCase()} - ${state.description}`);
          console.log(`    Suggestion: ${state.suggestion}\n`);
        });
      });
    }
  } catch (error) {
    console.error('Error analyzing target:', error);
    process.exit(1);
  }
}
