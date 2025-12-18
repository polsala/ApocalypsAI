use std::env;
use std::fs;
use std::path::Path;
use std::process;

/// Calculate SHA-256 hash of a file
fn calculate_hash<P: AsRef<Path>>(path: P) -> Result<String, Box<dyn std::error::Error>> {
    let contents = fs::read(path)?;
    let hash = sha256::digest(&contents);
    Ok(hash)
}

/// Format hash with quantum-inspired styling
fn format_quantum_hash(hash: &str) -> String {
    // Take first 8 characters and format as hex with 0x prefix
    let shortened = &hash[..8];
    format!("0x{}", shortened)
}

/// Determine quantum state based on hash comparison
fn determine_quantum_state(hash1: &str, hash2: &str) -> (&'static str, &'static str, &'static str) {
    if hash1 == hash2 {
        ("✅ QUANTUM ENTANGLEMENT DETECTED!", "These files are perfectly synchronized across the quantum realm.", "🎉")
    } else {
        ("❌ QUANTUM DECOHERENCE OBSERVED!", "These files have collapsed into different quantum states.", "⚠️")
    }
}

/// Print the quantum analysis results
fn print_quantum_analysis(
    file1: &str,
    file2: &str,
    hash1: &str,
    hash2: &str,
) {
    println!("📄 File 1: {}", file1);
    println!("📄 File 2: {}", file2);
    println!("");
    
    println!("🌀 Quantum State Analysis:");
    println!("📊 Hash 1: {}", format_quantum_hash(hash1));
    println!("📊 Hash 2: {}", format_quantum_hash(hash2));
    println!("");
    
    let (title, message, emoji) = determine_quantum_state(hash1, hash2);
    println!("{} {}", emoji, title);
    println!("{}", message);
}

fn main() {
    let args: Vec<String> = env::args().collect();
    
    // Check argument count
    if args.len() != 3 {
        eprintln!("Usage: {} <file1> <file2>", args[0]);
        eprintln!("Example: {} file1.rs file2.rs", args[0]);
        process::exit(1);
    }
    
    let file1 = &args[1];
    let file2 = &args[2];
    
    // Validate files exist
    if !Path::new(file1).exists() {
        eprintln!("❌ Error: File '{}' does not exist", file1);
        process::exit(1);
    }
    
    if !Path::new(file2).exists() {
        eprintln!("❌ Error: File '{}' does not exist", file2);
        process::exit(1);
    }
    
    // Calculate hashes
    let hash1 = match calculate_hash(file1) {
        Ok(hash) => hash,
        Err(e) => {
            eprintln!("❌ Error reading '{}': {}", file1, e);
            process::exit(1);
        }
    };
    
    let hash2 = match calculate_hash(file2) {
        Ok(hash) => hash,
        Err(e) => {
            eprintln!("❌ Error reading '{}': {}", file2, e);
            process::exit(1);
        }
    };
    
    // Print results
    print_quantum_analysis(file1, file2, &hash1, &hash2);
    
    // Exit with appropriate code
    if hash1 == hash2 {
        process::exit(0);
    } else {
        process::exit(1);
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
        let mut file1 = NamedTempFile::new().unwrap();
        let mut file2 = NamedTempFile::new().unwrap();
        
        let content = b"fn main() { println!(\"Hello, world!\"); }";
        file1.write_all(content).unwrap();
        file2.write_all(content).unwrap();
        
        let hash1 = calculate_hash(file1.path()).unwrap();
        let hash2 = calculate_hash(file2.path()).unwrap();
        
        assert_eq!(hash1, hash2);
    }
    
    #[test]
    fn test_calculate_hash_different_files() {
        let mut file1 = NamedTempFile::new().unwrap();
        let mut file2 = NamedTempFile::new().unwrap();
        
        file1.write_all(b"fn main() { println!(\"Hello!\"); }\").unwrap();
        file2.write_all(b"fn main() { println!(\"World!\"); }\").unwrap();
        
        let hash1 = calculate_hash(file1.path()).unwrap();
        let hash2 = calculate_hash(file2.path()).unwrap();
        
        assert_ne!(hash1, hash2);
    }
    
    #[test]
    fn test_format_quantum_hash() {
        let hash = "1a2b3c4d5e6f7890abcdef1234567890abcdef1234567890abcdef1234567890";
        let formatted = format_quantum_hash(hash);
        assert_eq!(formatted, "0x1a2b3c4d");
    }
    
    #[test]
    fn test_determine_quantum_state_entangled() {
        let (title, message, emoji) = determine_quantum_state(
            "1a2b3c4d5e6f7890abcdef1234567890abcdef1234567890abcdef1234567890",
            "1a2b3c4d5e6f7890abcdef1234567890abcdef1234567890abcdef1234567890",
        );
        assert_eq!(title, "✅ QUANTUM ENTANGLEMENT DETECTED!");
        assert_eq!(message, "These files are perfectly synchronized across the quantum realm.");
        assert_eq!(emoji, "🎉");
    }
    
    #[test]
    fn test_determine_quantum_state_decohered() {
        let (title, message, emoji) = determine_quantum_state(
            "1a2b3c4d5e6f7890abcdef1234567890abcdef1234567890abcdef1234567890",
            "fedcba0987654321abcdef1234567890abcdef1234567890abcdef1234567890",
        );
        assert_eq!(title, "❌ QUANTUM DECOHERENCE OBSERVED!");
        assert_eq!(message, "These files have collapsed into different quantum states.");
        assert_eq!(emoji, "⚠️");
    }
}
