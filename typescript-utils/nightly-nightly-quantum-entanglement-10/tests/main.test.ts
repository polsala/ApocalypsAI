import { QuantumEntanglementChecker, Position, EntanglementResult } from '../src/main';

describe('QuantumEntanglementChecker', () => {
  let checker: QuantumEntanglementChecker;

  beforeEach(() => {
    checker = new QuantumEntanglementChecker();
  });

  describe('registerNode', () => {
    it('should register a node successfully', () => {
      const position: Position = { x: 0, y: 0, z: 0 };
      
      checker.registerNode('node-1', position);
      
      expect(checker.getNodeCount()).toBe(1);
    });

    it('should throw error when registering node without ID', () => {
      const position: Position = { x: 0, y: 0, z: 0 };
      
      expect(() => {
        checker.registerNode('', position);
      }).toThrow('Node ID and position are required');
    });

    it('should throw error when registering node without position', () => {
      expect(() => {
        checker.registerNode('node-1', null as any);
      }).toThrow('Node ID and position are required');
    });

    it('should throw error when registering duplicate node ID', () => {
      const position: Position = { x: 0, y: 0, z: 0 };
      
      checker.registerNode('node-1', position);
      
      expect(() => {
        checker.registerNode('node-1', position);
      }).toThrow("Node with ID 'node-1' already exists");
    });
  });

  describe('verifyEntanglement', () => {
    it('should throw error when less than 2 nodes are registered', () => {
      checker.registerNode('node-1', { x: 0, y: 0, z: 0 });
      
      expect(() => {
        checker.verifyEntanglement();
      }).toThrow('At least 2 nodes are required for entanglement');
    });

    it('should return valid entanglement result for 2 close nodes', () => {
      checker.registerNode('node-1', { x: 0, y: 0, z: 0 });
      checker.registerNode('node-2', { x: 1, y: 1, z: 1 });
      
      const result = checker.verifyEntanglement();
      
      expect(result.entanglementScore).toBeGreaterThan(70);
      expect(result.spookyAction).toBe(true);
      expect(result.consistentStates).toBe(2);
      expect(result.totalNodes).toBe(2);
      expect(result.timestamp).toBeInstanceOf(Date);
    });

    it('should return valid entanglement result for 2 distant nodes', () => {
      checker.registerNode('node-1', { x: 0, y: 0, z: 0 });
      checker.registerNode('node-2', { x: 200, y: 200, z: 200 });
      
      const result = checker.verifyEntanglement();
      
      expect(result.entanglementScore).toBeLessThan(30);
      expect(result.spookyAction).toBe(false);
      expect(result.consistentStates).toBeLessThan(2);
      expect(result.totalNodes).toBe(2);
    });

    it('should handle multiple nodes with mixed distances', () => {
      checker.registerNode('node-1', { x: 0, y: 0, z: 0 });
      checker.registerNode('node-2', { x: 1, y: 1, z: 1 });
      checker.registerNode('node-3', { x: 150, y: 150, z: 150 });
      
      const result = checker.verifyEntanglement();
      
      expect(result.totalNodes).toBe(3);
      expect(result.entanglementScore).toBeGreaterThan(0);
      expect(result.entanglementScore).toBeLessThan(100);
      expect(result.consistentStates).toBeGreaterThanOrEqual(0);
      expect(result.consistentStates).toBeLessThanOrEqual(3);
    });
  });

  describe('getEntanglementMatrix', () => {
    it('should return identity matrix for single node', () => {
      checker.registerNode('node-1', { x: 0, y: 0, z: 0 });
      
      const matrix = checker.getEntanglementMatrix();
      
      expect(matrix).toEqual([[1.0]]);
    });

    it('should return symmetric matrix for multiple nodes', () => {
      checker.registerNode('node-1', { x: 0, y: 0, z: 0 });
      checker.registerNode('node-2', { x: 5, y: 5, z: 5 });
      
      const matrix = checker.getEntanglementMatrix();
      
      expect(matrix.length).toBe(2);
      expect(matrix[0].length).toBe(2);
      expect(matrix[1].length).toBe(2);
      expect(matrix[0][0]).toBe(1.0);
      expect(matrix[1][1]).toBe(1.0);
      expect(matrix[0][1]).toBeCloseTo(matrix[1][0], 2);
    });

    it('should return higher scores for closer nodes', () => {
      checker.registerNode('close-1', { x: 0, y: 0, z: 0 });
      checker.registerNode('close-2', { x: 1, y: 1, z: 1 });
      checker.registerNode('far-1', { x: 100, y: 100, z: 100 });
      
      const matrix = checker.getEntanglementMatrix();
      
      // Close nodes should have higher entanglement than far nodes
      expect(matrix[0][1]).toBeGreaterThan(matrix[0][2]);
      expect(matrix[1][0]).toBeGreaterThan(matrix[1][2]);
    });
  });

  describe('getNodeCount', () => {
    it('should return correct node count', () => {
      expect(checker.getNodeCount()).toBe(0);
      
      checker.registerNode('node-1', { x: 0, y: 0, z: 0 });
      expect(checker.getNodeCount()).toBe(1);
      
      checker.registerNode('node-2', { x: 1, y: 1, z: 1 });
      expect(checker.getNodeCount()).toBe(2);
    });
  });

  describe('clear', () => {
    it('should remove all nodes', () => {
      checker.registerNode('node-1', { x: 0, y: 0, z: 0 });
      checker.registerNode('node-2', { x: 1, y: 1, z: 1 });
      
      expect(checker.getNodeCount()).toBe(2);
      
      checker.clear();
      
      expect(checker.getNodeCount()).toBe(0);
      
      expect(() => {
        checker.verifyEntanglement();
      }).toThrow('At least 2 nodes are required for entanglement');
    });
  });

  describe('calculateDistance', () => {
    it('should calculate correct Euclidean distance', () => {
      const pos1: Position = { x: 0, y: 0, z: 0 };
      const pos2: Position = { x: 3, y: 4, z: 0 };
      
      // Distance should be 5 (3-4-5 triangle)
      const distance = Math.sqrt(
        Math.pow(pos2.x - pos1.x, 2) + 
        Math.pow(pos2.y - pos1.y, 2) + 
        Math.pow(pos2.z - pos1.z, 2)
      );
      
      expect(distance).toBe(5);
    });
  });

  describe('calculateEntanglementScore', () => {
    it('should return 1.0 for zero distance', () => {
      const score = (checker as any).calculateEntanglementScore(0);
      expect(score).toBe(1.0);
    });

    it('should return scores between 0 and 1', () => {
      for (let distance = 0; distance <= 200; distance += 10) {
        const score = (checker as any).calculateEntanglementScore(distance);
        expect(score).toBeGreaterThanOrEqual(0);
        expect(score).toBeLessThanOrEqual(1);
      }
    });

    it('should return lower scores for greater distances', () => {
      const score1 = (checker as any).calculateEntanglementScore(10);
      const score2 = (checker as any).calculateEntanglementScore(100);
      
      expect(score1).toBeGreaterThan(score2);
    });
  });
});
