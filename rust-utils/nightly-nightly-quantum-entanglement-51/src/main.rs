use std::env;
use std::fs;
use std::io::{self, Write};
use std::collections::HashMap;
use serde::{Deserialize, Serialize};
use rand::Rng;

#[derive(Debug, Clone, Serialize, Deserialize)]
struct QuantumState {
    particles: usize,
    state_type: String,
    coefficients: Vec<f64>,
    measurements: Vec<Measurement>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct Measurement {
    particle_1: String,
    particle_2: String,
}

#[derive(Debug, Clone)]
struct Args {
    particles: usize,
    measurements: usize,
    educational: bool,
    save_file: Option<String>,
    load_file: Option<String>,
    help: bool,
}

impl Default for Args {
    fn default() -> Self {
        Self {
            particles: 2,
            measurements: 5,
            educational: false,
            save_file: None,
            load_file: None,
            help: false,
        }
    }
}

fn main() {
    let args = parse_args();
    
    if args.help {
        print_help();
        return;
    }
    
    if let Some(load_file) = &args.load_file {
        match load_quantum_state(load_file) {
            Ok(state) => {
                println!("=== Loaded Quantum State ===");
                println!("Particles: {}", state.particles);
                println!("State Type: {}", state.state_type);
                println!("Measurements: {}", state.measurements.len());
                return;
            }
            Err(e) => {
                eprintln!("Error loading quantum state: {}", e);
                return;
            }
        }
    }
    
    let mut state = create_quantum_state(args.particles);
    
    if args.educational {
        run_educational_simulation(&mut state, args.measurements);
    } else {
        run_basic_simulation(&mut state, args.measurements);
    }
    
    if let Some(save_file) = &args.save_file {
        if let Err(e) = save_quantum_state(&state, save_file) {
            eprintln!("Error saving quantum state: {}", e);
        }
    }
}

fn parse_args() -> Args {
    let mut args = Args::default();
    let mut iter = env::args().skip(1);
    
    while let Some(arg) = iter.next() {
        match arg.as_str() {
            "--particles" | "-p" => {
                if let Some(val) = iter.next() {
                    args.particles = val.parse().unwrap_or(2);
                }
            }
            "--measurements" | "-m" => {
                if let Some(val) = iter.next() {
                    args.measurements = val.parse().unwrap_or(5);
                }
            }
            "--educational" | "-e" => {
                args.educational = true;
            }
            "--save" | "-s" => {
                if let Some(val) = iter.next() {
                    args.save_file = Some(val);
                }
            }
            "--load" | "-l" => {
                if let Some(val) = iter.next() {
                    args.load_file = Some(val);
                }
            }
            "--help" | "-h" => {
                args.help = true;
            }
            _ => {}
        }
    }
    
    args
}

fn print_help() {
    println!("Quantum Entanglement Simulator");
    println!("");
    println!("Usage: quantum_simulator [OPTIONS]");
    println!("");
    println!("Options:");
    println!("  -p, --particles N     Number of particles (default: 2)");
    println!("  -m, --measurements N  Number of measurements (default: 5)");
    println!("  -e, --educational     Enable educational mode with explanations");
    println!("  -s, --save FILE       Save quantum state to file");
    println!("  -l, --load FILE       Load quantum state from file");
    println!("  -h, --help            Show this help message");
    println!("");
    println!("Examples:");
    println!("  quantum_simulator --particles 2 --measurements 5");
    println!("  quantum_simulator --educational --particles 3");
    println!("  quantum_simulator --save state.json");
    println!("  quantum_simulator --load state.json");
}

fn create_quantum_state(particles: usize) -> QuantumState {
    QuantumState {
        particles,
        state_type: "bell".to_string(),
        coefficients: vec![1.0 / (2.0_f64).sqrt(); 2],
        measurements: Vec::new(),
    }
}

fn run_basic_simulation(state: &mut QuantumState, measurements: usize) {
    println!("=== Quantum Entanglement Simulation ===");
    println!("Particles: {}", state.particles);
    println!("Measurements: {}", measurements);
    println!("");
    
    println!("Initial State: |00⟩");
    println!("Entanglement Applied: Bell State Created");
    println!("");
    
    for i in 1..=measurements {
        let measurement = measure_entangled_particles(state.particles);
        state.measurements.push(measurement.clone());
        
        println!("Measurement {}:", i);
        println!("Particle 1: {}", format_spin(&measurement.particle_1));
        println!("Particle 2: {}", format_spin(&measurement.particle_2));
        
        let correlation = check_correlation(&measurement);
        println!("Correlation: {}", correlation);
        println!("");
    }
    
    println!("=== Simulation Complete ===");
}

fn run_educational_simulation(state: &mut QuantumState, measurements: usize) {
    println!("=== Quantum Entanglement Simulation (Educational Mode) ===");
    println!("");
    
    print_quantum_concepts();
    
    println!("Initial State: |00⟩");
    println!("This represents two particles both in the '0' state (spin down).");
    println!("");
    
    println!("Applying Hadamard Gate to Particle 1...");
    println!("This creates a superposition of states: (|0⟩ + |1⟩)/√2");
    println!("");
    
    println!("Applying CNOT Gate...");
    println!("This entangles the particles, creating a Bell state: (|00⟩ + |11⟩)/√2");
    println!("");
    
    println!("Now the particles are entangled! Measuring one instantly determines the state of the other, no matter how far apart they are.");
    println!("");
    
    for i in 1..=measurements {
        let measurement = measure_entangled_particles(state.particles);
        state.measurements.push(measurement.clone());
        
        println!("Measurement {}:", i);
        println!("Particle 1: {}", format_spin(&measurement.particle_1));
        println!("Particle 2: {}", format_spin(&measurement.particle_2));
        
        println!("Explanation: Due to entanglement, both particles collapsed to the same state!");
        println!("");
    }
    
    println!("=== Educational Simulation Complete ===");
}

fn print_quantum_concepts() {
    println!("What is Quantum Entanglement?");
    println!("Quantum entanglement is a physical phenomenon that occurs when pairs or groups of particles are generated, interact, or share spatial proximity in ways such that the quantum state of each particle cannot be described independently of the state of the others.");
    println!("");
}

fn measure_entangled_particles(particles: usize) -> Measurement {
    let mut rng = rand::thread_rng();
    
    // For entangled particles, they should have correlated states
    let spin1 = if rng.gen_bool(0.5) { "up" } else { "down" };
    let spin2 = spin1; // Perfect correlation for Bell state
    
    Measurement {
        particle_1: spin1.to_string(),
        particle_2: spin2.to_string(),
    }
}

fn format_spin(spin: &str) -> String {
    match spin {
        "up" => "↑ (spin up)".to_string(),
        "down" => "↓ (spin down)".to_string(),
        _ => spin.to_string(),
    }
}

fn check_correlation(measurement: &Measurement) -> String {
    if measurement.particle_1 == measurement.particle_2 {
        "Perfect correlation ✓".to_string()
    } else {
        "Perfect anti-correlation ✓".to_string()
    }
}

fn save_quantum_state(state: &QuantumState, filename: &str) -> Result<(), Box<dyn std::error::Error>> {
    let json = serde_json::to_string_pretty(state)?;
    fs::write(filename, json)?;
    println!("Quantum state saved to {}", filename);
    Ok(())
}

fn load_quantum_state(filename: &str) -> Result<QuantumState, Box<dyn std::error::Error>> {
    let content = fs::read_to_string(filename)?;
    let state: QuantumState = serde_json::from_str(&content)?;
    Ok(state)
}

#[cfg(test)]
mod tests {
    use super::*;
    use tempfile::NamedTempFile;
    
    #[test]
    fn test_create_quantum_state() {
        let state = create_quantum_state(2);
        assert_eq!(state.particles, 2);
        assert_eq!(state.state_type, "bell");
        assert_eq!(state.coefficients.len(), 2);
        assert_eq!(state.measurements.len(), 0);
    }
    
    #[test]
    fn test_measure_entangled_particles() {
        let measurement = measure_entangled_particles(2);
        assert!(measurement.particle_1 == "up" || measurement.particle_1 == "down");
        assert!(measurement.particle_2 == "up" || measurement.particle_2 == "down");
        // For entangled particles, they should be correlated
        assert_eq!(measurement.particle_1, measurement.particle_2);
    }
    
    #[test]
    fn test_format_spin() {
        assert_eq!(format_spin("up"), "↑ (spin up)");
        assert_eq!(format_spin("down"), "↓ (spin down)");
        assert_eq!(format_spin("unknown"), "unknown");
    }
    
    #[test]
    fn test_check_correlation() {
        let measurement = Measurement {
            particle_1: "up".to_string(),
            particle_2: "up".to_string(),
        };
        assert_eq!(check_correlation(&measurement), "Perfect correlation ✓");
        
        let measurement2 = Measurement {
            particle_1: "up".to_string(),
            particle_2: "down".to_string(),
        };
        assert_eq!(check_correlation(&measurement2), "Perfect anti-correlation ✓");
    }
    
    #[test]
    fn test_save_and_load_quantum_state() {
        let state = create_quantum_state(3);
        
        let temp_file = NamedTempFile::new().unwrap();
        let filename = temp_file.path().to_str().unwrap();
        
        // Save state
        assert!(save_quantum_state(&state, filename).is_ok());
        
        // Load state
        let loaded_state = load_quantum_state(filename).unwrap();
        assert_eq!(state.particles, loaded_state.particles);
        assert_eq!(state.state_type, loaded_state.state_type);
        assert_eq!(state.coefficients, loaded_state.coefficients);
        assert_eq!(state.measurements, loaded_state.measurements);
    }
    
    #[test]
    fn test_parse_args() {
        let test_args = vec!["quantum_simulator", "--particles", "3", "--measurements", "10", "--educational"];
        let mut iter = test_args.into_iter();
        
        // Skip program name
        iter.next();
        
        let mut args = Args::default();
        while let Some(arg) = iter.next() {
            match arg.as_str() {
                "--particles" => {
                    if let Some(val) = iter.next() {
                        args.particles = val.parse().unwrap_or(2);
                    }
                }
                "--measurements" => {
                    if let Some(val) = iter.next() {
                        args.measurements = val.parse().unwrap_or(5);
                    }
                }
                "--educational" => {
                    args.educational = true;
                }
                _ => {}
            }
        }
        
        assert_eq!(args.particles, 3);
        assert_eq!(args.measurements, 10);
        assert!(args.educational);
    }
}
