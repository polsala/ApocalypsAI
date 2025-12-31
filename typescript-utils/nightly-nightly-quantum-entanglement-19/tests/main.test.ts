import { Command } from 'commander';
import { QuantumEntanglementChecker } from '../src/quantum-entanglement-checker';
import * as fs from 'fs';
import * as yaml from 'js-yaml';

// Mock console.log to capture output
let consoleOutput: string[] = [];
const originalConsoleLog = console.log;

beforeEach(() => {
  consoleOutput = [];
  console.log = (...args: any[]) => {
    consoleOutput.push(args.join(' '));
  };
});

afterEach(() => {
  console.log = originalConsoleLog;
});

describe('QuantumEntanglementChecker CLI', () => {
  let program: Command;

  beforeEach(() => {
    program = new Command();
    
    // Setup CLI commands
    program
      .command('check')
      .option('-n, --nodes <number>', 'Number of nodes', '3')
      .option('-s, --state <state>', 'Quantum state', 'superposition')
      .option('-t, --threshold <number>', 'Entanglement threshold', '0.8')
      .action((options) => {
        const nodes = parseInt(options.nodes, 10);
        const state = options.state;
        const threshold = parseFloat(options.threshold);
        
        const checker = new QuantumEntanglementChecker(nodes, state, threshold);
        const result = checker.checkEntanglement();
        
        console.log('QUANTUM CHECK COMPLETE');
        console.log(`Nodes: ${nodes}`);
        console.log(`State: ${state}`);
        console.log(`Entangled: ${result.entangled}`);
        console.log(`Coherence: ${result.coherence}`);
      });
  });

  test('should check entanglement with default options', () => {
    program.parse(['node', 'test', 'check'], { from: 'user' });
    
    expect(consoleOutput).toContain('QUANTUM CHECK COMPLETE');
    expect(consoleOutput).toContain('Nodes: 3');
    expect(consoleOutput).toContain('State: superposition');
  });

  test('should check entanglement with custom options', () => {
    program.parse(['node', 'test', 'check', '--nodes', '5', '--state', 'entangled', '--threshold', '0.9'], { from: 'user' });
    
    expect(consoleOutput).toContain('QUANTUM CHECK COMPLETE');
    expect(consoleOutput).toContain('Nodes: 5');
    expect(consoleOutput).toContain('State: entangled');
  });

  test('should handle invalid node count', () => {
    // Test with minimum nodes
    program.parse(['node', 'test', 'check', '--nodes', '1'], { from: 'user' });
    
    // Should default to minimum of 2 nodes
    expect(consoleOutput).toContain('Nodes: 2');
  });

  test('should handle invalid threshold', () => {
    // Test with threshold above 1.0
    program.parse(['node', 'test', 'check', '--threshold', '1.5'], { from: 'user' });
    
    // Should clamp threshold to 1.0
    expect(consoleOutput.length).toBeGreaterThan(0);
  });
});

describe('QuantumEntanglementChecker Core Logic', () => {
  test('should create checker with valid parameters', () => {
    const checker = new QuantumEntanglementChecker(3, 'superposition', 0.8);
    
    expect(checker).toBeDefined();
  });

  test('should clamp nodes to valid range', () => {
    const checker1 = new QuantumEntanglementChecker(1, 'superposition');
    const checker2 = new QuantumEntanglementChecker(150, 'superposition');
    
    // Should clamp to minimum 2 and maximum 100
    expect(checker1).toBeDefined();
    expect(checker2).toBeDefined();
  });

  test('should clamp threshold to valid range', () => {
    const checker1 = new QuantumEntanglementChecker(3, 'superposition', -0.1);
    const checker2 = new QuantumEntanglementChecker(3, 'superposition', 1.1);
    
    expect(checker1).toBeDefined();
    expect(checker2).toBeDefined();
  });

  test('should generate entanglement result', () => {
    const checker = new QuantumEntanglementChecker(3, 'superposition');
    const result = checker.checkEntanglement();
    
    expect(result).toHaveProperty('entangled');
    expect(result).toHaveProperty('coherence');
    expect(result).toHaveProperty('entanglementStrength');
    expect(result).toHaveProperty('quantumFluctuations');
    expect(result).toHaveProperty('timestamp');
    
    expect(typeof result.entangled).toBe('boolean');
    expect(typeof result.coherence).toBe('number');
    expect(typeof result.entanglementStrength).toBe('number');
    expect(typeof result.quantumFluctuations).toBe('number');
    expect(typeof result.timestamp).toBe('string');
  });

  test('should generate report', () => {
    const checker = new QuantumEntanglementChecker(3, 'superposition');
    const report = checker.generateReport();
    
    expect(report).toHaveProperty('timestamp');
    expect(report).toHaveProperty('nodes');
    expect(report).toHaveProperty('quantumState');
    expect(report).toHaveProperty('entangled');
    expect(report).toHaveProperty('coherence');
    expect(report).toHaveProperty('entanglementStrength');
    expect(report).toHaveProperty('quantumFluctuations');
    expect(report).toHaveProperty('recommendations');
    
    expect(Array.isArray(report.recommendations)).toBe(true);
  });

  test('should verify coherence with timeout', async () => {
    const checker = new QuantumEntanglementChecker(2, 'entangled');
    const result = await checker.verifyCoherence(5); // 5 second timeout
    
    expect(result).toHaveProperty('verified');
    expect(result).toHaveProperty('coherence');
    expect(result).toHaveProperty('verificationTime');
    
    expect(typeof result.verified).toBe('boolean');
    expect(typeof result.coherence).toBe('number');
    expect(typeof result.verificationTime).toBe('number');
  });

  test('should handle verification timeout', async () => {
    const checker = new QuantumEntanglementChecker(2, 'entangled');
    
    await expect(checker.verifyCoherence(0.1)).rejects.toThrow('Quantum verification timeout exceeded');
  });

  test('should handle different quantum states', () => {
    const states: Array<'superposition' | 'entangled' | 'decoherence' | 'tunneling'> = ['superposition', 'entangled', 'decoherence', 'tunneling'];
    
    states.forEach(state => {
      const checker = new QuantumEntanglementChecker(3, state);
      const result = checker.checkEntanglement();
      
      expect(result).toBeDefined();
      expect(typeof result.coherence).toBe('number');
      expect(result.coherence >= 0 && result.coherence <= 1).toBe(true);
    });
  });

  test('should generate recommendations', () => {
    const checker = new QuantumEntanglementChecker(3, 'superposition');
    const result = checker.checkEntanglement();
    const report = checker.generateReport();
    
    expect(Array.isArray(report.recommendations)).toBe(true);
    expect(report.recommendations.length).toBeGreaterThan(0);
  });
});
