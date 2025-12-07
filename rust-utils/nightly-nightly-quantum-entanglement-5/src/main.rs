use std::env;
use std::fs;
use std::path::Path;
use std::collections::HashMap;
use std::io::{self, Read};
use sha2::{Sha256, Digest};
use rand::Rng;

const VERSION: &str = env!("CARGO_PKG_VERSION");

#[derive(Debug)]
struct QuantumResult {
    file1: String,
    file2: String,
    hash1: String,
    hash2: String,
    quantum_match: bool,
    entanglement_probability: f64,
    coherence_score: f64,
    superposition_status: bool,
}

impl QuantumResult {
    fn new(file1: String, file2: String, hash1: String, hash2: String) -> Self {
        let quantum_match = hash1 == hash2;
        let mut rng = rand::thread_rng();
        
        // Add quantum uncertainty to the comparison
        let quantum_factor = rng.gen_range(0.0..0.1);
        let base_probability = if quantum_match { 1.0 } else { 0.0 };
        let entanglement_probability = (base_probability - quantum_factor).max(0.0).min(1.0);
        
        // Calculate coherence score based on hash similarity
        let coherence_score = calculate_coherence(&hash1, &hash2);
        
        // Determine superposition status
        let superposition_status = rng.gen_bool(0.5);
        
        Self {
            file1,
            file2,
            hash1,
            hash2,
            quantum_match,
            entanglement_probability,
            coherence_score,
            superposition_status,
        }
    }
    
    fn display(&self, verbose: bool) {
        println!("\n🔬 Quantum Entanglement Analysis Report";
        println!("=".repeat(50));
        println!("File 1: {}", self.file1);
        println!("File 2: {}", self.file2);
        
        if verbose {
            println!("\nHash 1: {}", self.hash1);
            println!("Hash 2: {}", self.hash2);
        }
        
        println!("\n⚛️  Quantum State Match: {}", 
                 if self.quantum_match { "✓ YES" } else { "✗ NO" });
        
        println!("🌀 Entanglement Probability: {:.1}%", 
                 self.entanglement_probability * 100.0);
        
        println!("📊 Coherence Score: {:.1}/10.0", self.coherence_score);
        
        println!("🔮 Superposition Status: {}", 
                 if self.superposition_status { "ACTIVE" } else { "COLLAPSED" });
        
        if self.quantum_match {
            println!("\n🎉 CONCLUSION: These files are quantum-entangled!");
            println!("They share the same quantum state across all possible universes.");
        } else {
            println!("\n💥 CONCLUSION: No quantum entanglement detected.");
            println!("These files exist in separate quantum realities.");
        }
    }
}

fn calculate_coherence(hash1: &str, hash2: &str) -> f64 {
    if hash1 == hash2 {
        return 10.0;
    }
    
    let mut matching_chars = 0;
    let max_len = hash1.len().min(hash2.len());
    
    for (c1, c2) in hash1.chars().zip(hash2.chars()).take(max_len) {
        if c1 == c2 {
            matching_chars += 1;
        }
    }
    
    (matching_chars as f64 / max_len as f64) * 10.0
}

fn calculate_file_hash<P: AsRef<Path>>(path: P) -> io::Result<String> {
    let mut file = fs::File::open(&path)?;
    let mut hasher = Sha256::new();
    let mut buffer = [0; 8192];
    
    loop {
        let bytes_read = file.read(&mut buffer)?;
        if bytes_read == 0 {
            break;
        }
        hasher.update(&buffer[..bytes_read]);
    }
    
    let result = hasher.finalize();
    Ok(format!("{:x}", result))
}

fn check_entanglement(file1: &str, file2: &str) -> io::Result<QuantumResult> {
    let hash1 = calculate_file_hash(file1)?;
    let hash2 = calculate_file_hash(file2)?;
    
    Ok(QuantumResult::new(file1.to_string(), file2.to_string(), hash1, hash2))
}

fn process_batch_file<P: AsRef<Path>>(path: P) -> io::Result<Vec<QuantumResult>> {
    let content = fs::read_to_string(path)?;
    let mut results = Vec::new();
    
    for (line_num, line) in content.lines().enumerate() {
        let line = line.trim();
        if line.is_empty() || line.starts_with('#') {
            continue;
        }
        
        let parts: Vec<&str> = line.split_whitespace().collect();
        if parts.len() != 2 {
            eprintln!("Warning: Skipping invalid line {}: expected 2 file paths", line_num + 1);
            continue;
        }
        
        match check_entanglement(parts[0], parts[1]) {
            Ok(result) => results.push(result),
            Err(e) => eprintln!("Error checking line {}: {}", line_num + 1, e),
        }
    }
    
    Ok(results)
}

fn print_usage() {
    println!("\nUsage:");
    println!("  quantum-entanglement-checker [OPTIONS] <file1> <file2>");
    println!("  quantum-entanglement-checker --batch <batch_file>");
    println!("  quantum-entanglement-checker --help");
    println!("  quantum-entanglement-checker --version");
    println!("\nOptions:");
    println!("  -v, --verbose    Show detailed hash information");
    println!("  -b, --batch      Process multiple file pairs from a batch file");
    println!("  -h, --help       Show this help message");
    println!("  -V, --version    Show version information");
    println!("\nBatch file format (one pair per line):\n  file1.txt file2.txt\n  backup1.zip backup2.zip");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    
    if args.len() < 2 {
        eprintln!("Error: Not enough arguments");
        print_usage();
        std::process::exit(1);
    }
    
    let mut verbose = false;
    let mut batch_mode = false;
    let mut batch_file = String::new();
    let mut file1 = String::new();
    let mut file2 = String::new();
    
    let mut i = 1;
    while i < args.len() {
        match args[i].as_str() {
            "-v" | "--verbose" => {
                verbose = true;
                i += 1;
            }
            "-b" | "--batch" => {
                batch_mode = true;
                i += 1;
                if i < args.len() {
                    batch_file = args[i].clone();
                    i += 1;
                } else {
                    eprintln!("Error: --batch requires a file path");
                    std::process::exit(1);
                }
            }
            "-h" | "--help" => {
                print_usage();
                std::process::exit(0);
            }
            "-V" | "--version" => {
                println!("Nightly Quantum Entanglement Checker v{}", VERSION);
                std::process::exit(0);
            }
            _ => {
                if !file1.is_empty() && !file2.is_empty() {
                    eprintln!("Error: Too many arguments");
                    print_usage();
                    std::process::exit(1);
                } else if file1.is_empty() {
                    file1 = args[i].clone();
                } else {
                    file2 = args[i].clone();
                }
                i += 1;
            }
        }
    }
    
    if batch_mode {
        match process_batch_file(&batch_file) {
            Ok(results) => {
                println!("\nBatch Processing Results:");
                println!("=".repeat(30));
                for result in results {
                    result.display(verbose);
                    println!("\n{}");
                }
            }
            Err(e) => {
                eprintln!("Error reading batch file '{}': {}", batch_file, e);
                std::process::exit(1);
            }
        }
    } else {
        if file1.is_empty() || file2.is_empty() {
            eprintln!("Error: Two file paths are required");
            print_usage();
            std::process::exit(1);
        }
        
        match check_entanglement(&file1, &file2) {
            Ok(result) => result.display(verbose),
            Err(e) => {
                eprintln!("Error: {}", e);
                std::process::exit(1);
            }
        }
    }
}
