import { QuantumEntanglementChecker, QuantumState, AnalysisResult } from '../src/main';

// Mock rationale: Deterministic quantum states for reproducible tests
const createMockQuantumState = (superposition: number, entangled: number, collapsed: number): QuantumState => ({
  superposition,
  entangled,
  collapsed
});

describe('QuantumEntanglementChecker', () => {
  let checker: QuantumEntanglementChecker;

  beforeEach(() => {
    checker = new QuantumEntanglementChecker();
  });

  describe('calculateEntanglement', () => {
    it('should return high entanglement for well-connected code', () => {
      const states = createMockQuantumState(5, 10, 2);
      const result = (checker as any).calculateEntanglement(states);
      expect(result).toBeGreaterThan(0.7);
      expect(result).toBeLessThanOrEqual(0.99);
    });

    it('should return low entanglement for isolated code', () => {
      const states = createMockQuantumState(1, 1, 10);
      const result = (checker as any).calculateEntanglement(states);
      expect(result).toBeLessThan(0.5);
      expect(result).toBeGreaterThanOrEqual(0.1);
    });

    it('should handle edge cases', () => {
      const states = createMockQuantumState(0, 0, 1);
      const result = (checker as any).calculateEntanglement(states);
      expect(result).toBe(0.1); // Minimum threshold
    });
  });

  describe('determineStatus', () => {
    it('should return ENTANGLED for high entanglement', () => {
      const status = (checker as any).determineStatus(0.8);
      expect(status).toBe('ENTANGLED');
    });

    it('should return SEPARATED for low entanglement', () => {
      const status = (checker as any).determineStatus(0.2);
      expect(status).toBe('SEPARATED');
    });

    it('should return UNCERTAIN for medium entanglement', () => {
      const status = (checker as any).determineStatus(0.5);
      expect(status).toBe('UNCERTAIN');
    });
  });

  describe('generateRecommendations', () => {
    it('should provide recommendations for separated states', () => {
      const states = createMockQuantumState(2, 1, 8);
      const recommendations = (checker as any).generateRecommendations(states, 'SEPARATED');
      expect(recommendations.length).toBeGreaterThan(0);
      expect(recommendations.some(rec => rec.includes('import'))).toBe(true);
    });

    it('should provide collapse warnings', () => {
      const states = createMockQuantumState(3, 2, 10);
      const recommendations = (checker as any).generateRecommendations(states, 'UNCERTAIN');
      expect(recommendations.some(rec => rec.includes('collapse'))).toBe(true);
    });

    it('should provide positive feedback for optimal states', () => {
      const states = createMockQuantumState(5, 8, 2);
      const recommendations = (checker as any).generateRecommendations(states, 'ENTANGLED');
      expect(recommendations.some(rec => rec.includes('optimal'))).toBe(true);
    });
  });

  describe('hashString', () => {
    it('should produce consistent hashes', () => {
      const input = 'test string';
      const hash1 = (checker as any).hashString(input);
      const hash2 = (checker as any).hashString(input);
      expect(hash1).toBe(hash2);
    });

    it('should produce different hashes for different inputs', () => {
      const hash1 = (checker as any).hashString('test1');
      const hash2 = (checker as any).hashString('test2');
      expect(hash1).not.toBe(hash2);
    });
  });

  describe('generateRandomSequence', () => {
    it('should produce deterministic sequences', () => {
      const seed = 12345;
      const seq1 = (checker as any).generateRandomSequence(seed, 3);
      const seq2 = (checker as any).generateRandomSequence(seed, 3);
      expect(seq1).toEqual(seq2);
    });

    it('should produce values between 0 and 1', () => {
      const seed = 12345;
      const sequence = (checker as any).generateRandomSequence(seed, 10);
      sequence.forEach(value => {
        expect(value).toBeGreaterThanOrEqual(0);
        expect(value).toBeLessThanOrEqual(1);
      });
    });
  });

  describe('getStatusEmoji', () => {
    it('should return correct emojis', () => {
      expect((checker as any).getStatusEmoji('ENTANGLED')).toBe('✅');
      expect((checker as any).getStatusEmoji('SEPARATED')).toBe('❌');
      expect((checker as any).getStatusEmoji('UNCERTAIN')).toBe('⚠️');
    });
  });

  describe('Integration Tests', () => {
    it('should analyze a mock TypeScript file', async () => {
      // Create a temporary test file
      const mockContent = `
        import { useState } from 'react';
        import { fetchData } from './api';
        
        function myComponent() {
          const [state, setState] = useState(null);
          
          const handleClick = async () => {
            const data = await fetchData();
            setState(data);
          };
          
          return <button onClick={handleClick}>Click me</button>;
        }
      `;
      
      // Mock the readFile method
      const originalReadFile = (checker as any).readFile;
      (checker as any).readFile = () => mockContent;
      
      const result = await checker.analyzeFile('mock.ts');
      
      // Restore original method
      (checker as any).readFile = originalReadFile;
      
      expect(result).toBeDefined();
      expect(result.entanglementLevel).toBeGreaterThan(0);
      expect(result.entanglementLevel).toBeLessThanOrEqual(1);
      expect(result.status).toMatch(/(ENTANGLED|SEPARATED|UNCERTAIN)/);
      expect(Array.isArray(result.recommendations)).toBe(true);
    });
  });
});

// Test configuration options
describe('QuantumEntanglementChecker Configuration', () => {
  it('should use default configuration', () => {
    const checker = new QuantumEntanglementChecker();
    expect((checker as any).config.verbose).toBe(false);
    expect((checker as any).config.report).toBe(false);
    expect((checker as any).config.threshold).toBe(0.7);
  });

  it('should override configuration', () => {
    const checker = new QuantumEntanglementChecker({
      verbose: true,
      threshold: 0.8
    });
    expect((checker as any).config.verbose).toBe(true);
    expect((checker as any).config.threshold).toBe(0.8);
  });
});
