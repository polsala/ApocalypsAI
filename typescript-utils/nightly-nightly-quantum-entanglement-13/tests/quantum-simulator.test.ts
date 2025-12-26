import { QuantumSimulator } from '../src/quantum-simulator';
import { QuantumState, ComponentAnalysis } from '../src/types';
import { DependencyGraph } from '../src/dependency-graph';

describe('QuantumSimulator', () => {
  let simulator: QuantumSimulator;
  let mockComponents: ComponentAnalysis[];
  let mockDependencyGraph: DependencyGraph;

  beforeEach(() => {
    simulator = new QuantumSimulator();
    mockComponents = [
      {
        name: 'UserService',
        filePath: './src/services/user.service.ts',
        dependencies: ['AuthService', 'Database'],
        linesOfCode: 150,
        complexity: 25
      },
      {
        name: 'AuthService',
        filePath: './src/services/auth.service.ts',
        dependencies: ['Database', 'Logger'],
        linesOfCode: 120,
        complexity: 20
      },
      {
        name: 'Database',
        filePath: './src/database.ts',
        dependencies: [],
        linesOfCode: 200,
        complexity: 40
      }
    ];

    mockDependencyGraph = new DependencyGraph();
    mockDependencyGraph.buildGraph(mockComponents);
  });

  test('should simulate quantum states for components', () => {
    const states = simulator.simulateStates(mockComponents, mockDependencyGraph);

    expect(states).toHaveLength(3);
    expect(states[0].componentName).toBe('UserService');
    expect(states[0].dependencies).toEqual(['AuthService', 'Database']);
    expect(states[0].quantumSignature).toHaveLength(10);
    expect(typeof states[0].coherenceLevel).toBe('number');
    expect(states[0].entanglementHistory).toEqual([]);
  });

  test('should generate consistent quantum signatures', () => {
    const states1 = simulator.simulateStates(mockComponents, mockDependencyGraph);
    const states2 = simulator.simulateStates(mockComponents, mockDependencyGraph);

    // Signatures should be deterministic for the same input
    expect(states1[0].quantumSignature).toEqual(states2[0].quantumSignature);
  });

  test('should calculate interference between quantum states', () => {
    const state1 = [0.1, 0.2, 0.3, 0.4, 0.5];
    const state2 = [0.2, 0.3, 0.4, 0.5, 0.6];

    const interference = simulator.calculateInterference(state1, state2);

    expect(typeof interference).toBe('number');
    expect(interference).toBeGreaterThanOrEqual(0);
    expect(interference).toBeLessThanOrEqual(1);
  });

  test('should simulate entanglement decay over time', () => {
    const states = simulator.simulateStates(mockComponents, mockDependencyGraph);
    const decayedStates = simulator.simulateEntanglementDecay(states, 5);

    expect(decayedStates).toHaveLength(states.length);

    states.forEach((original, index) => {
      const decayed = decayedStates[index];
      expect(decayed.coherenceLevel).toBeLessThanOrEqual(original.coherenceLevel);
      expect(decayed.entanglementHistory).toContain(`t=5`);
    });
  });

  test('should handle empty component list', () => {
    const states = simulator.simulateStates([], mockDependencyGraph);

    expect(states).toHaveLength(0);
  });

  test('should handle components with no dependencies', () => {
    const singleComponent: ComponentAnalysis[] = [
      {
        name: 'Standalone',
        filePath: './src/standalone.ts',
        dependencies: [],
        linesOfCode: 50,
        complexity: 5
      }
    ];

    const states = simulator.simulateStates(singleComponent, mockDependencyGraph);

    expect(states).toHaveLength(1);
    expect(states[0].dependencies).toEqual([]);
    expect(states[0].coherenceLevel).toBeGreaterThan(0);
  });
});
