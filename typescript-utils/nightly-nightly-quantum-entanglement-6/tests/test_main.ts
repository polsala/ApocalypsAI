import { QuantumEntanglementChecker } from '../src/main';
import * as fs from 'fs';

// Mock rationale: We use fs.writeFileSync to create temporary test files
// and fs.unlinkSync to clean them up, avoiding actual file I/O dependencies

class QuantumEntanglementCheckerTest {
  private checker: QuantumEntanglementChecker;
  
  constructor() {
    this.checker = new QuantumEntanglementChecker();
  }

  /**
   * Test identical code snippets
   */
  testIdenticalCode(): void {
    console.log('Testing identical code snippets...');
    
    const code1 = 'function hello() { console.log("Hello World"); }';
    const code2 = 'function hello() { console.log("Hello World"); }';
    
    const result = this.checker.checkEntanglement(code1, code2, 0.0);
    
    if (result.score === 1.0 && result.entangled) {
      console.log('✅ PASS: Identical code should be 100% entangled');
    } else {
      console.log('❌ FAIL: Identical code should be 100% entangled');
      console.log(`   Score: ${result.score}, Entangled: ${result.entangled}`);
    }
  }

  /**
   * Test different code snippets
   */
  testDifferentCode(): void {
    console.log('Testing different code snippets...');
    
    const code1 = 'function add(a, b) { return a + b; }';
    const code2 = 'function subtract(a, b) { return a - b; }';
    
    const result = this.checker.checkEntanglement(code1, code2, 0.0);
    
    if (!result.entangled && result.score < 0.5) {
      console.log('✅ PASS: Different code should not be entangled');
    } else {
      console.log('❌ FAIL: Different code should not be entangled');
      console.log(`   Score: ${result.score}, Entangled: ${result.entangled}`);
    }
  }

  /**
   * Test code with comments (should be normalized)
   */
  testCodeWithComments(): void {
    console.log('Testing code with comments...');
    
    const code1 = `function hello() {
      // This is a comment
      console.log("Hello World");
      /* Multi-line comment */
    }`;
    
    const code2 = `function hello() {
      console.log("Hello World");
    }`;
    
    const result = this.checker.checkEntanglement(code1, code2, 0.0);
    
    if (result.score === 1.0 && result.entangled) {
      console.log('✅ PASS: Code with comments should be treated as identical');
    } else {
      console.log('❌ FAIL: Code with comments should be treated as identical');
      console.log(`   Score: ${result.score}, Entangled: ${result.entangled}`);
    }
  }

  /**
   * Test chaos factor effects
   */
  testChaosFactor(): void {
    console.log('Testing chaos factor effects...');
    
    const code1 = 'function test() { return 42; }';
    const code2 = 'function test() { return 42; }';
    
    const resultNoChaos = this.checker.checkEntanglement(code1, code2, 0.0);
    const resultWithChaos = this.checker.checkEntanglement(code1, code2, 0.5);
    
    if (resultNoChaos.score === 1.0 && resultWithChaos.score < 1.0) {
      console.log('✅ PASS: Chaos factor should reduce similarity score');
    } else {
      console.log('❌ FAIL: Chaos factor should reduce similarity score');
      console.log(`   No Chaos Score: ${resultNoChaos.score}`);
      console.log(`   With Chaos Score: ${resultWithChaos.score}`);
    }
  }

  /**
   * Test file reading functionality
   */
  testFileReading(): void {
    console.log('Testing file reading functionality...');
    
    const tempFile1 = 'temp_test1.ts';
    const tempFile2 = 'temp_test2.ts';
    
    try {
      // Create temporary files
      fs.writeFileSync(tempFile1, 'function test() { return "file1"; }');
      fs.writeFileSync(tempFile2, 'function test() { return "file1"; }');
      
      const result = this.checker.checkFilesEntanglement(tempFile1, tempFile2, 0.0);
      
      if (result.score === 1.0 && result.entangled) {
        console.log('✅ PASS: File reading should work correctly');
      } else {
        console.log('❌ FAIL: File reading should work correctly');
        console.log(`   Score: ${result.score}, Entangled: ${result.entangled}`);
      }
    } catch (error) {
      console.log('❌ FAIL: File reading test threw an error');
      console.log(`   Error: ${error.message}`);
    } finally {
      // Clean up temporary files
      try {
        fs.unlinkSync(tempFile1);
        fs.unlinkSync(tempFile2);
      } catch (e) {
        // Ignore cleanup errors
      }
    }
  }

  /**
   * Test error handling for non-existent files
   */
  testFileNotFoundError(): void {
    console.log('Testing file not found error handling...');
    
    try {
      this.checker.checkFilesEntanglement('nonexistent1.ts', 'nonexistent2.ts', 0.0);
      console.log('❌ FAIL: Should throw error for non-existent files');
    } catch (error) {
      if (error.message.includes('Failed to read files')) {
        console.log('✅ PASS: Correctly handles file not found errors');
      } else {
        console.log('❌ FAIL: Wrong error message');
        console.log(`   Error: ${error.message}`);
      }
    }
  }

  /**
   * Test hash consistency
   */
  testHashConsistency(): void {
    console.log('Testing hash consistency...');
    
    const code = 'function consistent() { return true; }';
    
    const hash1 = this.checker['quantumHash'](code, 0.0);
    const hash2 = this.checker['quantumHash'](code, 0.0);
    
    if (hash1 === hash2) {
      console.log('✅ PASS: Hash function is consistent');
    } else {
      console.log('❌ FAIL: Hash function should be consistent');
      console.log(`   Hash 1: ${hash1}`);
      console.log(`   Hash 2: ${hash2}`);
    }
  }

  /**
   * Run all tests
   */
  runAllTests(): void {
    console.log('=== Running Quantum Entanglement Checker Tests ===\n');
    
    this.testIdenticalCode();
    this.testDifferentCode();
    this.testCodeWithComments();
    this.testChaosFactor();
    this.testFileReading();
    this.testFileNotFoundError();
    this.testHashConsistency();
    
    console.log('\n=== Test Suite Complete ===');
  }
}

// Run tests if this file is executed directly
if (require.main === module) {
  const testSuite = new QuantumEntanglementCheckerTest();
  testSuite.runAllTests();
}

export { QuantumEntanglementCheckerTest };
