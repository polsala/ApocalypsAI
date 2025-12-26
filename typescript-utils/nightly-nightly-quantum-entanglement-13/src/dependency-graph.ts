import { ComponentNode, DependencyGraph, ComponentMetrics } from './types';
import { ComponentAnalysis } from './types';

export class DependencyGraph {
  public nodes: Map<string, ComponentNode>;
  public edges: Array<{ from: string; to: string; weight: number }>;

  constructor() {
    this.nodes = new Map();
    this.edges = [];
  }

  buildGraph(components: ComponentAnalysis[]): void {
    // Clear existing graph
    this.nodes.clear();
    this.edges = [];

    // Create nodes for all components
    components.forEach(component => {
      const metrics: ComponentMetrics = {
        coupling: 0,
        cohesion: 1.0,
        complexity: component.complexity,
        linesOfCode: component.linesOfCode
      };

      this.nodes.set(component.name, {
        id: component.name,
        name: component.name,
        dependencies: component.dependencies,
        dependents: [],
        metrics
      });
    });

    // Build edges and update dependents
    components.forEach(component => {
      const sourceNode = this.nodes.get(component.name);
      if (!sourceNode) return;

      component.dependencies.forEach(depName => {
        const targetNode = this.nodes.get(depName);
        if (targetNode) {
          // Add edge
          const weight = this.calculateEdgeWeight(sourceNode, targetNode);
          this.edges.push({
            from: sourceNode.name,
            to: targetNode.name,
            weight
          });

          // Update dependents
          targetNode.dependents.push(sourceNode.name);
        }
      });
    });

    // Calculate coupling and cohesion metrics
    this.calculateMetrics();
  }

  private calculateEdgeWeight(source: ComponentNode, target: ComponentNode): number {
    // Calculate edge weight based on various factors
    let weight = 1.0;

    // Complexity factor
    weight += (source.metrics.complexity + target.metrics.complexity) / 100;

    // Lines of code factor
    weight += (source.metrics.linesOfCode + target.metrics.linesOfCode) / 1000;

    // Dependency count factor
    weight += source.dependencies.length / 10;

    return Math.min(weight, 5.0); // Cap maximum weight
  }

  private calculateMetrics(): void {
    this.nodes.forEach(node => {
      // Calculate coupling (how much this component depends on others)
      const totalDependencies = node.dependencies.length + node.dependents.length;
      const maxPossibleConnections = this.nodes.size - 1;
      node.metrics.coupling = maxPossibleConnections > 0 ? totalDependencies / maxPossibleConnections : 0;

      // Calculate cohesion (how well the component's own code is organized)
      // This is a simplified calculation based on complexity and lines of code
      const complexityRatio = node.metrics.complexity / Math.max(1, node.metrics.linesOfCode);
      node.metrics.cohesion = Math.max(0, 1 - complexityRatio);
    });
  }

  findCycles(): string[][] {
    const cycles: string[][] = [];
    const visited = new Set<string>();
    const recStack = new Set<string>();
    const path: string[] = [];

    const detectCycle = (nodeId: string): void => {
      visited.add(nodeId);
      recStack.add(nodeId);
      path.push(nodeId);

      const node = this.nodes.get(nodeId);
      if (!node) return;

      for (const dep of node.dependencies) {
        if (!visited.has(dep)) {
          detectCycle(dep);
        } else if (recStack.has(dep)) {
          // Found a cycle
          const cycleStart = path.indexOf(dep);
          const cycle = path.slice(cycleStart);
          cycles.push(cycle);
        }
      }

      path.pop();
      recStack.delete(nodeId);
    };

    this.nodes.forEach((_, nodeId) => {
      if (!visited.has(nodeId)) {
        detectCycle(nodeId);
      }
    });

    return cycles;
  }

  getConnectedComponents(): string[][] {
    const components: string[][] = [];
    const visited = new Set<string>();

    const dfs = (nodeId: string, component: string[]): void => {
      if (visited.has(nodeId)) return;

      visited.add(nodeId);
      component.push(nodeId);

      const node = this.nodes.get(nodeId);
      if (!node) return;

      // Visit dependencies
      node.dependencies.forEach(dep => dfs(dep, component));
      // Visit dependents
      node.dependents.forEach(dep => dfs(dep, component));
    };

    this.nodes.forEach((_, nodeId) => {
      if (!visited.has(nodeId)) {
        const component: string[] = [];
        dfs(nodeId, component);
        if (component.length > 0) {
          components.push(component);
        }
      }
    });

    return components;
  }

  getMetrics(): {
    totalNodes: number;
    totalEdges: number;
    averageCoupling: number;
    averageCohesion: number;
    cycles: number;
    connectedComponents: number;
  } {
    const totalNodes = this.nodes.size;
    const totalEdges = this.edges.length;

    let totalCoupling = 0;
    let totalCohesion = 0;

    this.nodes.forEach(node => {
      totalCoupling += node.metrics.coupling;
      totalCohesion += node.metrics.cohesion;
    });

    const cycles = this.findCycles();
    const connectedComponents = this.getConnectedComponents();

    return {
      totalNodes,
      totalEdges,
      averageCoupling: totalNodes > 0 ? totalCoupling / totalNodes : 0,
      averageCohesion: totalNodes > 0 ? totalCohesion / totalNodes : 0,
      cycles: cycles.length,
      connectedComponents: connectedComponents.length
    };
  }
}
