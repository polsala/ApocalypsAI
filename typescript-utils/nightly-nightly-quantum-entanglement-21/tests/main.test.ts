import { QuantumEntanglementChecker } from '../src/quantum-entanglement-checker';
import { QuantumReportGenerator } from '../src/quantum-report-generator';
import { parseArgs } from '../src/cli-parser';

// Mock console methods to avoid cluttering test output
const originalConsole = { ...console };
beforeEach(() => {
  console.log = jest.fn();
  console.error = jest.fn();
  console.clear = jest.fn();
});

afterEach(() => {
  console.log = originalConsole.log;
  console.error = originalConsole.error;
  console.clear = originalConsole.clear;
});

describe('QuantumEntanglementChecker', () => {
  let checker: QuantumEntanglementChecker;

  beforeEach(() => {
    checker = new QuantumEntanglementChecker();
  });

  test('should check entanglement for given nodes', async () => {
    const nodes = ['Alpha', 'Beta'];
    const result = await checker.checkEntanglement(nodes);

    expect(result.nodes).toHaveLength(2);
    expect(result.nodes[0].name).toBe('Alpha');
    expect(result.nodes[1].name).toBe('Beta');
    expect(result.timestamp).toBeInstanceOf(Date);
    expect(result.overallStability).toBeGreaterThanOrEqual(0);
    expect(result.overallStability).toBeLessThanOrEqual(100);
  });

  test('should generate quantum nodes with valid properties', async () => {
    const nodes = ['TestNode'];
    const result = await checker.checkEntanglement(nodes);

    const node = result.nodes[0];
    expect(node.spin).toMatch(/^(up|down)$/);
    expect(node.coherence).toBeGreaterThanOrEqual(0);
    expect(node.coherence).toBeLessThanOrEqual(100);
    expect(typeof node.entangledWith).toBe('object');
  });

  test('should generate entanglement links with valid properties', async () => {
    const nodes = ['Alpha', 'Beta', 'Gamma'];
    const result = await checker.checkEntanglement(nodes);

    if (result.links.length > 0) {
      const link = result.links[0];
      expect(link.from).toBeDefined();
      expect(link.to).toBeDefined();
      expect(link.strength).toMatch(/^(strong|medium|weak)$/);
      expect(link.bellState).toBeDefined();
      expect(link.coherence).toBeGreaterThanOrEqual(0);
      expect(link.coherence).toBeLessThanOrEqual(100);
    }
  });

  test('should handle empty node list', async () => {
    const result = await checker.checkEntanglement([]);

    expect(result.nodes).toHaveLength(0);
    expect(result.links).toHaveLength(0);
    expect(result.overallStability).toBe(0);
  });
});

describe('QuantumReportGenerator', () => {
  let generator: QuantumReportGenerator;
  let mockResult: any;

  beforeEach(() => {
    generator = new QuantumReportGenerator();
    mockResult = {
      nodes: [
        { name: 'Alpha', spin: 'up', coherence: 94, entangledWith: ['Beta'] },
        { name: 'Beta', spin: 'down', coherence: 92, entangledWith: ['Alpha'] }
      ],
      links: [
        { from: 'Alpha', to: 'Beta', strength: 'strong', bellState: '|↑↓⟩ - |↓↑⟩', coherence: 93 }
      ],
      overallStability: 87,
      warnings: ['Node Gamma experiencing decoherence'],
      timestamp: new Date('2024-01-15T10:30:00.000Z')
    };
  });

  test('should generate valid JSON report', () => {
    const report = generator.generateReport(mockResult, ['Alpha', 'Beta']);
    const parsed = JSON.parse(report);

    expect(parsed.timestamp).toBe('2024-01-15T10:30:00.000Z');
    expect(parsed.quantumStateAnalysis).toHaveLength(2);
    expect(parsed.entanglementLinks).toHaveLength(1);
    expect(parsed.overallStability).toBe(87);
    expect(parsed.warnings).toContain('Node Gamma experiencing decoherence');
  });

  test('should display results correctly', () => {
    generator.displayResults(mockResult, ['Alpha', 'Beta']);
    // Test passes if no errors are thrown
    expect(true).toBe(true);
  });
});

describe('CLI Parser', () => {
  test('should parse nodes argument', () => {
    const originalArgv = process.argv;
    process.argv = ['node', 'script', '--nodes', 'alpha,beta,gamma'];
    
    const result = parseArgs();
    
    expect(result.nodes).toBe('alpha,beta,gamma');
    
    process.argv = originalArgv;
  });

  test('should parse report flag', () => {
    const originalArgv = process.argv;
    process.argv = ['node', 'script', '--report'];
    
    const result = parseArgs();
    
    expect(result.report).toBe(true);
    
    process.argv = originalArgv;
  });

  test('should parse monitor flag', () => {
    const originalArgv = process.argv;
    process.argv = ['node', 'script', '--monitor', '--interval', '10000'];
    
    const result = parseArgs();
    
    expect(result.monitor).toBe(true);
    expect(result.interval).toBe(10000);
    
    process.argv = originalArgv;
  });

  test('should parse help flag', () => {
    const originalArgv = process.argv;
    process.argv = ['node', 'script', '--help'];
    
    const result = parseArgs();
    
    expect(result.help).toBe(true);
    
    process.argv = originalArgv;
  });

  test('should return default values for empty args', () => {
    const originalArgv = process.argv;
    process.argv = ['node', 'script'];
    
    const result = parseArgs();
    
    expect(result.nodes).toBeUndefined();
    expect(result.report).toBe(false);
    expect(result.monitor).toBe(false);
    expect(result.interval).toBe(5000);
    expect(result.help).toBe(false);
    
    process.argv = originalArgv;
  });
});
