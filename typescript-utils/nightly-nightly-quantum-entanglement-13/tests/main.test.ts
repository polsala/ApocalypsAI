import { QuantumEntanglementAnalyzer } from '../src/analyzer';
import { parseArguments } from '../src/cli-parser';
import { formatReport } from '../src/report-formatter';
import { EntanglementResult, ReportType } from '../src/types';

// Mock dependencies
jest.mock('../src/file-analyzer');
jest.mock('../src/quantum-simulator');
jest.mock('../src/dependency-graph');

describe('QuantumEntanglementAnalyzer', () => {
  let analyzer: QuantumEntanglementAnalyzer;

  beforeEach(() => {
    analyzer = new QuantumEntanglementAnalyzer();
  });

  test('should analyze directory and return results', async () => {
    const mockResult: EntanglementResult = {
      targetPath: './test-src',
      timestamp: '2024-01-15T10:30:00Z',
      analysisTime: 100,
      totalFiles: 5,
      totalComponents: 3,
      entanglementScore: 0.42,
      entangledPairs: [
        {
          component1: 'UserService',
          component2: 'AuthService',
          score: 0.87,
          type: 'high'
        }
      ],
      recommendations: ['Consider refactoring high-entanglement pairs']
    };

    // Mock the analyze method
    jest.spyOn(analyzer, 'analyze').mockResolvedValue(mockResult);

    const result = await analyzer.analyze('./test-src', {
      threshold: 0.3,
      reportType: 'detailed'
    });

    expect(result).toEqual(mockResult);
    expect(result.entanglementScore).toBe(0.42);
    expect(result.entangledPairs.length).toBe(1);
  });

  test('should handle analysis errors gracefully', async () => {
    jest.spyOn(analyzer, 'analyze').mockRejectedValue(new Error('Analysis failed'));

    await expect(
      analyzer.analyze('./invalid-path', {
        threshold: 0.3,
        reportType: 'detailed'
      })
    ).rejects.toThrow('Analysis failed');
  });
});

describe('CLI Argument Parsing', () => {
  test('should parse basic arguments correctly', () => {
    const originalArgv = process.argv;
    process.argv = ['node', 'quantum-entangle-check', './src'];

    const options = parseArguments();

    expect(options.targetPath).toBe('./src');
    expect(options.threshold).toBe(0.3);
    expect(options.reportType).toBe('detailed');
    expect(options.watch).toBe(false);

    process.argv = originalArgv;
  });

  test('should parse custom threshold', () => {
    const originalArgv = process.argv;
    process.argv = ['node', 'quantum-entangle-check', './src', '--threshold', '0.5'];

    const options = parseArguments();

    expect(options.threshold).toBe(0.5);

    process.argv = originalArgv;
  });

  test('should parse report type', () => {
    const originalArgv = process.argv;
    process.argv = ['node', 'quantum-entangle-check', './src', '--report', 'simple'];

    const options = parseArguments();

    expect(options.reportType).toBe('simple');

    process.argv = originalArgv;
  });

  test('should parse watch flag', () => {
    const originalArgv = process.argv;
    process.argv = ['node', 'quantum-entangle-check', './src', '--watch'];

    const options = parseArguments();

    expect(options.watch).toBe(true);

    process.argv = originalArgv;
  });

  test('should throw error for invalid threshold', () => {
    const originalArgv = process.argv;
    process.argv = ['node', 'quantum-entangle-check', './src', '--threshold', '1.5'];

    expect(() => parseArguments()).toThrow();

    process.argv = originalArgv;
  });
});

describe('Report Formatting', () => {
  const mockResult: EntanglementResult = {
    targetPath: './src',
    timestamp: '2024-01-15T10:30:00Z',
    analysisTime: 150,
    totalFiles: 10,
    totalComponents: 8,
    entanglementScore: 0.65,
    entangledPairs: [
      {
        component1: 'UserService',
        component2: 'AuthService',
        score: 0.87,
        type: 'high'
      },
      {
        component1: 'Database',
        component2: 'Cache',
        score: 0.72,
        type: 'high'
      },
      {
        component1: 'Logger',
        component2: 'Config',
        score: 0.45,
        type: 'medium'
      }
    ],
    recommendations: [
      '⚠️  High entanglement detected - consider major refactoring',
      '💡 Implement dependency injection patterns'
    ]
  };

  test('should format simple report', () => {
    const report = formatReport(mockResult, 'simple');

    expect(report).toContain('🔬 Quantum Entanglement Analysis');
    expect(report).toContain('📁 Target: ./src');
    expect(report).toContain('📊 Overall Score: 0.65');
    expect(report).toContain('⚠️  HIGH');
  });

  test('should format detailed report', () => {
    const report = formatReport(mockResult, 'detailed');

    expect(report).toContain('🔬 Quantum Entanglement Analysis Report');
    expect(report).toContain('⚠️  High Entanglement Detected (2 pairs):');
    expect(report).toContain('UserService ↔ AuthService');
    expect(report).toContain('💡 Implement dependency injection patterns');
  });

  test('should format JSON report', () => {
    const report = formatReport(mockResult, 'json');

    const parsed = JSON.parse(report);
    expect(parsed).toEqual(mockResult);
    expect(parsed.entanglementScore).toBe(0.65);
    expect(parsed.entangledPairs.length).toBe(3);
  });
});

// Mock file system for testing
jest.mock('fs', () => ({
  promises: {
    readdir: jest.fn(),
    stat: jest.fn(),
    readFile: jest.fn()
  }
}));

jest.mock('path', () => ({
  join: jest.fn((...args) => args.join('/')),
  basename: jest.fn((path, ext) => {
    const name = path.split('/').pop() || '';
    return ext ? name.replace(ext, '') : name;
  }),
  dirname: jest.fn((path) => path.split('/').slice(0, -1).join('/')),
  extname: jest.fn((path) => '.' + path.split('.').pop()),
  resolve: jest.fn((...args) => args.join('/'))
}));
