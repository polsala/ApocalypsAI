import { EntanglementResult, QuantumNode, EntanglementLink } from './quantum-entanglement-checker';
import * as fs from 'fs';
import * as path from 'path';

export class QuantumReportGenerator {
  displayResults(result: EntanglementResult, nodes: string[]): void {
    console.log(`📍 Location: Node Cluster ${nodes.join(' + ')}`);
    console.log(`🕒 Timestamp: ${result.timestamp.toISOString()}`);
    console.log();
    
    console.log('⚛️  Quantum State Analysis:');
    result.nodes.forEach(node => {
      const spinSymbol = node.spin === 'up' ? '↑' : '↓';
      const status = node.entangledWith.length > 0 ? '✓ Entangled' : '○ Isolated';
      console.log(`   - Node ${node.name}: ${status} (Spin: ${spinSymbol}, Coherence: ${node.coherence}%)`);
    });
    console.log();
    
    console.log('🔗 Entanglement Links:');
    if (result.links.length > 0) {
      result.links.forEach(link => {
        const strengthSymbol = this.getStrengthSymbol(link.strength);
        console.log(`   - ${link.from} ↔ ${link.to}: ${strengthSymbol} ${link.strength} (Bell State: ${link.bellState})`);
      });
    } else {
      console.log('   - No entanglement links detected');
    }
    console.log();
    
    if (result.warnings.length > 0) {
      console.log('⚠️  Quantum Warnings:');
      result.warnings.forEach(warning => {
        console.log(`   - ${warning}`);
      });
      console.log();
    }
    
    console.log(`✨ Quantum Entanglement Status: ${result.overallStability}% Stable`);
  }

  generateReport(result: EntanglementResult, nodes: string[]): string {
    const report = {
      timestamp: result.timestamp.toISOString(),
      location: `Node Cluster ${nodes.join(' + ')}`,
      quantumStateAnalysis: result.nodes.map(node => ({
        name: node.name,
        spin: node.spin,
        coherence: node.coherence,
        entangledWith: node.entangledWith,
        status: node.entangledWith.length > 0 ? 'ENTANGLED' : 'ISOLATED'
      })),
      entanglementLinks: result.links.map(link => ({
        from: link.from,
        to: link.to,
        strength: link.strength.toUpperCase(),
        bellState: link.bellState,
        coherence: link.coherence
      })),
      warnings: result.warnings,
      overallStability: result.overallStability,
      quantumMetrics: {
        totalNodes: result.nodes.length,
        entangledNodes: result.nodes.filter(n => n.entangledWith.length > 0).length,
        totalLinks: result.links.length,
        strongLinks: result.links.filter(l => l.strength === 'strong').length,
        mediumLinks: result.links.filter(l => l.strength === 'medium').length,
        weakLinks: result.links.filter(l => l.strength === 'weak').length
      }
    };
    
    return JSON.stringify(report, null, 2);
  }

  async saveReport(report: string, filePath: string): Promise<void> {
    const fullPath = path.resolve(filePath);
    
    try {
      await fs.promises.writeFile(fullPath, report, 'utf8');
    } catch (error) {
      throw new Error(`Failed to save report to ${fullPath}: ${error}`);
    }
  }

  private getStrengthSymbol(strength: string): string {
    switch (strength) {
      case 'strong': return '🔗';
      case 'medium': return '〰️';
      case 'weak': return '⚠️';
      default: return '❓';
    }
  }
}
