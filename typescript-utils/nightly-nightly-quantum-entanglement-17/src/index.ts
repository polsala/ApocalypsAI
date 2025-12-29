import { QuantumEntanglementChecker, quickEntanglementTest } from './quantum-entanglement-checker';

// CLI interface
if (require.main === module) {
  console.log('🔬 Initializing Quantum Entanglement Checker...');
  console.log('⚠️  Warning: May cause temporary reality distortion');
  console.log();

  const report = quickEntanglementTest();
  console.log(report);
}

// Export for use as library
export { QuantumEntanglementChecker, quickEntanglementTest };
