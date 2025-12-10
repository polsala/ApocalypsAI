import { QuantumEntanglementChecker } from '../src/quantum-entanglement-checker';
import { Command } from 'commander';

// Mock console.log for testing
const originalLog = console.log;
let loggedOutput: string[] = [];

beforeEach(() => {
  loggedOutput = [];
  console.log = (...args: any[]) => {
    loggedOutput.push(args.join(' '));
  };
});

afterEach(() => {
  console.log = originalLog;
});

describe('QuantumEntanglementChecker', () => {
  let checker: QuantumEntanglementChecker;
  
  beforeEach(() => {
    checker = new QuantumEntanglementChecker();
  });
  
  test('should check entanglement between services', () => {
    const services = ['service-a', 'service-b'];
    const result = checker.checkEntanglement(services);
    
    expect(result).toHaveLength(1);
    expect(result[0]).toHaveProperty('serviceA', 'service-a');
    expect(result[0]).toHaveProperty('serviceB', 'service-b');
    expect(result[0]).toHaveProperty('strength');
    expect(result[0]).toHaveProperty('verified');
    expect(typeof result[0].strength).toBe('number');
    expect(result[0].strength).toBeGreaterThanOrEqual(0.1);
    expect(result[0].strength).toBeLessThanOrEqual(1.0);
  });
  
  test('should throw error for less than 2 services', () => {
    expect(() => {
      checker.checkEntanglement(['service-a']);
    }).toThrow('At least 2 services are required for entanglement checking');
  });
  
  test('should validate quantum states', () => {
    const nodes = ['node-1', 'node-2'];
    const result = checker.validateQuantumStates(nodes);
    
    expect(result).toHaveLength(2);
    expect(result[0]).toHaveProperty('node', 'node-1');
    expect(result[0]).toHaveProperty('consistent');
    expect(result[0]).toHaveProperty('decoherence');
    expect(typeof result[0].consistent).toBe('boolean');
    expect(typeof result[0].decoherence).toBe('number');
  });
  
  test('should simulate entanglement', () => {
    const services = ['service-a', 'service-b'];
    const result = checker.simulateEntanglement(services);
    
    expect(result).toHaveProperty('iterations', 10);
    expect(result).toHaveProperty('averageStrength');
    expect(result).toHaveProperty('maxStrength');
    expect(result).toHaveProperty('minStrength');
    expect(typeof result.averageStrength).toBe('number');
    expect(typeof result.maxStrength).toBe('number');
    expect(typeof result.minStrength).toBe('number');
    expect(result.maxStrength).toBeGreaterThanOrEqual(result.minStrength);
  });
  
  test('should generate spooky quote', () => {
    const quote = checker.generateSpookyQuote();
    expect(typeof quote).toBe('string');
    expect(quote.length).toBeGreaterThan(0);
    expect(quote).toContain('"');
  });
  
  test('should have consistent entanglement calculations', () => {
    const services = ['service-a', 'service-b'];
    const result1 = checker.checkEntanglement(services);
    const result2 = checker.checkEntanglement(services);
    
    // Results should be similar but not identical due to quantum uncertainty
    expect(Math.abs(result1[0].strength - result2[0].strength)).toBeLessThan(0.5);
  });
});

// Mock rationale: We mock console.log to capture CLI output without actually printing to stdout during tests
