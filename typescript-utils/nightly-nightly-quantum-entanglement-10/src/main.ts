export interface Position {
  x: number;
  y: number;
  z: number;
}

export interface EntanglementResult {
  entanglementScore: number;
  spookyAction: boolean;
  consistentStates: number;
  totalNodes: number;
  timestamp: Date;
}

export class QuantumEntanglementChecker {
  private nodes: Map<string, Position> = new Map();
  private readonly MAX_ENTANGLEMENT_DISTANCE = 100;
  private readonly QUANTUM_THRESHOLD = 0.7;

  /**
   * Registers a node in the quantum network
   * @param id Unique identifier for the node
   * @param position 3D coordinates of the node
   */
  registerNode(id: string, position: Position): void {
    if (!id || !position) {
      throw new Error('Node ID and position are required');
    }
    
    if (this.nodes.has(id)) {
      throw new Error(`Node with ID '${id}' already exists`);
    }
    
    this.nodes.set(id, position);
  }

  /**
   * Verifies quantum entanglement across all registered nodes
   * @returns Entanglement verification result
   */
  verifyEntanglement(): EntanglementResult {
    const nodeCount = this.nodes.size;
    
    if (nodeCount < 2) {
      throw new Error('At least 2 nodes are required for entanglement');
    }

    const entanglementMatrix = this.getEntanglementMatrix();
    const entanglementScores = entanglementMatrix.map(row => 
      row.reduce((sum, score) => sum + score, 0) / row.length
    );
    
    const averageScore = entanglementScores.reduce((sum, score) => sum + score, 0) / entanglementScores.length;
    const entanglementScore = Math.min(100, Math.max(0, Math.round(averageScore * 100)));
    
    const consistentStates = entanglementScores.filter(score => score >= this.QUANTUM_THRESHOLD).length;
    const spookyAction = entanglementScore > 50;

    return {
      entanglementScore,
      spookyAction,
      consistentStates,
      totalNodes: nodeCount,
      timestamp: new Date()
    };
  }

  /**
   * Returns the entanglement matrix showing connection strengths between nodes
   * @returns 2D array of entanglement scores between nodes (0.0 to 1.0)
   */
  getEntanglementMatrix(): number[][] {
    const nodeIds = Array.from(this.nodes.keys());
    const matrix: number[][] = [];

    for (let i = 0; i < nodeIds.length; i++) {
      matrix[i] = [];
      for (let j = 0; j < nodeIds.length; j++) {
        if (i === j) {
          matrix[i][j] = 1.0; // Perfect entanglement with self
        } else {
          const distance = this.calculateDistance(
            this.nodes.get(nodeIds[i])!,
            this.nodes.get(nodeIds[j])!
          );
          matrix[i][j] = this.calculateEntanglementScore(distance);
        }
      }
    }

    return matrix;
  }

  /**
   * Calculates Euclidean distance between two positions
   * @param pos1 First position
   * @param pos2 Second position
   * @returns Distance between positions
   */
  private calculateDistance(pos1: Position, pos2: Position): number {
    const dx = pos2.x - pos1.x;
    const dy = pos2.y - pos1.y;
    const dz = pos2.z - pos1.z;
    
    return Math.sqrt(dx * dx + dy * dy + dz * dz);
  }

  /**
   * Calculates entanglement score based on distance
   * Closer nodes have higher entanglement scores
   * @param distance Distance between nodes
   * @returns Entanglement score (0.0 to 1.0)
   */
  private calculateEntanglementScore(distance: number): number {
    if (distance <= 0) return 1.0;
    
    // Inverse relationship: closer = more entangled
    const normalizedDistance = Math.min(1, distance / this.MAX_ENTANGLEMENT_DISTANCE);
    const baseScore = 1 - normalizedDistance;
    
    // Add some quantum randomness for realism
    const quantumFluctuation = (Math.sin(distance) + 1) / 2 * 0.1;
    
    return Math.max(0, Math.min(1, baseScore + quantumFluctuation));
  }

  /**
   * Gets the current number of registered nodes
   * @returns Number of nodes
   */
  getNodeCount(): number {
    return this.nodes.size;
  }

  /**
   * Clears all registered nodes
   */
  clear(): void {
    this.nodes.clear();
  }
}
