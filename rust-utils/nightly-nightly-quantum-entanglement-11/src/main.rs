use std::collections::{HashMap, HashSet};
use std::fs;
use std::path::Path;
use std::time::{SystemTime, UNIX_EPOCH};
use clap::{Arg, Command};
use rand::Rng;

/// Quantum state representation for files
#[derive(Debug, Clone, PartialEq)]
enum QuantumState {
    Superposition(f64, f64), // (probability_amplitude_0, probability_amplitude_1)
    Collapsed(bool),          // Measured state: true or false
}

/// Bell state types for maximum entanglement
#[derive(Debug, Clone, PartialEq)]
enum BellState {
    PhiPlus,  // (|00⟩ + |11⟩) / √2
    PhiMinus, // (|00⟩ - |11⟩) / √2
    PsiPlus,  // (|01⟩ + |10⟩) / √2
    PsiMinus, // (|01⟩ - |10⟩) / √2
}

/// File quantum properties
#[derive(Debug, Clone)]
struct QuantumFile {
    path: String,
    state: QuantumState,
    timestamp: u64,
    hash: u64,
}

/// Quantum entanglement analyzer
struct QuantumEntanglementChecker {
    files: Vec<QuantumFile>,
    rng: rand::rngs::ThreadRng,
}

impl QuantumEntanglementChecker {
    fn new() -> Self {
        Self {
            files: Vec::new(),
            rng: rand::thread_rng(),
        }
    }

    fn load_file(&mut self, path: &str) -> Result<(), Box<dyn std::error::Error>> {
        if !Path::new(path).exists() {
            return Err(format!("File not found: {}", path).into());
        }

        let content = fs::read_to_string(path)?;
        let hash = self.calculate_hash(&content);
        let timestamp = self.get_file_timestamp(path)?;

        // Create quantum superposition state based on file properties
        let probability_0 = (hash as f64 % 1000.0) / 1000.0;
        let probability_1 = 1.0 - probability_0;

        let quantum_file = QuantumFile {
            path: path.to_string(),
            state: QuantumState::Superposition(probability_0, probability_1),
            timestamp,
            hash,
        };

        self.files.push(quantum_file);
        Ok(())
    }

    fn calculate_hash(&self, content: &str) -> u64 {
        use std::collections::hash_map::DefaultHasher;
        use std::hash::{Hash, Hasher};
        
        let mut hasher = DefaultHasher::new();
        content.hash(&mut hasher);
        hasher.finish()
    }

    fn get_file_timestamp(&self, path: &str) -> Result<u64, Box<dyn std::error::Error>> {
        let metadata = fs::metadata(path)?;
        let modified = metadata.modified()?;
        let since_epoch = modified.duration_since(UNIX_EPOCH)?;
        Ok(since_epoch.as_secs())
    }

    fn observe_file(&mut self, index: usize) -> Result<bool, &'static str> {
        if index >= self.files.len() {
            return Err("Invalid file index");
        }

        let file = &mut self.files[index];
        
        match file.state.clone() {
            QuantumState::Collapsed(result) => Ok(result),
            QuantumState::Superposition(prob_0, prob_1) => {
                // Collapse superposition based on probabilities
                let random = self.rng.gen::<f64>();
                let result = random > prob_0;
                
                file.state = QuantumState::Collapsed(result);
                Ok(result)
            }
        }
    }

    fn check_entanglement(&self, index_a: usize, index_b: usize) -> Option<(f64, BellState)> {
        if index_a >= self.files.len() || index_b >= self.files.len() || index_a == index_b {
            return None;
        }

        let file_a = &self.files[index_a];
        let file_b = &self.files[index_b];

        // Calculate quantum correlation based on hash similarity and timestamp proximity
        let hash_diff = (file_a.hash as i64 - file_b.hash as i64).abs() as f64;
        let time_diff = (file_a.timestamp as i64 - file_b.timestamp as i64).abs() as f64;

        // Normalize differences
        let normalized_hash_diff = hash_diff / 1_000_000_000.0;
        let normalized_time_diff = time_diff / 86400.0; // seconds in a day

        // Calculate entanglement score (lower differences = higher entanglement)
        let correlation = 1.0 - ((normalized_hash_diff + normalized_time_diff) / 2.0);
        let clamped_correlation = correlation.max(0.0).min(1.0);

        // Determine Bell state based on correlation patterns
        let bell_state = match clamped_correlation {
            x if x > 0.8 => BellState::PhiPlus,
            x if x > 0.6 => BellState::PhiMinus,
            x if x > 0.4 => BellState::PsiPlus,
            _ => BellState::PsiMinus,
        };

        Some((clamped_correlation, bell_state))
    }

    fn test_decoherence(&self, indices: &[usize]) -> Result<f64, &'static str> {
        if indices.len() < 2 {
            return Err("Need at least 2 files for decoherence test");
        }

        let mut total_correlation = 0.0;
        let mut pairs = 0;

        for i in 0..indices.len() {
            for j in (i+1)..indices.len() {
                if let Some((correlation, _)) = self.check_entanglement(indices[i], indices[j]) {
                    total_correlation += correlation;
                    pairs += 1;
                }
            }
        }

        if pairs == 0 {
            return Err("No valid file pairs for decoherence test");
        }

        Ok(total_correlation / pairs as f64)
    }

    fn generate_report(&self) -> String {
        let mut report = String::from("🔬 Quantum Entanglement Analysis Report\n");
        report.push_str("========================================\n\n");

        if self.files.len() < 2 {
            report.push_str("⚠️  Need at least 2 files to analyze entanglement.\n");
            return report;
        }

        for i in 0..self.files.len() {
            for j in (i+1)..self.files.len() {
                if let Some((correlation, bell_state)) = self.check_entanglement(i, j) {
                    report.push_str(&format!("File A: {}\n", self.files[i].path));
                    report.push_str(&format!("File B: {}\n", self.files[j].path));
                    report.push_str(&format!("Quantum Correlation Score: {:.3}\n", correlation));
                    
                    let entanglement_status = match correlation {
                        x if x > 0.8 => "✨ STRONGLY ENTANGLED",
                        x if x > 0.6 => "💫 MODERATELY ENTANGLED",
                        x if x > 0.4 => "⚡ WEAKLY ENTANGLED",
                        _ => "❌ NOT ENTANGLED",
                    };
                    
                    report.push_str(&format!("Entanglement Status: {}\n", entanglement_status));
                    report.push_str(&format!("Bell State: {:?}\n", bell_state));
                    
                    let decoherence_risk = match correlation {
                        x if x > 0.7 => "LOW",
                        x if x > 0.5 => "MEDIUM",
                        _ => "HIGH",
                    };
                    
                    report.push_str(&format!("Decoherence Risk: {}\n", decoherence_risk));
                    
                    let spooky_action = if correlation > 0.5 {
                        "CONFIRMED 🎃"
                    } else {
                        "NOT DETECTED 👻"
                    };
                    
                    report.push_str(&format!("Spooky Action: {}\n", spooky_action));
                    report.push_str("\n");
                }
            }
        }

        report
    }
}

fn main() {
    let matches = Command::new("Quantum Entanglement Checker")
        .version("1.0.0")
        .author("ApocalypsAI")
        .about("Simulates quantum entanglement between files to detect spooky correlations")
        .subcommand(
            Command::new("check")
                .about("Check entanglement between two files")
                .arg(Arg::new("file1")
                    .help("First file to analyze")
                    .required(true))
                .arg(Arg::new("file2")
                    .help("Second file to analyze")
                    .required(true))
        )
        .subcommand(
            Command::new("report")
                .about("Generate entanglement report for a directory")
                .arg(Arg::new("directory")
                    .help("Directory to analyze")
                    .required(true))
        )
        .subcommand(
            Command::new("decoherence")
                .about("Test quantum decoherence with multiple files")
                .arg(Arg::new("files")
                    .help("Files to test for decoherence")
                    .required(true)
                    .num_args(2..))
        )
        .get_matches();

    let mut checker = QuantumEntanglementChecker::new();

    match matches.subcommand() {
        Some(("check", sub_matches)) => {
            let file1 = sub_matches.get_one::<String>("file1").unwrap();
            let file2 = sub_matches.get_one::<String>("file2").unwrap();

            match checker.load_file(file1) {
                Ok(_) => {},
                Err(e) => {
                    eprintln!("❌ Error loading {}: {}", file1, e);
                    std::process::exit(1);
                }
            }

            match checker.load_file(file2) {
                Ok(_) => {},
                Err(e) => {
                    eprintln!("❌ Error loading {}: {}", file2, e);
                    std::process::exit(1);
                }
            }

            if let Some((correlation, bell_state)) = checker.check_entanglement(0, 1) {
                println!("🔬 Quantum Entanglement Check");
                println!("===============================");
                println!("\nFile A: {}", file1);
                println!("File B: {}", file2);
                println!("\nQuantum Correlation Score: {:.3}", correlation);
                
                let status = match correlation {
                    x if x > 0.8 => "✨ STRONGLY ENTANGLED",
                    x if x > 0.6 => "💫 MODERATELY ENTANGLED",
                    x if x > 0.4 => "⚡ WEAKLY ENTANGLED",
                    _ => "❌ NOT ENTANGLED",
                };
                
                println!("Entanglement Status: {}", status);
                println!("Bell State: {:?}", bell_state);
                
                let spooky = if correlation > 0.5 {
                    "YES 🎃"
                } else {
                    "NO 👻"
                };
                
                println!("Spooky Action at a Distance: {}", spooky);
            } else {
                println!("❌ Could not analyze entanglement between files.");
            }
        }

        Some(("report", sub_matches)) => {
            let directory = sub_matches.get_one::<String>("directory").unwrap();
            
            if let Err(e) = load_directory(&mut checker, directory) {
                eprintln!("❌ Error loading directory {}: {}", directory, e);
                std::process::exit(1);
            }

            println!("{}", checker.generate_report());
        }

        Some(("decoherence", sub_matches)) => {
            let files: Vec<&String> = sub_matches.get_many::<String>("files").unwrap().collect();
            
            for file in &files {
                if let Err(e) = checker.load_file(file) {
                    eprintln!("❌ Error loading {}: {}", file, e);
                    std::process::exit(1);
                }
            }

            let indices: Vec<usize> = (0..files.len()).collect();
            
            match checker.test_decoherence(&indices) {
                Ok(correlation) => {
                    println!("🔬 Quantum Decoherence Test");
                    println!("============================");
                    println!("\nAverage Correlation: {:.3}", correlation);
                    
                    let stability = match correlation {
                        x if x > 0.7 => "HIGHLY STABLE",
                        x if x > 0.5 => "MODERATELY STABLE",
                        _ => "UNSTABLE",
                    };
                    
                    println!("Quantum Stability: {}", stability);
                    println!("\nRecommendation: {}", if correlation > 0.6 {
                        "These files maintain quantum coherence well together."
                    } else {
                        "Quantum decoherence detected. Handle with care!"
                    });
                }
                Err(e) => {
                    eprintln!("❌ Decoherence test failed: {}", e);
                    std::process::exit(1);
                }
            }
        }

        _ => {
            println!("Use --help for usage information.");
        }
    }
}

fn load_directory(checker: &mut QuantumEntanglementChecker, path: &str) -> Result<(), Box<dyn std::error::Error>> {
    let entries = fs::read_dir(path)?;
    let mut loaded = 0;
    
    for entry in entries {
        let entry = entry?;
        let path = entry.path();
        
        if path.is_file() {
            if let Some(extension) = path.extension() {
                let ext = extension.to_string_lossy().to_lowercase();
                
                // Only load source code files
                if matches!(ext.as_str(), "rs" | "py" | "js" | "ts" | "java" | "go" | "c" | "cpp" | "h") {
                    if let Ok(_) = checker.load_file(&path.to_string_lossy()) {
                        loaded += 1;
                    }
                }
            }
        }
    }
    
    if loaded == 0 {
        return Err("No suitable files found in directory".into());
    }
    
    Ok(())
}
