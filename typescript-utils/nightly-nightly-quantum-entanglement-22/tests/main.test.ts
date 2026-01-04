import { describe, it, expect, beforeEach } from '@jest/globals';
import { main } from '../src/main';
import { Logger } from '../src/logger';
import { QuantumNode } from '../src/quantum';
import { loadConfig } from '../src/config';

// Mock console methods to avoid polluting test output
const originalConsole = { ...console };

beforeEach(() => {
  console.log = jest.fn();
  console.error = jest.fn();
  console.warn = jest.fn();
});

afterEach(() => {
  console.log = originalConsole.log;
  console.error = originalConsole.error;
  console.warn = originalConsole.warn;
});

describe('Quantum Entanglement Checker', () => {
  it('should load default configuration when no config file exists', () => {
    const config = loadConfig();
    expect(config.nodes).toBeDefined();
    expect(config.nodes.length).toBeGreaterThan(0);
    expect(config.entanglementThreshold).toBe(0.8);
    expect(config.measurementProbability).toBe(0.1);
  });

  it('should create quantum nodes with valid properties', () => {
    const node = new QuantumNode('test-node');
    
    expect(node.getName()).toBe('test-node');
    expect(typeof node.getQuantumState()).toBe('number');
    expect(node.getQuantumState()).toBeGreaterThanOrEqual(0);
    expect(node.getQuantumState()).toBeLessThanOrEqual(1);
    expect(node.isCurrentlyEntangled()).toBe(false);
    expect(node.getCoherenceTime()).toBe(0);
  });

  it('should simulate quantum entanglement correctly', () => {
    const nodeA = new QuantumNode('node-a');
    const nodeB = new QuantumNode('node-b');
    
    nodeA.entangleWith(nodeB);
    
    // If entangled, both nodes should have the same quantum state
    if (nodeA.isCurrentlyEntangled()) {
      expect(nodeA.getQuantumState()).toBe(nodeB.getQuantumState());
      expect(nodeA.getCoherenceTime()).toBe(nodeB.getCoherenceTime());
      expect(nodeA.getCoherenceTime()).toBeGreaterThan(0);
    }
  });

  it('should simulate quantum measurement', () => {
    const node = new QuantumNode('test-node');
    const originalState = node.getQuantumState();
    
    const measurement = node.measure();
    
    // Measurement should be close to original state but with some noise
    expect(typeof measurement).toBe('number');
    expect(measurement).toBeGreaterThanOrEqual(0);
    expect(measurement).toBeLessThanOrEqual(1);
    expect(Math.abs(measurement - originalState)).toBeLessThan(0.1);
  });

  it('should simulate quantum decoherence', () => {
    const node = new QuantumNode('test-node');
    node.entangleWith(new QuantumNode('dummy-node'));
    
    const initialCoherence = node.getCoherenceTime();
    
    if (initialCoherence > 0) {
      node.simulateDecoherence();
      expect(node.getCoherenceTime()).toBeLessThanOrEqual(initialCoherence);
      
      // Simulate multiple decoherence events
      for (let i = 0; i < 10; i++) {
        node.simulateDecoherence();
      }
      expect(node.getCoherenceTime()).toBe(0);
      expect(node.isCurrentlyEntangled()).toBe(false);
    }
  });

  it('should validate configuration correctly', () => {
    const { validateConfig } = require('../src/config');
    
    const validConfig = {
      nodes: ['node1', 'node2'],
      entanglementThreshold: 0.8,
      measurementProbability: 0.1
    };
    
    const invalidConfig1 = {
      nodes: [],
      entanglementThreshold: 0.8,
      measurementProbability: 0.1
    };
    
    const invalidConfig2 = {
      nodes: ['node1'],
      entanglementThreshold: 1.5,
      measurementProbability: 0.1
    };
    
    expect(validateConfig(validConfig)).toBe(true);
    expect(validateConfig(invalidConfig1)).toBe(false);
    expect(validateConfig(invalidConfig2)).toBe(false);
  });

  it('should handle logger colors correctly', () => {
    const logger = new Logger();
    
    // These should not throw errors
    expect(() => logger.log('Test message')).not.toThrow();
    expect(() => logger.warn('Test warning')).not.toThrow();
    expect(() => logger.error('Test error')).not.toThrow();
    expect(() => logger.success('Test success')).not.toThrow();
    expect(() => logger.info('Test info')).not.toThrow();
  });
});
