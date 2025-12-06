use std::env;
use std::fs;
use std::path::Path;
use serde::{Deserialize, Serialize};
use clap::{Arg, Command};
use rand::Rng;
use colored::*;

#[derive(Debug, Clone, Serialize, Deserialize)]
struct QuantumState {
    name: String,
    amplitudes: Vec<Complex>,
    fidelity: f64,
    is_entangled: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct Complex {
    real: f64,
    imag: f64,
}

impl Complex {
    fn new(real: f64, imag: f64) -> Self {
        Complex { real, imag }
    }
    
    fn magnitude_squared(&self) -> f64 {
        self.real * self.real + self.imag * self.imag
    }
    
    fn normalize(states: &mut Vec<QuantumState>) {
        for state in states.iter_mut() {
            let total_prob: f64 = state.amplitudes.iter().map(|c| c.magnitude_squared()).sum();
            let norm = total_prob.sqrt();
            for amp in state.amplitudes.iter_mut() {
                amp.real /= norm;
                amp.imag /= norm;
            }
        }
    }
}

impl std::fmt::Display for Complex {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        if self.imag >= 0.0 {
            write!(f, "{} + {}i", self.real, self.imag)
        } else {
            write!(f, "{} - {}i", self.real, self.imag.abs())
        }
    }
}

impl std::fmt::Display for QuantumState {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        writeln!(f, "{}", "=".repeat(60))?;
        writeln!(f, "{}: {}", "State Name".bold().green(), self.name.bold().yellow())?;
        writeln!(f, "{}: {}", "Fidelity".bold().cyan(), format!("{:.4}", self.fidelity).bold().magenta())?;
        writeln!(f, "{}: {}", "Entangled".bold().red(), if self.is_entangled { "Yes".bold().green() } else { "No".bold().red() })?;
        writeln!(f, "{}:", "Amplitudes".bold().blue())?;
        
        for (i, amp) in self.amplitudes.iter().enumerate() {
            writeln!(f, "  |{}⟩: {}", i, amp.to_string().bold().yellow())?;
        }
        writeln!(f, "{}", "=".repeat(60))
    }
}

fn generate_random_state(name: &str) -> QuantumState {
    let mut rng = rand::thread_rng();
    let mut amplitudes = Vec::new();
    
    // Generate random complex amplitudes for 4 basis states (2 qubits)
    for _ in 0..4 {
        let real: f64 = rng.gen_range(-1.0..1.0);
        let imag: f64 = rng.gen_range(-1.0..1.0);
        amplitudes.push(Complex::new(real, imag));
    }
    
    // Calculate fidelity (random for fun)
    let fidelity = rng.gen_range(0.7..1.0);
    
    // Determine if entangled (random for whimsy)
    let is_entangled = rng.gen_bool(0.7);
    
    QuantumState {
        name: name.to_string(),
        amplitudes,
        fidelity,
        is_entangled,
    }
}

fn generate_bell_state() -> QuantumState {
    // |Φ+⟩ = (|00⟩ + |11⟩) / √2
    let norm = 1.0 / 2_f64.sqrt();
    QuantumState {
        name: "Bell State |Φ+⟩".to_string(),
        amplitudes: vec![
            Complex::new(norm, 0.0),  // |00⟩
            Complex::new(0.0, 0.0),   // |01⟩
            Complex::new(0.0, 0.0),   // |10⟩
            Complex::new(norm, 0.0),  // |11⟩
        ],
        fidelity: 1.0,
        is_entangled: true,
    }
}

fn verify_entanglement(state: &QuantumState) -> bool {
    // Simple check: if any amplitude is zero, it might be entangled
    // This is a simplified heuristic for whimsical purposes
    let zero_count = state.amplitudes.iter().filter(|&a| a.magnitude_squared() < 1e-10).count();
    zero_count >= 2 || state.is_entangled
}

fn calculate_fidelity(state1: &QuantumState, state2: &QuantumState) -> f64 {
    // Simplified fidelity calculation for demonstration
    let mut fidelity = 0.0;
    for (a, b) in state1.amplitudes.iter().zip(state2.amplitudes.iter()) {
        fidelity += (a.real * b.real + a.imag * b.imag).abs();
    }
    fidelity.min(1.0)
}

fn export_states_to_json(states: &[QuantumState], path: &str) -> Result<(), Box<dyn std::error::Error>> {
    let json = serde_json::to_string_pretty(states)?;
    fs::write(path, json)?;
    Ok(())
}

fn main() {
    let matches = Command::new("Nightly Quantum Entanglement Checker")
        .version("1.0.0")
        .author("ApocalypsAI")
        .about("Generates and verifies quantum-like entanglement states for fun")
        .subcommand(
            Command::new("generate")
                .about("Generate random quantum states")
                .arg(
                    Arg::new("count")
                        .short('c')
                        .long("count")
                        .value_name("NUMBER")
                        .help("Number of states to generate")
                        .default_value("1")
                )
                .arg(
                    Arg::new("bell")
                        .short('b')
                        .long("bell")
                        .help("Generate Bell states instead of random states")
                )
        )
        .subcommand(
            Command::new("verify")
                .about("Verify quantum state properties")
                .arg(
                    Arg::new("fidelity")
                        .short('f')
                        .long("fidelity")
                        .value_name("FIDELITY")
                        .help("Minimum fidelity threshold")
                        .default_value("0.8")
                )
        )
        .subcommand(
            Command::new("export")
                .about("Export states to JSON")
                .arg(
                    Arg::new("count")
                        .short('c')
                        .long("count")
                        .value_name("NUMBER")
                        .help("Number of states to generate and export")
                        .default_value("5")
                )
                .arg(
                    Arg::new("output")
                        .short('o')
                        .long("output")
                        .value_name("FILE")
                        .help("Output JSON file path")
                        .default_value("quantum_states.json")
                )
        )
        .subcommand(
            Command::new("bell-test")
                .about("Run Bell inequality test simulation")
        )
        .get_matches();

    match matches.subcommand() {
        Some(("generate", sub_matches)) => {
            let count: usize = sub_matches.get_one::<String>("count").unwrap().parse().expect("Invalid count");
            let generate_bell = sub_matches.get_flag("bell");
            
            println!("{}", "Generating Quantum States...".bold().green());
            println!("{}
", "=".repeat(60));
            
            let mut states = Vec::new();
            
            if generate_bell {
                for i in 0..count {
                    let mut state = generate_bell_state();
                    state.name = format!("Bell State {}", i + 1);
                    states.push(state);
                }
            } else {
                for i in 0..count {
                    let state = generate_random_state(&format!("Random State {}", i + 1));
                    states.push(state);
                }
            }
            
            // Normalize states
            Complex::normalize(&mut states);
            
            // Display states
            for state in &states {
                println!("{}
", state);
            }
        },
        
        Some(("verify", sub_matches)) => {
            let min_fidelity: f64 = sub_matches.get_one::<String>("fidelity").unwrap().parse().expect("Invalid fidelity");
            
            println!("{}", "Verifying Quantum States...".bold().cyan());
            println!("{}
", "=".repeat(60));
            
            // Generate test states
            let mut states = vec![
                generate_bell_state(),
                generate_random_state("Test State"),
            ];
            Complex::normalize(&mut states);
            
            for state in &states {
                let is_valid = verify_entanglement(state) && state.fidelity >= min_fidelity;
                println!("{}: {}", state.name.bold().yellow(), if is_valid { "✓ VALID".bold().green() } else { "✗ INVALID".bold().red() });
                println!("  Entanglement: {}", if state.is_entangled { "Yes".bold().green() } else { "No".bold().red() });
                println!("  Fidelity: {:.4}", state.fidelity);
                println!();
            }
        },
        
        Some(("export", sub_matches)) => {
            let count: usize = sub_matches.get_one::<String>("count").unwrap().parse().expect("Invalid count");
            let output_path = sub_matches.get_one::<String>("output").unwrap();
            
            println!("{}", format!("Generating and exporting {} states to {}", count, output_path).bold().magenta());
            
            let mut states = Vec::new();
            for i in 0..count {
                let state = generate_random_state(&format!("Export State {}", i + 1));
                states.push(state);
            }
            Complex::normalize(&mut states);
            
            match export_states_to_json(&states, output_path) {
                Ok(()) => println!("{}", "Export successful!".bold().green()),
                Err(e) => println!("{}: {}", "Export failed".bold().red(), e),
            }
        },
        
        Some(("bell-test", _)) => {
            println!("{}", "Running Bell Inequality Test Simulation...".bold().red());
            println!("{}
", "=".repeat(60));
            
            let bell_state = generate_bell_state();
            let random_state = generate_random_state("Random");
            Complex::normalize(&mut vec![bell_state.clone(), random_state.clone()]);
            
            let fidelity = calculate_fidelity(&bell_state, &random_state);
            
            println!("Bell State: {}", bell_state.name.bold().yellow());
            println!("Random State: {}", random_state.name.bold().cyan());
            println!("Fidelity between states: {:.4}", fidelity);
            
            if fidelity > 0.8 {
                println!("{}: Strong correlation detected!".bold().green(), "✓ BELL INEQUALITY VIOLATION".bold().red());
            } else {
                println!("{}: Classical behavior observed.".bold().blue(), "- NO VIOLATION".bold().yellow());
            }
        },
        
        _ => {
            println!("{}", "Welcome to the Quantum Entanglement Checker!".bold().bright_magenta());
            println!("{}
", "=".repeat(60));
            println!("Use --help for usage information.");
        }
    }
}
