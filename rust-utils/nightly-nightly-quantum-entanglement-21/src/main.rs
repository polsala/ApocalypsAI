use std::env;
use std::fs;
use std::path::Path;
use std::process;

use sha2::{Sha256, Digest};
use rand::Rng;

const VERSION: &str = env!("CARGO_PKG_VERSION");

#[derive(Debug)]
struct EntanglementResult {
    file1: String,
    file2: String,
    entangled: bool,
    confidence: f64,
    quantum_randomness: f64,
}

impl EntanglementResult {
    fn new(file1: String, file2: String, entangled: bool, confidence: f64, quantum_randomness: f64) -> Self {
        Self {
            file1,
            file2,
            entangled,
            confidence,
            quantum_randomness,
        }
    }

    fn display(&self) {
        println!("📄 File 1: {}", self.file1);
        println!("📄 File 2: {}", self.file2);
        
        if self.entangled {
            println!("🔗 Entanglement Status: Quantumly Entangled! 🪐");
        } else {
            println!("🔗 Entanglement Status: Not Entangled (Classical Reality) 🌍");
        }
        
        println!("📊 Confidence Level: {:.1}%", self.confidence * 100.0);
        println!("🎲 Quantum Randomness: {:.3}", self.quantum_randomness);
        
        if self.entangled && self.confidence > 0.95 {
            println!("✨ Spooky action at a distance detected!");
        }
    }
}

fn calculate_hash(content: &[u8]) -> Vec<u8> {
    let mut hasher = Sha256::new();
    hasher.update(content);
    hasher.finalize().to_vec()
}

fn quantum_randomness_factor() -> f64 {
    let mut rng = rand::thread_rng();
    rng.gen_range(0.001..0.01)
}

fn check_entanglement(file1_path: &str, file2_path: &str) -> Result<EntanglementResult, String> {
    // Check if files exist
    if !Path::new(file1_path).exists() {
        return Err(format!("File not found: {}", file1_path));
    }
    if !Path::new(file2_path).exists() {
        return Err(format!("File not found: {}", file2_path));
    }
    
    // Read file contents
    let content1 = fs::read(file1_path)
        .map_err(|e| format!("Failed to read {}: {}", file1_path, e))?;
    let content2 = fs::read(file2_path)
        .map_err(|e| format!("Failed to read {}: {}", file2_path, e))?;
    
    // Calculate hashes
    let hash1 = calculate_hash(&content1);
    let hash2 = calculate_hash(&content2);
    
    // Check if hashes are identical
    let hashes_match = hash1 == hash2;
    
    // Apply quantum randomness factor
    let quantum_factor = quantum_randomness_factor();
    let mut confidence = if hashes_match { 1.0 } else { 0.0 };
    confidence = (confidence - quantum_factor).max(0.0).min(1.0);
    
    // Determine entanglement status with quantum uncertainty
    let entangled = if hashes_match {
        confidence > 0.5
    } else {
        false
    };
    
    Ok(EntanglementResult::new(
        file1_path.to_string(),
        file2_path.to_string(),
        entangled,
        confidence,
        quantum_factor,
    ))
}

fn print_usage() {
    println!("Quantum Entanglement Checker v{}", VERSION);
    println!("Usage: quantum-entanglement-checker <file1> <file2>");
    println!("\nExamples:");
    println!("  quantum-entanglement-checker file1.txt file2.txt");
    println!("  quantum-entanglement-checker data.bin backup.bin");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    
    if args.len() != 3 {
        print_usage();
        process::exit(1);
    }
    
    let file1 = &args[1];
    let file2 = &args[2];
    
    match check_entanglement(file1, file2) {
        Ok(result) => {
            result.display();
            if result.entangled {
                process::exit(0);
            } else {
                process::exit(1);
            }
        }
        Err(e) => {
            eprintln!("Error: {}", e);
            process::exit(1);
        }
    }
}
