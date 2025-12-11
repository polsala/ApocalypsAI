import * as crypto from 'crypto';
import * as fs from 'fs';

export interface EntanglementResult {
  score: number;
  entangled: boolean;
  hash1: string;
  hash2: string;
  chaosFactor: number;
}

class QuantumEntanglementChecker {
  private readonly CHAOS_SEED = 42;
  private readonly ENTANGLEMENT_THRESHOLD = 0.8;

  /**
   * Calculate a quantum-inspired hash with chaos factor
   * @param code The code snippet to hash
   * @param chaosFactor Additional entropy for quantum effects
   * @returns Hex string hash
   */
  private quantumHash(code: string, chaosFactor: number = 0): string {
    // Normalize code by removing whitespace and comments for fair comparison
    const normalizedCode = this.normalizeCode(code);
    
    // Apply chaos factor to introduce quantum uncertainty
    const chaoticInput = this.applyChaos(normalizedCode, chaosFactor);
    
    // Generate SHA-256 hash
    return crypto.createHash('sha256').update(chaoticInput).digest('hex');
  }

  /**
   * Normalize code by removing comments and extra whitespace
   * @param code The code to normalize
   * @returns Normalized code string
   */
  private normalizeCode(code: string): string {
    return code
      .replace(/\/\/.*$/gm, '') // Remove single-line comments
      .replace(/\/\*[\s\S]*?\*\//g, '') // Remove multi-line comments
      .replace(/\s+/g, ' ') // Normalize whitespace
      .trim();
  }

  /**
   * Apply chaos factor to introduce quantum uncertainty
   * @param input The input string
   * @param chaosFactor The chaos factor (0-1)
   * @returns Chaotic string
   */
  private applyChaos(input: string, chaosFactor: number): string {
    if (chaosFactor <= 0) return input;
    
    // Seed the random number generator for reproducible chaos
    const seed = this.hashString(input) ^ this.CHAOS_SEED;
    let random = this.xorshift(seed);
    
    // Apply chaos based on factor
    let result = input;
    const iterations = Math.floor(chaosFactor * 10);
    
    for (let i = 0; i < iterations; i++) {
      const pos = Math.floor(random * input.length);
      const charCode = input.charCodeAt(pos);
      const shifted = (charCode + Math.floor(random * 256)) % 256;
      result = result.substring(0, pos) + String.fromCharCode(shifted) + result.substring(pos + 1);
      random = this.xorshift(random * 1000000);
    }
    
    return result;
  }

  /**
   * Simple hash function for seeding
   * @param str Input string
   * @returns Hash number
   */
  private hashString(str: string): number {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash; // Convert to 32-bit integer
    }
    return Math.abs(hash);
  }

  /**
   * Xorshift random number generator for reproducible chaos
   * @param seed Initial seed
   * @returns Random number between 0 and 1
   */
  private xorshift(seed: number): number {
    let x = seed || 123456789;
    x ^= x << 13;
    x ^= x >>> 17;
    x ^= x << 5;
    return Math.abs(x) / 0xFFFFFFFF;
  }

  /**
   * Calculate similarity score between two hashes
   * @param hash1 First hash
   * @param hash2 Second hash
   * @returns Similarity score (0-1)
   */
  private calculateSimilarity(hash1: string, hash2: string): number {
    let matches = 0;
    const length = Math.min(hash1.length, hash2.length);
    
    for (let i = 0; i < length; i++) {
      if (hash1[i] === hash2[i]) {
        matches++;
      }
    }
    
    return matches / length;
  }

  /**
   * Check if two code snippets are quantum entangled
   * @param code1 First code snippet
   * @param code2 Second code snippet
   * @param chaosFactor Quantum uncertainty factor (0-1)
   * @returns Entanglement result
   */
  public checkEntanglement(code1: string, code2: string, chaosFactor: number = 0.1): EntanglementResult {
    const hash1 = this.quantumHash(code1, chaosFactor);
    const hash2 = this.quantumHash(code2, chaosFactor);
    
    const score = this.calculateSimilarity(hash1, hash2);
    const entangled = score >= this.ENTANGLEMENT_THRESHOLD;
    
    return {
      score,
      entangled,
      hash1,
      hash2,
      chaosFactor
    };
  }

  /**
   * Check if two files are quantum entangled
   * @param filePath1 Path to first file
   * @param filePath2 Path to second file
   * @param chaosFactor Quantum uncertainty factor (0-1)
   * @returns Promise with entanglement result
   */
  public async checkFilesEntanglement(filePath1: string, filePath2: string, chaosFactor: number = 0.1): Promise<EntanglementResult> {
    try {
      const code1 = fs.readFileSync(filePath1, 'utf-8');
      const code2 = fs.readFileSync(filePath2, 'utf-8');
      
      return this.checkEntanglement(code1, code2, chaosFactor);
    } catch (error) {
      throw new Error(`Failed to read files: ${error.message}`);
    }
  }
}

// CLI interface
if (require.main === module) {
  const args = process.argv.slice(2);
  
  if (args.length < 2) {
    console.log('Usage: ts-node main.ts <file1> <file2> [chaosFactor]');
    process.exit(1);
  }
  
  const [file1, file2, chaosStr] = args;
  const chaosFactor = chaosStr ? parseFloat(chaosStr) : 0.1;
  
  const checker = new QuantumEntanglementChecker();
  
  checker.checkFilesEntanglement(file1, file2, chaosFactor)
    .then(result => {
      console.log('=== Quantum Entanglement Analysis ===');
      console.log(`File 1: ${file1}`);
      console.log(`File 2: ${file2}`);
      console.log(`Chaos Factor: ${result.chaosFactor}`);
      console.log(`Hash 1: ${result.hash1}`);
      console.log(`Hash 2: ${result.hash2}`);
      console.log(`Similarity Score: ${result.score.toFixed(4)}`);
      console.log(`Are Quantum Entangled: ${result.entangled ? 'YES 🌀' : 'NO ❌'}`);
      
      if (result.entangled) {
        console.log('\n🎉 These code snippets are quantumly entangled! Spooky action at a distance detected!');
      } else {
        console.log('\n🤷 No quantum entanglement detected. These snippets are independent.');
      }
    })
    .catch(error => {
      console.error(`Error: ${error.message}`);
      process.exit(1);
    });
}

export { QuantumEntanglementChecker };
