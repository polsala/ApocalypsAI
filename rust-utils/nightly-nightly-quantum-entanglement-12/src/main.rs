use std::env;
use std::fs;
use std::path::Path;
use std::process;
use clap::{Arg, Command};
use sha2::{Sha256, Digest};
use rand::Rng;

/// Quantum energy levels based on file size
#[derive(Debug, Clone)]
enum QuantumEnergy {
    Low,
    Medium,
    High,
}

impl QuantumEnergy {
    fn from_size(size: u64) -> Self {
        if size < 1024 {
            QuantumEnergy::Low
        } else if size < 1024 * 1024 {
            QuantumEnergy::Medium
        } else {
            QuantumEnergy::High
        }
    }

    fn to_string(&self) -> &'static str {
        match self {
            QuantumEnergy::Low => "Low",
            QuantumEnergy::Medium => "Medium",
            QuantumEnergy::High => "High",
        }
    }
}

/// Quantum state representation
#[derive(Debug)]
struct QuantumState {
    hash: String,
    size: u64,
    energy: QuantumEnergy,
}

impl QuantumState {
    fn new(file_path: &Path) -> Result<Self, String> {
        let content = fs::read(file_path)
            .map_err(|e| format!("Failed to read file {}: {}", file_path.display(), e))?;
        
        let mut hasher = Sha256::new();
        hasher.update(&content);
        let hash = format!("{:x}", hasher.finalize());
        
        let size = content.len() as u64;
        let energy = QuantumEnergy::from_size(size);
        
        Ok(QuantumState { hash, size, energy })
    }

    fn get_hash_prefix(&self) -> String {
        self.hash[..12].to_string()
    }
}

/// Quantum entanglement analysis result
#[derive(Debug)]
struct EntanglementResult {
    probability: f64,
    entangled: bool,
    explanation: String,
}

impl EntanglementResult {
    fn new(state1: &QuantumState, state2: &QuantumState, threshold: f64) -> Self {
        if state1.hash == state2.hash {
            EntanglementResult {
                probability: 100.0,
                entangled: true,
                explanation: "Identical quantum states detected!".to_string(),
            }
        } else {
            // Quantum uncertainty: random probability when hashes differ
            let mut rng = rand::thread_rng();
            let probability = rng.gen_range(0.0..100.0);
            let entangled = probability >= (100.0 - threshold * 100.0);
            
            EntanglementResult {
                probability,
                entangled,
                explanation: "Different quantum states, but quantum uncertainty allows for entanglement!".to_string(),
            }
        }
    }
}

/// Print quantum analysis report
fn print_quantum_report(
    file1: &Path,
    file2: &Path,
    state1: &QuantumState,
    state2: &QuantumState,
    result: &EntanglementResult,
    verbose: bool,
) {
    println!("🔬 Quantum Entanglement Analysis");
    println!("================================");
    println!("");
    
    println!("File 1: {}", file1.display());
    println!("  📏 Size: {} bytes", state1.size);
    println!("  🌀 Quantum State: {}...", state1.get_hash_prefix());
    println!("  ⚡ Energy Level: {}", state1.energy.to_string());
    
    if verbose {
        println!("  📊 Full Hash: {}", state1.hash);
    }
    
    println!("");
    
    println!("File 2: {}", file2.display());
    println!("  📏 Size: {} bytes", state2.size);
    println!("  🌀 Quantum State: {}...", state2.get_hash_prefix());
    println!("  ⚡ Energy Level: {}", state2.energy.to_string());
    
    if verbose {
        println!("  📊 Full Hash: {}", state2.hash);
    }
    
    println!("");
    println!("🔮 Entanglement Probability: {:.1}%", result.probability);
    
    if result.entangled {
        println!("✅ Quantum States Match!");
        println!("🎉 Files are quantum-entangled!");
    } else {
        println!("❌ Quantum States Differ");
        println!("🌌 Files are not entangled");
    }
    
    println!("");
    println!("📝 Explanation: {}");
}

/// Main function
fn main() {
    let matches = Command::new("Quantum Entanglement Checker")
        .version("1.0.0")
        .author("ApocalypsAI")
        .about("Checks if two files are quantum-entangled")
        .arg(
            Arg::new("file1")
                .short('f')
                .long("file1")
                .value_name("FILE1")
                .help("First file to compare")
                .required(true),
        )
        .arg(
            Arg::new("file2")
                .short('s')
                .long("file2")
                .value_name("FILE2")
                .help("Second file to compare")
                .required(true),
        )
        .arg(
            Arg::new("threshold")
                .short('t')
                .long("threshold")
                .value_name("THRESHOLD")
                .help("Entanglement threshold (0.0-1.0)")
                .default_value("0.5"),
        )
        .arg(
            Arg::new("verbose")
                .short('v')
                .long("verbose")
                .help("Verbose output with full hashes")
                .action(clap::ArgAction::SetTrue),
        )
        .get_matches();

    let file1_path = matches.get_one::<String>("file1").unwrap();
    let file2_path = matches.get_one::<String>("file2").unwrap();
    let threshold_str = matches.get_one::<String>("threshold").unwrap();
    let verbose = matches.get_flag("verbose");

    let file1 = Path::new(file1_path);
    let file2 = Path::new(file2_path);

    // Validate threshold
    let threshold: f64 = threshold_str.parse()
        .map_err(|_| {
            eprintln!("❌ Error: Threshold must be a number between 0.0 and 1.0");
            process::exit(1);
        })
        .unwrap_or_else(|e| {
            eprintln!("❌ Error: {}", e);
            process::exit(1);
        });

    if threshold < 0.0 || threshold > 1.0 {
        eprintln!("❌ Error: Threshold must be between 0.0 and 1.0");
        process::exit(1);
    }

    // Check if files exist
    if !file1.exists() {
        eprintln!("❌ Error: File {} does not exist", file1.display());
        process::exit(1);
    }
    
    if !file2.exists() {
        eprintln!("❌ Error: File {} does not exist", file2.display());
        process::exit(1);
    }

    // Get quantum states
    let state1 = QuantumState::new(file1)
        .unwrap_or_else(|e| {
            eprintln!("❌ Error reading {}: {}", file1.display(), e);
            process::exit(1);
        });

    let state2 = QuantumState::new(file2)
        .unwrap_or_else(|e| {
            eprintln!("❌ Error reading {}: {}", file2.display(), e);
            process::exit(1);
        });

    // Analyze entanglement
    let result = EntanglementResult::new(&state1, &state2, threshold);

    // Print report
    print_quantum_report(file1, file2, &state1, &state2, &result, verbose);

    // Exit with appropriate code
    if result.entangled {
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
    fn test_quantum_energy_from_size() {
        assert_eq!(QuantumEnergy::from_size(100), QuantumEnergy::Low);
        assert_eq!(QuantumEnergy::from_size(5000), QuantumEnergy::Medium);
        assert_eq!(QuantumEnergy::from_size(2000000), QuantumEnergy::High);
    }

    #[test]
    fn test_quantum_state_new() {
        let mut temp_file = NamedTempFile::new().unwrap();
        writeln!(temp_file, "Hello, quantum world!").unwrap();
        
        let state = QuantumState::new(temp_file.path()).unwrap();
        assert_eq!(state.size, 22); // "Hello, quantum world!\n" is 22 bytes
        assert_eq!(state.energy, QuantumEnergy::Low);
        assert_eq!(state.get_hash_prefix().len(), 12);
    }

    #[test]
    fn test_entanglement_result_identical() {
        let mut temp_file1 = NamedTempFile::new().unwrap();
        let mut temp_file2 = NamedTempFile::new().unwrap();
        
        writeln!(temp_file1, "Identical content").unwrap();
        writeln!(temp_file2, "Identical content").unwrap();
        
        let state1 = QuantumState::new(temp_file1.path()).unwrap();
        let state2 = QuantumState::new(temp_file2.path()).unwrap();
        
        let result = EntanglementResult::new(&state1, &state2, 0.5);
        assert_eq!(result.probability, 100.0);
        assert!(result.entangled);
        assert_eq!(result.explanation, "Identical quantum states detected!");
    }

    #[test]
    fn test_entanglement_result_different() {
        let mut temp_file1 = NamedTempFile::new().unwrap();
        let mut temp_file2 = NamedTempFile::new().unwrap();
        
        writeln!(temp_file1, "Different content 1").unwrap();
        writeln!(temp_file2, "Different content 2").unwrap();
        
        let state1 = QuantumState::new(temp_file1.path()).unwrap();
        let state2 = QuantumState::new(temp_file2.path()).unwrap();
        
        let result = EntanglementResult::new(&state1, &state2, 0.5);
        assert!(result.probability >= 0.0 && result.probability <= 100.0);
        assert_eq!(result.explanation, "Different quantum states, but quantum uncertainty allows for entanglement!");
    }

    #[test]
    fn test_entanglement_result_threshold() {
        let mut temp_file1 = NamedTempFile::new().unwrap();
        let mut temp_file2 = NamedTempFile::new().unwrap();
        
        writeln!(temp_file1, "Content A").unwrap();
        writeln!(temp_file2, "Content B").unwrap();
        
        let state1 = QuantumState::new(temp_file1.path()).unwrap();
        let state2 = QuantumState::new(temp_file2.path()).unwrap();
        
        // With threshold 1.0, should never be entangled for different content
        let result = EntanglementResult::new(&state1, &state2, 1.0);
        assert!(!result.entangled);
        
        // With threshold 0.0, should always be entangled
        let result = EntanglementResult::new(&state1, &state2, 0.0);
        assert!(result.entangled);
    }
}
