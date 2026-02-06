import { findShortestPath } from '../src/utils/graph';

describe('findShortestPath', () => {
  // Mock rationale: These tests are for the pure function `findShortestPath`.
  // We provide various graph structures and expected outcomes to verify its correctness.

  test('should find the shortest path in a simple graph', () => {
    const graph = {
      'A': { 'B': 1, 'C': 4 },
      'B': { 'A': 1, 'D': 2, 'E': 5 },
      'C': { 'A': 4, 'F': 1 },
      'D': { 'B': 2, 'E': 1 },
      'E': { 'B': 5, 'D': 1, 'F': 2 },
      'F': { 'C': 1, 'E': 2 }
    };
    const result = findShortestPath(graph, 'A', 'F');
    expect(result.path).toEqual(['A', 'B', 'D', 'E', 'F']);
    expect(result.distance).toBe(6);
  });

  test('should handle a graph with no path', () => {
    const graph = {
      'A': { 'B': 1 },
      'B': { 'A': 1 },
      'C': { 'D': 1 },
      'D': { 'C': 1 }
    };
    const result = findShortestPath(graph, 'A', 'C');
    expect(result.path).toEqual([]);
    expect(result.distance).toBe(Infinity);
  });

  test('should return path and distance for start and end being the same node', () => {
    const graph = {
      'A': { 'B': 1 },
      'B': { 'A': 1 }
    };
    const result = findShortestPath(graph, 'A', 'A');
    expect(result.path).toEqual(['A']);
    expect(result.distance).toBe(0);
  });

  test('should find shortest path with varying edge weights', () => {
    const graph = {
      '0,0': { '0,1': 1, '1,0': 10 },
      '0,1': { '0,0': 1, '1,1': 1 },
      '1,0': { '0,0': 10, '1,1': 1 },
      '1,1': { '0,1': 1, '1,0': 1 }
    };
    const result = findShortestPath(graph, '0,0', '1,1');
    expect(result.path).toEqual(['0,0', '0,1', '1,1']);
    expect(result.distance).toBe(2);
  });

  test('should handle disconnected nodes correctly', () => {
    const graph = {
      'A': { 'B': 1 },
      'B': { 'A': 1 },
      'C': {},
      'D': {}
    };
    const result = findShortestPath(graph, 'A', 'C');
    expect(result.path).toEqual([]);
    expect(result.distance).toBe(Infinity);
  });

  test('should work with a larger grid-like graph and risk factors', () => {
    // Simulate a 3x3 grid with some costs
    const graph = {
      '0,0': { '0,1': 1, '1,0': 1 },
      '0,1': { '0,0': 1, '0,2': 5, '1,1': 1 }, // 0,2 has high cost
      '0,2': { '0,1': 5, '1,2': 1 },
      '1,0': { '0,0': 1, '1,1': 1, '2,0': 1 },
      '1,1': { '0,1': 1, '1,0': 1, '1,2': 1, '2,1': 1 },
      '1,2': { '0,2': 1, '1,1': 1, '2,2': 1 },
      '2,0': { '1,0': 1, '2,1': 1 },
      '2,1': { '1,1': 1, '2,0': 1, '2,2': 1 },
      '2,2': { '1,2': 1, '2,1': 1 }
    };
    const result = findShortestPath(graph, '0,0', '2,2');
    // Expected path avoiding '0,1' -> '0,2' high cost
    expect(result.path).toEqual(['0,0', '1,0', '1,1', '1,2', '2,2']);
    expect(result.distance).toBe(5);
  });
});
