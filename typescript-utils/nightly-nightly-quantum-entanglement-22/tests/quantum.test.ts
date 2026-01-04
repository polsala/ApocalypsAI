import { describe, it, expect, beforeEach } from '@jest/globals';
import { QuantumNode, EntanglementChecker, QuantumMetrics, EntanglementResult } from '../src/quantum';
import { Logger } from '../src/logger';

// Mock logger to avoid console pollution
const mockLogger = {
  log: jest.fn(),
  warn: jest.fn(),
  error: jest.fn(),
  success: jest.fn(),
  info: jest.fn()
};

describe('Quantum Physics Simulation', () => {
  let checker: EntanglementChecker;
  let nodes: QuantumNode[];

  beforeEach(() => {
    const config = {
      entanglementThreshold: 0.7,
      measurementProbability: 0.1
    };
    checker = new EntanglementChecker(config, mockLogger);
    nodes = [
      new QuantumNode('node-alpha'),
      new QuantumNode('node-beta'),
      new QuantumNode('node-gamma')
    ];
  });

  it('should calculate quantum metrics correctly', () => {
    const node = new QuantumNode('test-node');
    const metrics = (checker as any).calculateMetrics(node);
    
    expect(metrics).toHaveProperty('entanglementFidelity');
    expect(metrics).toHaveProperty('coherenceTime');
    expect(metrics).toHaveProperty('bellInequalityViolation');
    expect(metrics).toHaveProperty('quantumVolume');
    
    expect(metrics.entanglementFidelity).toBeGreaterThanOrEqual(0);
    expect(metrics.entanglementFidelity).toBeLessThanOrEqual(1);
    expect(metrics.coherenceTime).toBeGreaterThanOrEqual(0);
    expect(typeof metrics.bellInequalityViolation).toBe('boolean');
    expect(metrics.quantumVolume).toBeGreaterThanOrEqual(1);
  });

  it('should evaluate entanglement correctly', () => {
    const node = new QuantumNode('test-node');
    const metrics = {
      entanglementFidelity: 0.8,
      coherenceTime: 50,
      bellInequalityViolation: true,
      quantumVolume: 8
    };
    
    const result = (checker as any).evaluateEntanglement(metrics);
    expect(result).toBe(true);
    
    // Test with low fidelity
    const badMetrics = {
      ...metrics,
      entanglementFidelity: 0.5
    };
    const badResult = (checker as any).evaluateEntanglement(badMetrics);
    expect(badResult).toBe(false);
  });

  it('should generate appropriate descriptions', () => {
    const node = new QuantumNode('test-node');
    const metrics = {
      entanglementFidelity: 0.9,
      coherenceTime: 75,
      bellInequalityViolation: true,
      quantumVolume: 16
    };
    
    const successDescription = (checker as any).generateDescription(node, true, metrics);
    expect(successDescription).toContain('Entangled');
    expect(successDescription).toContain('fidelity');
    expect(successDescription).toContain('coherence');
    
    const failureDescription = (checker as any).generateDescription(node, false, metrics);
    expect(failureDescription).toContain('No entanglement');
  });

  it('should calculate system health correctly', () => {
    const mockResults: EntanglementResult[] = [
      {
        success: true,
        description: 'Test',
        metrics: {
          entanglementFidelity: 0.9,
          coherenceTime: 100,
          bellInequalityViolation: true,
          quantumVolume: 32
        }
      },
      {
        success: false,
        description: 'Test',
        metrics: {
          entanglementFidelity: 0.3,
          coherenceTime: 5,
          bellInequalityViolation: false,
          quantumVolume: 2
        }
      }
    ];
    
    const health = checker.calculateSystemHealth(mockResults);
    expect(health).toBeGreaterThanOrEqual(0);
    expect(health).toBeLessThanOrEqual(100);
    expect(typeof health).toBe('number');
  });

  it('should handle entanglement verification', async () => {
    const results = await checker.verifyEntanglement(nodes);
    
    expect(results).toHaveLength(nodes.length);
    results.forEach(result => {
      expect(result).toHaveProperty('success');
      expect(result).toHaveProperty('description');
      expect(result).toHaveProperty('metrics');
      expect(typeof result.success).toBe('boolean');
      expect(typeof result.description).toBe('string');
      expect(result.metrics).toHaveProperty('entanglementFidelity');
    });
  });

  it('should simulate entanglement between nodes', () => {
    const nodeA = nodes[0];
    const nodeB = nodes[1];
    
    nodeA.entangleWith(nodeB);
    
    if (nodeA.isCurrentlyEntangled()) {
      expect(nodeA.getQuantumState()).toBe(nodeB.getQuantumState());
      expect(nodeA.getCoherenceTime()).toBe(nodeB.getCoherenceTime());
      expect(nodeA.getCoherenceTime()).toBeGreaterThan(0);
    }
  });

  it('should handle quantum measurement correctly', () => {
    const node = nodes[0];
    const originalState = node.getQuantumState();
    
    const measurement1 = node.measure();
    const measurement2 = node.measure();
    
    // Measurements should be close to original but may vary slightly due to noise
    expect(measurement1).toBeGreaterThanOrEqual(0);
    expect(measurement1).toBeLessThanOrEqual(1);
    expect(measurement2).toBeGreaterThanOrEqual(0);
    expect(measurement2).toBeLessThanOrEqual(1);
    
    // Multiple measurements should be consistent
    expect(Math.abs(measurement1 - measurement2)).toBeLessThan(0.2);
  });

  it('should simulate decoherence correctly', () => {
    const node = nodes[0];
    node.entangleWith(nodes[1]);
    
    if (node.getCoherenceTime() > 0) {
      const initialCoherence = node.getCoherenceTime();
      
      // Simulate multiple decoherence events
      for (let i = 0; i < 20; i++) {
        node.simulateDecoherence();
      }
      
      expect(node.getCoherenceTime()).toBeLessThanOrEqual(initialCoherence);
      expect(node.getCoherenceTime()).toBe(0);
      expect(node.isCurrentlyEntangled()).toBe(false);
    }
  });
});
