import { QuantumEntanglementChecker } from '../src/checker';
import { BellStateAnalyzer } from '../src/bell-analyzer';
import { QuantumMonitor } from '../src/monitor';
import { QuantumMetrics } from '../src/metrics';
import { loadConfig, getDefaultConfig } from '../src/config';

// Mock console.log to capture output
const originalConsoleLog = console.log;
const originalConsoleError = console.error;

beforeEach(() => {
  console.log = jest.fn();
  console.error = jest.fn();
});

afterEach(() => {
  console.log = originalConsoleLog;
  console.error = originalConsoleError;
});

describe('QuantumEntanglementChecker', () => {
  let checker: QuantumEntanglementChecker;

  beforeEach(() => {
    checker = new QuantumEntanglementChecker(getDefaultConfig());
  });

  test('should check entanglement for multiple components', async () => {
    const components = ['service-a', 'service-b', 'service-c'];
    const result = await checker.checkEntanglement(components);

    expect(result).toHaveProperty('fidelity');
    expect(result).toHaveProperty('entangled');
    expect(result).toHaveProperty('decoherenceRisk');
    expect(result).toHaveProperty('recommendations');
    expect(result).toHaveProperty('correlationMatrix');
    expect(result).toHaveProperty('bellState');
    expect(result).toHaveProperty('superpositionStates');

    expect(typeof result.fidelity).toBe('number');
    expect(result.fidelity).toBeGreaterThanOrEqual(0);
    expect(result.fidelity).toBeLessThanOrEqual(1);
    expect(typeof result.entangled).toBe('boolean');
    expect(typeof result.decoherenceRisk).toBe('string');
    expect(typeof result.recommendations).toBe('string');
    expect(Array.isArray(result.correlationMatrix)).toBe(true);
    expect(typeof result.bellState).toBe('string');
    expect(typeof result.superpositionStates).toBe('number');
  });

  test('should throw error for less than 2 components', async () => {
    await expect(checker.checkEntanglement(['single'])).rejects.toThrow(
      'At least 2 components required for entanglement check'
    );
  });

  test('should respect custom threshold', async () => {
    const components = ['service-a', 'service-b'];
    const result = await checker.checkEntanglement(components, 0.9);

    // With high threshold, entanglement might fail
    expect(result).toHaveProperty('fidelity');
    expect(result).toHaveProperty('entangled');
  });
});

describe('BellStateAnalyzer', () => {
  let analyzer: BellStateAnalyzer;

  beforeEach(() => {
    analyzer = new BellStateAnalyzer(getDefaultConfig());
  });

  test('should verify Bell states for component pairs', async () => {
    const pairs = ['service-a:service-b', 'service-c:service-d'];
    const results = await analyzer.verifyBellStates(pairs, 'phi_plus');

    expect(Array.isArray(results)).toBe(true);
    expect(results).toHaveLength(2);

    results.forEach(result => {
      expect(result).toHaveProperty('fidelity');
      expect(result).toHaveProperty('verified');
      expect(result).toHaveProperty('bellInequality');
      expect(result).toHaveProperty('correlation');
      expect(result).toHaveProperty('recommendations');

      expect(typeof result.fidelity).toBe('number');
      expect(result.fidelity).toBeGreaterThanOrEqual(0);
      expect(result.fidelity).toBeLessThanOrEqual(1);
      expect(typeof result.verified).toBe('boolean');
      expect(typeof result.bellInequality).toBe('number');
      expect(typeof result.correlation).toBe('number');
      expect(Array.isArray(result.recommendations)).toBe(true);
    });
  });

  test('should handle invalid pair format', async () => {
    await expect(analyzer.verifyBellStates(['invalid-pair'], 'phi_plus'))
      .rejects.toThrow('Invalid pair format: invalid-pair. Use component1:component2');
  });

  test('should work with different Bell states', async () => {
    const pairs = ['service-a:service-b'];
    const states = ['phi_plus', 'phi_minus', 'psi_plus', 'psi_minus'];

    for (const state of states) {
      const results = await analyzer.verifyBellStates(pairs, state);
      expect(results).toHaveLength(1);
      expect(results[0]).toHaveProperty('fidelity');
    }
  });
});

describe('QuantumMetrics', () => {
  let metrics: QuantumMetrics;

  beforeEach(() => {
    metrics = new QuantumMetrics(getDefaultConfig());
  });

  test('should generate metrics for components', async () => {
    const result = await metrics.generateMetrics('test-service', 1.0);

    expect(Array.isArray(result)).toBe(true);
    expect(result).toHaveLength(10);

    result.forEach(metric => {
      expect(typeof metric).toBe('number');
      expect(metric).toBeGreaterThanOrEqual(0);
      expect(metric).toBeLessThanOrEqual(1);
    });
  });

  test('should generate different metrics for different components', async () => {
    const metrics1 = await metrics.generateMetrics('service-a', 1.0);
    const metrics2 = await metrics.generateMetrics('service-b', 1.0);

    // Metrics should be different due to component name hashing
    expect(metrics1).not.toEqual(metrics2);
  });

  test('should analyze system metrics', async () => {
    const result = await metrics.analyzeSystem(['cpu', 'memory'], 0.8);

    expect(result).toHaveProperty('systemFidelity');
    expect(result).toHaveProperty('coherence');
    expect(result).toHaveProperty('entanglementQuality');
    expect(result).toHaveProperty('decoherenceEvents');
    expect(result).toHaveProperty('superpositionStates');
    expect(result).toHaveProperty('recommendations');

    expect(typeof result.systemFidelity).toBe('number');
    expect(result.systemFidelity).toBeGreaterThanOrEqual(0);
    expect(result.systemFidelity).toBeLessThanOrEqual(1);
    expect(typeof result.coherence).toBe('number');
    expect(result.coherence).toBeGreaterThanOrEqual(0);
    expect(result.coherence).toBeLessThanOrEqual(1);
    expect(typeof result.entanglementQuality).toBe('string');
    expect(typeof result.decoherenceEvents).toBe('number');
    expect(typeof result.superpositionStates).toBe('number');
    expect(Array.isArray(result.recommendations)).toBe(true);
  });
});

describe('QuantumMonitor', () => {
  let monitor: QuantumMonitor;

  beforeEach(() => {
    monitor = new QuantumMonitor(getDefaultConfig());
  });

  test('should create monitor instance', () => {
    expect(monitor).toBeInstanceOf(QuantumMonitor);
  });

  test('should stop monitoring when requested', () => {
    // This test verifies the stopMonitoring method works
    monitor.stopMonitoring();
    expect(monitor['isMonitoring']).toBe(false);
    expect(monitor['monitoringInterval']).toBeNull();
  });
});

describe('Configuration', () => {
  test('should load default config when no file exists', () => {
    const config = loadConfig('/nonexistent/path/quantum.config.json');
    const defaultConfig = getDefaultConfig();

    expect(config).toEqual(defaultConfig);
  });

  test('should validate config correctly', () => {
    const validConfig = getDefaultConfig();
    const errors = require('../src/config').validateConfig(validConfig);
    expect(errors).toHaveLength(0);

    const invalidConfig = {
      ...validConfig,
      entanglement: {
        ...validConfig.entanglement,
        threshold: 1.5 // Invalid
      }
    };

    const invalidErrors = require('../src/config').validateConfig(invalidConfig);
    expect(invalidErrors.length).toBeGreaterThan(0);
    expect(invalidErrors[0]).toContain('entanglement.threshold must be between 0 and 1');
  });
});

describe('Integration Tests', () => {
  test('should work together: checker -> metrics -> config', async () => {
    const config = getDefaultConfig();
    const checker = new QuantumEntanglementChecker(config);
    const metrics = new QuantumMetrics(config);

    // Generate metrics
    const componentMetrics = await metrics.generateMetrics('test-service');
    expect(componentMetrics).toHaveLength(10);

    // Use metrics in checker
    const result = await checker.checkEntanglement(['test-service', 'other-service']);
    expect(result).toHaveProperty('fidelity');
    expect(result).toHaveProperty('entangled');
  });

  test('should handle Bell state verification with different configurations', async () => {
    const config = getDefaultConfig();
    const analyzer = new BellStateAnalyzer(config);

    const pairs = ['service-a:service-b'];
    const states = ['phi_plus', 'phi_minus', 'psi_plus', 'psi_minus'];

    for (const state of states) {
      const results = await analyzer.verifyBellStates(pairs, state);
      expect(results).toHaveLength(1);
      expect(results[0].fidelity).toBeGreaterThanOrEqual(0);
      expect(results[0].fidelity).toBeLessThanOrEqual(1);
    }
  });
});
