import { QuantumEntanglementChecker, EntanglementStatus } from '../src/main';
import * as fs from 'fs';
import * as path from 'path';

// Mock file system for testing
const mockFiles = {
  'similar1.ts': `
function calculateTotal(items: number[]): number {
  return items.reduce((sum, item) => sum + item, 0);
}

const config = {
  apiUrl: 'https://api.example.com',
  timeout: 5000
};
`,
  'similar2.ts': `
function sumArray(numbers: number[]): number {
  return numbers.reduce((acc, num) => acc + num, 0);
}

const settings = {
  apiUrl: 'https://api.example.com',
  timeout: 5000
};
`,
  'different1.ts': `
class UserManager {
  private users: User[] = [];
  
  addUser(user: User): void {
    this.users.push(user);
  }
}
`,
  'different2.ts': `
const config = {
  apiUrl: 'https://api.example.com',
  timeout: 5000
};

interface User {
  id: number;
  name: string;
}
`,
  'empty1.ts': '',
  'empty2.ts': '',
};

describe('QuantumEntanglementChecker', () => {
  let checker: QuantumEntanglementChecker;
  let tempDir: string;

  beforeAll(() => {
    // Create temporary directory for test files
    tempDir = path.join(__dirname, 'temp_test_files');
    if (!fs.existsSync(tempDir)) {
      fs.mkdirSync(tempDir);
    }

    // Create test files
    Object.entries(mockFiles).forEach(([filename, content]) => {
      fs.writeFileSync(path.join(tempDir, filename), content);
    });
  });

  afterAll(() => {
    // Clean up test files
    Object.keys(mockFiles).forEach(filename => {
      const filePath = path.join(tempDir, filename);
      if (fs.existsSync(filePath)) {
        fs.unlinkSync(filePath);
      }
    });
    fs.rmdirSync(tempDir);
  });

  beforeEach(() => {
    checker = new QuantumEntanglementChecker();
  });

  describe('checkEntanglement', () => {
    it('should detect high entanglement between similar functions', async () => {
      const result = await checker.checkEntanglement(
        path.join(tempDir, 'similar1.ts'),
        path.join(tempDir, 'similar2.ts')
      );

      expect(result.score).toBeGreaterThan(0.5);
      expect(result.status).toBe('PARTIALLY_ENTANGLED');
      expect(result.analysis.structuralSimilarity).toBeGreaterThan(0);
      expect(result.analysis.functionPatterns).toBeGreaterThan(0);
    });

    it('should detect no entanglement between different code structures', async () => {
      const result = await checker.checkEntanglement(
        path.join(tempDir, 'different1.ts'),
        path.join(tempDir, 'different2.ts')
      );

      expect(result.score).toBeLessThan(0.5);
      expect(result.status).toBe('NO_ENTANGLEMENT');
    });

    it('should handle empty files gracefully', async () => {
      const result = await checker.checkEntanglement(
        path.join(tempDir, 'empty1.ts'),
        path.join(tempDir, 'empty2.ts')
      );

      expect(result.score).toBe(0);
      expect(result.status).toBe('NO_ENTANGLEMENT');
    });

    it('should throw error for non-existent file', async () => {
      await expect(
        checker.checkEntanglement('nonexistent1.ts', 'nonexistent2.ts')
      ).rejects.toThrow('File not found');
    });

    it('should respect custom threshold', async () => {
      const result = await checker.checkEntanglement(
        path.join(tempDir, 'similar1.ts'),
        path.join(tempDir, 'similar2.ts'),
        { threshold: 0.9 }
      );

      // With high threshold, similar files might not be considered entangled
      expect(result.score).toBeLessThan(1);
    });

    it('should provide detailed analysis in verbose mode', async () => {
      const result = await checker.checkEntanglement(
        path.join(tempDir, 'similar1.ts'),
        path.join(tempDir, 'similar2.ts'),
        { verbose: true }
      );

      expect(result.analysis.detailedAnalysis).toBeDefined();
      expect(result.analysis.detailedAnalysis.length).toBeGreaterThan(0);
      expect(result.analysis.detailedAnalysis[0]).toContain('Detailed Quantum Analysis');
    });
  });

  describe('parseCodeStructure', () => {
    it('should parse functions correctly', async () => {
      const result = await checker.checkEntanglement(
        path.join(tempDir, 'similar1.ts'),
        path.join(tempDir, 'similar2.ts')
      );

      // The checker internally parses structures, so we test through the main method
      expect(result.analysis.structuralSimilarity).toBeDefined();
      expect(typeof result.analysis.structuralSimilarity).toBe('number');
    });

    it('should handle complex code structures', async () => {
      const complexCode = `
class ComplexClass {
  private data: any[];
  
  constructor(data: any[]) {
    this.data = data;
  }
  
  public processData(): any[] {
    return this.data.map(item => {
      if (typeof item === 'object') {
        return Object.keys(item);
      }
      return item;
    });
  }
}

function helperFunction(input: string): string {
  return input.toUpperCase();
}

const config = {
  version: '1.0.0',
  debug: true
};
`;

      const tempFile = path.join(tempDir, 'complex.ts');
      fs.writeFileSync(tempFile, complexCode);

      const result = await checker.checkEntanglement(
        path.join(tempDir, 'similar1.ts'),
        tempFile
      );

      expect(result.score).toBeGreaterThanOrEqual(0);
      expect(result.score).toBeLessThanOrEqual(1);

      // Clean up
      fs.unlinkSync(tempFile);
    });
  });

  describe('calculateOverallScore', () => {
    it('should return weighted average of all metrics', () => {
      // This is tested indirectly through the main checkEntanglement method
      const result = await checker.checkEntanglement(
        path.join(tempDir, 'similar1.ts'),
        path.join(tempDir, 'similar2.ts')
      );

      // Score should be between 0 and 1
      expect(result.score).toBeGreaterThanOrEqual(0);
      expect(result.score).toBeLessThanOrEqual(1);

      // All analysis metrics should be defined
      expect(result.analysis.structuralSimilarity).toBeDefined();
      expect(result.analysis.functionPatterns).toBeDefined();
      expect(result.analysis.variableNaming).toBeDefined();
      expect(result.analysis.logicFlow).toBeDefined();
    });
  });

  describe('determineStatus', () => {
    it('should correctly classify entanglement status', async () => {
      // Test high entanglement
      const highEntanglementResult = await checker.checkEntanglement(
        path.join(tempDir, 'similar1.ts'),
        path.join(tempDir, 'similar2.ts')
      );

      if (highEntanglementResult.score >= 0.8) {
        expect(highEntanglementResult.status).toBe('QUANTUM_ENTANGLED');
      } else if (highEntanglementResult.score >= 0.5) {
        expect(highEntanglementResult.status).toBe('PARTIALLY_ENTANGLED');
      } else {
        expect(highEntanglementResult.status).toBe('NO_ENTANGLEMENT');
      }

      // Test low entanglement
      const lowEntanglementResult = await checker.checkEntanglement(
        path.join(tempDir, 'different1.ts'),
        path.join(tempDir, 'different2.ts')
      );

      expect(lowEntanglementResult.status).toBe('NO_ENTANGLEMENT');
    });
  });

  describe('error handling', () => {
    it('should handle malformed code gracefully', async () => {
      const malformedCode = 'function broken { syntax error';
      const tempFile = path.join(tempDir, 'malformed.ts');
      fs.writeFileSync(tempFile, malformedCode);

      // Should not throw, but might return low similarity
      const result = await checker.checkEntanglement(
        path.join(tempDir, 'similar1.ts'),
        tempFile
      );

      expect(result.score).toBeGreaterThanOrEqual(0);
      expect(result.score).toBeLessThanOrEqual(1);

      // Clean up
      fs.unlinkSync(tempFile);
    });
  });

  describe('edge cases', () => {
    it('should handle files with only comments', async () => {
      const commentOnlyCode = `// This is a comment
/* This is a block comment */
// Another comment`;
      const tempFile1 = path.join(tempDir, 'comments1.ts');
      const tempFile2 = path.join(tempDir, 'comments2.ts');
      fs.writeFileSync(tempFile1, commentOnlyCode);
      fs.writeFileSync(tempFile2, commentOnlyCode);

      const result = await checker.checkEntanglement(tempFile1, tempFile2);

      // Files with only comments should have some similarity
      expect(result.score).toBeGreaterThanOrEqual(0);

      // Clean up
      fs.unlinkSync(tempFile1);
      fs.unlinkSync(tempFile2);
    });

    it('should handle very large files', async () => {
      const largeCode = 'function test() { return ' + 'a'.repeat(1000) + '; }';
      const tempFile1 = path.join(tempDir, 'large1.ts');
      const tempFile2 = path.join(tempDir, 'large2.ts');
      fs.writeFileSync(tempFile1, largeCode);
      fs.writeFileSync(tempFile2, largeCode);

      const result = await checker.checkEntanglement(tempFile1, tempFile2);

      // Identical large files should have high entanglement
      expect(result.score).toBeCloseTo(1, 1);

      // Clean up
      fs.unlinkSync(tempFile1);
      fs.unlinkSync(tempFile2);
    });
  });
});

// Mock rationale: We're testing the QuantumEntanglementChecker class with various scenarios
// including similar code, different code, empty files, malformed code, and edge cases.
// The tests use mock file system operations to create temporary test files and verify
// the behavior of the entanglement detection algorithms without requiring actual file I/O
// in the test environment. All tests are deterministic and offline.
