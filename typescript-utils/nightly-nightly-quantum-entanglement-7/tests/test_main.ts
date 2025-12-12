import { QuantumEntanglementChecker, QuantumState, AnalysisResult } from '../src/main';
import * as fs from 'fs';
import * as path from 'path';

// Mock file system operations for deterministic tests
jest.mock('fs');
const mockedFs = fs as jest.Mocked<typeof fs>;

describe('QuantumEntanglementChecker', () => {
  let checker: QuantumEntanglementChecker;

  beforeEach(() => {
    checker = new QuantumEntanglementChecker();
    jest.clearAllMocks();
  });

  describe('analyzeCode', () => {
    it('should detect superposition in untyped variables', () => {
      const code = 'let x = 42;';
      const result = checker.analyzeCode(code);
      
      expect(result.states).toHaveLength(1);
      expect(result.states[0].type).toBe('superposition');
      expect(result.states[0].variable).toBe('x');
      expect(result.states[0].line).toBe(1);
    });

    it('should not detect superposition in typed variables', () => {
      const code = 'let x: number = 42;';
      const result = checker.analyzeCode(code);
      
      expect(result.states).toHaveLength(0);
    });

    it('should detect entanglement between variables', () => {
      const code = 'let a = 42;\nlet b = a;';
      const result = checker.analyzeCode(code);
      
      expect(result.states).toHaveLength(2); // superposition + entanglement
      const entanglement = result.states.find(s => s.type === 'entanglement');
      expect(entanglement).toBeDefined();
      expect(entanglement?.variable).toBe('b');
    });

    it('should detect observer effect in console.log', () => {
      const code = 'let x = 42;\nconsole.log(x);';
      const result = checker.analyzeCode(code);
      
      expect(result.states).toHaveLength(2); // superposition + observer effect
      const observer = result.states.find(s => s.type === 'observer-effect');
      expect(observer).toBeDefined();
      expect(observer?.variable).toBe('x');
    });

    it('should handle empty code', () => {
      const code = '';
      const result = checker.analyzeCode(code);
      
      expect(result.states).toHaveLength(0);
      expect(result.totalIssues).toBe(0);
    });

    it('should handle multi-line code correctly', () => {
      const code = `let a = 1;
let b = a;
a = 2;
console.log(b);`;
      const result = checker.analyzeCode(code);
      
      expect(result.states).toHaveLength(4);
      expect(result.states[0].line).toBe(1);
      expect(result.states[1].line).toBe(2);
      expect(result.states[2].line).toBe(3);
      expect(result.states[3].line).toBe(4);
    });
  });

  describe('analyzeFile', () => {
    it('should analyze file content', () => {
      const mockContent = 'let x = 42;\nlet y = x;';
      mockedFs.readFileSync.mockReturnValue(mockContent);
      
      const result = checker.analyzeFile('/fake/path.ts');
      
      expect(mockedFs.readFileSync).toHaveBeenCalledWith('/fake/path.ts', 'utf-8');
      expect(result.states).toHaveLength(2);
      expect(result.file).toBe('/fake/path.ts');
    });
  });

  describe('analyzeDirectory', () => {
    it('should analyze directory recursively', () => {
      const mockFiles = [
        '/test/file1.ts',
        '/test/subdir/file2.js'
      ];
      
      mockedFs.readdirSync.mockReturnValue([
        { name: 'file1.ts', isDirectory: () => false, isFile: () => true },
        { name: 'subdir', isDirectory: () => true, isFile: () => false }
      ] as any);
      
      mockedFs.statSync.mockReturnValue({ isDirectory: () => true } as any);
      
      const results = checker.analyzeDirectory('/test');
      
      expect(mockedFs.readdirSync).toHaveBeenCalledWith('/test', { withFileTypes: true });
    });
  });

  describe('getSummary', () => {
    it('should generate correct summary', () => {
      const mockResults: AnalysisResult[] = [
        {
          file: 'test.ts',
          totalIssues: 3,
          states: [
            { type: 'superposition', line: 1, variable: 'x', description: '', suggestion: '' },
            { type: 'entanglement', line: 2, variable: 'y', description: '', suggestion: '' },
            { type: 'superposition', line: 3, variable: 'z', description: '', suggestion: '' }
          ]
        }
      ];
      
      const summary = checker.getSummary(mockResults);
      
      expect(summary).toContain('Total Issues Found: 3');
      expect(summary).toContain('Superposition: 2');
      expect(summary).toContain('Entanglement: 1');
      expect(summary).toContain('Decoherence: 0');
      expect(summary).toContain('Observer Effect: 0');
    });
  });

  describe('private methods', () => {
    it('should correctly identify type annotated variables', () => {
      const testCases = [
        { line: 'let x: number = 42;', expected: true },
        { line: 'let x = 42;', expected: false },
        { line: 'const y: string = "hello";', expected: true },
        { line: 'var z = true;', expected: false }
      ];
      
      testCases.forEach(({ line, expected }) => {
        const result = (checker as any).isTypeAnnotated(line);
        expect(result).toBe(expected);
      });
    });

    it('should validate variable names correctly', () => {
      const testCases = [
        { name: 'validVar', expected: true },
        { name: '_private', expected: true },
        { name: 'camelCase', expected: true },
        { name: '123invalid', expected: false },
        { name: 'invalid-name', expected: false },
        { name: 'valid123', expected: true }
      ];
      
      testCases.forEach(({ name, expected }) => {
        const result = (checker as any).isValidVariable(name);
        expect(result).toBe(expected);
      });
    });
  });

  describe('edge cases', () => {
    it('should handle self-assignment without entanglement', () => {
      const code = 'let x = 42;\nx = x;';
      const result = checker.analyzeCode(code);
      
      const entanglement = result.states.find(s => s.type === 'entanglement');
      expect(entanglement).toBeUndefined();
    });

    it('should handle complex expressions', () => {
      const code = 'let result = calculateValue(input * 2);';
      const result = checker.analyzeCode(code);
      
      expect(result.states).toHaveLength(1); // Only superposition for 'result'
      expect(result.states[0].type).toBe('superposition');
    });

    it('should handle TypeScript interfaces and types', () => {
      const code = `
interface User {
  name: string;
}

type UserId = string;

let user: User = { name: 'John' };
      `;
      const result = checker.analyzeCode(code);
      
      expect(result.states).toHaveLength(1); // Only superposition for 'user'
      expect(result.states[0].type).toBe('superposition');
    });
  });
});

// Mock rationale: We mock the file system to ensure tests are deterministic and don't depend on actual files.
// This allows us to test the analysis logic in isolation without requiring real file I/O operations.
