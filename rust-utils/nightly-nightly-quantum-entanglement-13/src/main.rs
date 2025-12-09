use std::env;
use std::fs;
use std::path::Path;
use std::process;

// Blake3 for fast, secure hashing
use blake3::Hasher;

/// Quantum entanglement check result
#[derive(Debug, PartialEq)]
enum EntanglementResult {
    Entangled,
    NotEntangled,
    Uncertain,
}

/// Quantum entanglement analysis report
#[derive(Debug)]
struct EntanglementReport {
    file1: String,
    file2: String,
    hash1: String,
    hash2: String,
    result: EntanglementResult,
    probability: f64,
    quantum_noise: f64,
    verbose: bool,
}

impl EntanglementReport {
    fn new(file1: String, file2: String, hash1: String, hash2: String, result: EntanglementResult, probability: f64, quantum_noise: f64, verbose: bool) -> Self {
        Self {
            file1,
            file2,
            hash1,
            hash2,
            result,
            probability,
            quantum_noise,
            verbose,
        }
    }

    fn print(&self) {
        println!("🔬 Quantum Entanglement Analysis Report");
        println!("=====================================");
        println!("");
        
        println!("File 1: {}", self.file1);
        println!("File 2: {}", self.file2);
        println!("");
        
        if self.verbose {
            println!("Hash 1: {}", &self.hash1[..12]);
            println!("Hash 2: {}", &self.hash2[..12]);
            println!("");
        }
        
        match self.result {
            EntanglementResult::Entangled => println!("Quantum State: IDENTICAL"),
            EntanglementResult::NotEntangled => println!("Quantum State: DIFFERENT"),
            EntanglementResult::Uncertain => println!("Quantum State: UNCERTAIN"),
        }
        
        println!("Probability: {:.1}%", self.probability * 100.0);
        println!("Quantum Noise: {:.6}", self.quantum_noise);
        println!("");
        
        match self.result {
            EntanglementResult::Entangled => {
                println!("🎉 CONCLUSION: These files are quantum-entangled!");
            },
            EntanglementResult::NotEntangled => {
                println!("❌ CONCLUSION: These files are not quantum-entangled.");
            },
            EntanglementResult::Uncertain => {
                println!("❓ CONCLUSION: Quantum state uncertain due to excessive noise.");
            },
        }
        
        println!("");
        println!("Note: This entanglement may or may not violate the no-cloning theorem.");
    }
}

/// Calculate Blake3 hash of a file
fn calculate_hash<P: AsRef<Path>>(path: P) -> Result<String, Box<dyn std::error::Error>> {
    let content = fs::read(path)?;
    let mut hasher = Hasher::new();
    hasher.update(&content);
    let hash = hasher.finalize();
    Ok(format!("{:x}", hash))
}

/// Simulate quantum probability with random noise
fn quantum_probability_simulation(base_probability: f64) -> (f64, f64) {
    // Generate pseudo-random quantum noise using hash of current time
    let time_ns = std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .unwrap()
        .as_nanos();
    
    let noise = (time_ns % 1000) as f64 / 1000000.0; // 0.0 to 0.000999
    
    let adjusted_probability = base_probability - noise;
    let clamped_probability = adjusted_probability.max(0.0).min(1.0);
    
    (clamped_probability, noise)
}

/// Check if two files are quantum-entangled
fn check_quantum_entanglement(
    file1: &str,
    file2: &str,
    threshold: f64,
    verbose: bool,
) -> Result<EntanglementReport, Box<dyn std::error::Error>> {
    // Verify files exist
    if !Path::new(file1).exists() {
        return Err(format!("File not found: {}", file1).into());
    }
    if !Path::new(file2).exists() {
        return Err(format!("File not found: {}", file2).into());
    }
    
    // Calculate hashes
    let hash1 = calculate_hash(file1)?;
    let hash2 = calculate_hash(file2)?;
    
    // Determine entanglement
    let (probability, quantum_noise) = if hash1 == hash2 {
        // Identical hashes - very likely entangled
        quantum_probability_simulation(0.997)
    } else {
        // Different hashes - not entangled
        quantum_probability_simulation(0.001)
    };
    
    let result = if probability >= threshold {
        if hash1 == hash2 {
            EntanglementResult::Entangled
        } else {
            EntanglementResult::Uncertain
        }
    } else {
        EntanglementResult::NotEntangled
    };
    
    Ok(EntanglementReport::new(
        file1.to_string(),
        file2.to_string(),
        hash1,
        hash2,
        result,
        probability,
        quantum_noise,
        verbose,
    ))
}

/// Parse command line arguments
fn parse_args() -> (String, String, f64, bool) {
    let args: Vec<String> = env::args().collect();
    
    if args.len() < 2 {
        print_usage();
        process::exit(1);
    }
    
    let mut file1 = None;
    let mut file2 = None;
    let mut threshold = 0.5;
    let mut verbose = false;
    
    let mut i = 1;
    while i < args.len() {
        match args[i].as_str() {
            "--file1" => {
                if i + 1 < args.len() {
                    file1 = Some(args[i + 1].clone());
                    i += 2;
                } else {
                    eprintln!("Error: --file1 requires a value");
                    process::exit(1);
                }
            },
            "--file2" => {
                if i + 1 < args.len() {
                    file2 = Some(args[i + 1].clone());
                    i += 2;
                } else {
                    eprintln!("Error: --file2 requires a value");
                    process::exit(1);
                }
            },
            "--threshold" => {
                if i + 1 < args.len() {
                    threshold = args[i + 1].parse().expect("Invalid threshold value");
                    if threshold < 0.0 || threshold > 1.0 {
                        eprintln!("Error: Threshold must be between 0.0 and 1.0");
                        process::exit(1);
                    }
                    i += 2;
                } else {
                    eprintln!("Error: --threshold requires a value");
                    process::exit(1);
                }
            },
            "--verbose" => {
                verbose = true;
                i += 1;
            },
            "--help" | "-h" => {
                print_usage();
                process::exit(0);
            },
            _ => {
                eprintln!("Unknown argument: {}", args[i]);
                print_usage();
                process::exit(1);
            },
        }
    }
    
    if file1.is_none() || file2.is_none() {
        eprintln!("Error: Both --file1 and --file2 are required");
        print_usage();
        process::exit(1);
    }
    
    (file1.unwrap(), file2.unwrap(), threshold, verbose)
}

/// Print usage information
fn print_usage() {
    println!("Usage: quantum-entanglement-checker --file1 <path> --file2 <path> [OPTIONS]");
    println!("");
    println!("Options:");
    println!("  --file1 <path>     First file to compare");
    println!("  --file2 <path>     Second file to compare");
    println!("  --threshold <val>  Probability threshold (0.0-1.0, default: 0.5)");
    println!("  --verbose          Show detailed output");
    println!("  --help, -h         Show this help message");
}

fn main() {
    let (file1, file2, threshold, verbose) = parse_args();
    
    match check_quantum_entanglement(&file1, &file2, threshold, verbose) {
        Ok(report) => {
            report.print();
            // Exit with appropriate code
            match report.result {
                EntanglementResult::Entangled => process::exit(0),
                EntanglementResult::NotEntangled => process::exit(1),
                EntanglementResult::Uncertain => process::exit(2),
            }
        },
        Err(e) => {
            eprintln!("Error: {}", e);
            process::exit(3);
        },
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::fs;
    use std::io::Write;
    use tempfile::NamedTempFile;
    
    #[test]
    fn test_calculate_hash_identical_files() {
        let mut temp1 = NamedTempFile::new().unwrap();
        let mut temp2 = NamedTempFile::new().unwrap();
        
        let content = b"Hello, quantum world!";
        temp1.write_all(content).unwrap();
        temp2.write_all(content).unwrap();
        
        let hash1 = calculate_hash(temp1.path().to_str().unwrap()).unwrap();
        let hash2 = calculate_hash(temp2.path().to_str().unwrap()).unwrap();
        
        assert_eq!(hash1, hash2);
    }
    
    #[test]
    fn test_calculate_hash_different_files() {
        let mut temp1 = NamedTempFile::new().unwrap();
        let mut temp2 = NamedTempFile::new().unwrap();
        
        temp1.write_all(b"Hello, world!").unwrap();
        temp2.write_all(b"Goodbye, world!").unwrap();
        
        let hash1 = calculate_hash(temp1.path().to_str().unwrap()).unwrap();
        let hash2 = calculate_hash(temp2.path().to_str().unwrap()).unwrap();
        
        assert_ne!(hash1, hash2);
    }
    
    #[test]
    fn test_quantum_probability_simulation() {
        let (prob, noise) = quantum_probability_simulation(0.997);
        
        assert!(prob >= 0.0 && prob <= 1.0);
        assert!(noise >= 0.0 && noise < 0.001);
        assert!(prob <= 0.997);
    }
    
    #[test]
    fn test_check_quantum_entanglement_identical() {
        let mut temp1 = NamedTempFile::new().unwrap();
        let mut temp2 = NamedTempFile::new().unwrap();
        
        let content = b"Quantum entanglement test";
        temp1.write_all(content).unwrap();
        temp2.write_all(content).unwrap();
        
        let report = check_quantum_entanglement(
            temp1.path().to_str().unwrap(),
            temp2.path().to_str().unwrap(),
            0.5,
            false,
        ).unwrap();
        
        assert_eq!(report.result, EntanglementResult::Entangled);
        assert!(report.probability > 0.99);
        assert_eq!(report.hash1, report.hash2);
    }
    
    #[test]
    fn test_check_quantum_entanglement_different() {
        let mut temp1 = NamedTempFile::new().unwrap();
        let mut temp2 = NamedTempFile::new().unwrap();
        
        temp1.write_all(b"File A content").unwrap();
        temp2.write_all(b"File B content").unwrap();
        
        let report = check_quantum_entanglement(
            temp1.path().to_str().unwrap(),
            temp2.path().to_str().unwrap(),
            0.5,
            false,
        ).unwrap();
        
        assert_eq!(report.result, EntanglementResult::NotEntangled);
        assert!(report.probability < 0.01);
        assert_ne!(report.hash1, report.hash2);
    }
    
    #[test]
    fn test_check_quantum_entanglement_nonexistent_file() {
        let result = check_quantum_entanglement(
            "nonexistent_file.txt",
            "another_nonexistent.txt",
            0.5,
            false,
        );
        
        assert!(result.is_err());
        assert!(result.unwrap_err().to_string().contains("File not found"));
    }
    
    #[test]
    fn test_entanglement_report_print() {
        // This test just ensures the print method doesn't panic
        let report = EntanglementReport::new(
            "file1.txt".to_string(),
            "file2.txt".to_string(),
            "a1b2c3d4e5f67890123456789012345678901234567890123456789012345678".to_string(),
            "a1b2c3d4e5f67890123456789012345678901234567890123456789012345678".to_string(),
            EntanglementResult::Entangled,
            0.997,
            0.0003,
            true,
        );
        
        // Should not panic
        report.print();
    }
}
