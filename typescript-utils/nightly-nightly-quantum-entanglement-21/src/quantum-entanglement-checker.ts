export interface QuantumNode {
  name: string;
  spin: 'up' | 'down';
  coherence: number;
  entangledWith: string[];
}

export interface EntanglementResult {
  nodes: QuantumNode[];
  links: EntanglementLink[];
  overallStability: number;
  warnings: string[];
  timestamp: Date;
}

export interface EntanglementLink {
  from: string;
  to: string;
  strength: 'strong' | 'medium' | 'weak';
  bellState: string;
  coherence: number;
}

export class QuantumEntanglementChecker {
  private readonly MAX_COHERENCE = 100;
  private readonly MIN_COHERENCE = 0;
  private readonly DECAY_RATE = 0.1;

  async checkEntanglement(nodes: string[]): Promise<EntanglementResult> {
    // Simulate quantum state generation
    const quantumNodes = nodes.map(name => this.generateQuantumNode(name));
    
    // Simulate entanglement links
    const links = this.generateEntanglementLinks(quantumNodes);
    
    // Calculate overall stability
    const overallStability = this.calculateOverallStability(quantumNodes, links);
    
    // Generate warnings
    const warnings = this.generateWarnings(quantumNodes, links);

    return {
      nodes: quantumNodes,
      links: links,
      overallStability: overallStability,
      warnings: warnings,
      timestamp: new Date()
    };
  }

  private generateQuantumNode(name: string): QuantumNode {
    const spin = Math.random() > 0.5 ? 'up' : 'down';
    const baseCoherence = 80 + Math.random() * 20; // 80-100%
    const entangledWith: string[] = [];

    return {
      name: name,
      spin: spin,
      coherence: Math.round(baseCoherence),
      entangledWith: entangledWith
    };
  }

  private generateEntanglementLinks(nodes: QuantumNode[]): EntanglementLink[] {
    const links: EntanglementLink[] = [];
    
    for (let i = 0; i < nodes.length; i++) {
      for (let j = i + 1; j < nodes.length; j++) {
        const node1 = nodes[i];
        const node2 = nodes[j];
        
        // Randomly decide if nodes are entangled
        if (Math.random() > 0.3) {
          const strength = this.calculateLinkStrength(node1.coherence, node2.coherence);
          const bellState = this.generateBellState(node1.spin, node2.spin);
          const coherence = this.calculateLinkCoherence(node1.coherence, node2.coherence, strength);
          
          const link: EntanglementLink = {
            from: node1.name,
            to: node2.name,
            strength: strength,
            bellState: bellState,
            coherence: Math.round(coherence)
          };
          
          links.push(link);
          node1.entangledWith.push(node2.name);
          node2.entangledWith.push(node1.name);
        }
      }
    }
    
    return links;
  }

  private calculateLinkStrength(coherence1: number, coherence2: number): 'strong' | 'medium' | 'weak' {
    const avgCoherence = (coherence1 + coherence2) / 2;
    
    if (avgCoherence >= 90) return 'strong';
    if (avgCoherence >= 75) return 'medium';
    return 'weak';
  }

  private generateBellState(spin1: string, spin2: string): string {
    const states = [
      '|↑↓⟩ - |↓↑⟩',
      '|↑↓⟩ + |↓↑⟩',
      '|↑↑⟩ + |↓↓⟩',
      '|↑↑⟩ - |↓↓⟩'
    ];
    
    return states[Math.floor(Math.random() * states.length)];
  }

  private calculateLinkCoherence(coherence1: number, coherence2: number, strength: string): number {
    let baseCoherence = (coherence1 + coherence2) / 2;
    
    switch (strength) {
      case 'strong':
        baseCoherence += 5;
        break;
      case 'medium':
        baseCoherence += 0;
        break;
      case 'weak':
        baseCoherence -= 10;
        break;
    }
    
    // Add some quantum noise
    const noise = (Math.random() - 0.5) * 5;
    return Math.max(this.MIN_COHERENCE, Math.min(this.MAX_COHERENCE, baseCoherence + noise));
  }

  private calculateOverallStability(nodes: QuantumNode[], links: EntanglementLink[]): number {
    if (links.length === 0) return 0;
    
    const totalCoherence = links.reduce((sum, link) => sum + link.coherence, 0);
    const avgCoherence = totalCoherence / links.length;
    
    // Factor in node coherence
    const nodeCoherence = nodes.reduce((sum, node) => sum + node.coherence, 0) / nodes.length;
    
    return Math.round((avgCoherence * 0.7) + (nodeCoherence * 0.3));
  }

  private generateWarnings(nodes: QuantumNode[], links: EntanglementLink[]): string[] {
    const warnings: string[] = [];
    
    // Check for low coherence nodes
    nodes.forEach(node => {
      if (node.coherence < 70) {
        warnings.push(`Node ${node.name} experiencing decoherence (coherence: ${node.coherence}%)`);
      }
    });
    
    // Check for weak entanglement links
    links.forEach(link => {
      if (link.strength === 'weak') {
        warnings.push(`Weak entanglement detected between ${link.from} and ${link.to}`);
      }
    });
    
    // Check for isolated nodes
    nodes.forEach(node => {
      if (node.entangledWith.length === 0) {
        warnings.push(`Node ${node.name} is quantumly isolated`);
      }
    });
    
    return warnings;
  }
}
