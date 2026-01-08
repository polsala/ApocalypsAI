use std::env;
use std::process;
use std::time::{Duration, Instant};

mod quantum;
mod visualization;

use quantum::{EntangledPair, MeasurementBasis, QuantumState};
use visualization::{clear_screen, print_header, print_particle_state, print_measurement_result};

#[derive(Debug)]
struct Config {
    particles: usize,
    measurements: usize,
    entanglement_strength: f64,
    verbose: bool,
}

impl Default for Config {
    fn default() -> Self {
        Self {
            particles: 5,
            measurements: 3,
            entanglement_strength: 0.9,
            verbose: false,
        }
    }
}

fn parse_args() -> Config {
    let mut config = Config::default();
    let args: Vec<String> = env::args().collect();
    
    let mut i = 1;
    while i < args.len() {
        match args[i].as_str() {
            "--particles" => {
                if i + 1 < args.len() {
                    config.particles = args[i + 1].parse().unwrap_or_else(|_| {
                        eprintln!("Error: Invalid number for --particles");
                        process::exit(1);
                    });
                    i += 2;
                } else {
                    eprintln!("Error: --particles requires a number");
                    process::exit(1);
                }
            }
            "--measurements" => {
                if i + 1 < args.len() {
                    config.measurements = args[i + 1].parse().unwrap_or_else(|_| {
                        eprintln!("Error: Invalid number for --measurements");
                        process::exit(1);
                    });
                    i += 2;
                } else {
                    eprintln!("Error: --measurements requires a number");
                    process::exit(1);
                }
            }
            "--entanglement" => {
                if i + 1 < args.len() {
                    config.entanglement_strength = args[i + 1].parse().unwrap_or_else(|_| {
                        eprintln!("Error: Invalid number for --entanglement (must be 0.0-1.0)");
                        process::exit(1);
                    });
                    if config.entanglement_strength < 0.0 || config.entanglement_strength > 1.0 {
                        eprintln!("Error: --entanglement must be between 0.0 and 1.0");
                        process::exit(1);
                    }
                    i += 2;
                } else {
                    eprintln!("Error: --entanglement requires a number");
                    process::exit(1);
                }
            }
            "--verbose" => {
                config.verbose = true;
                i += 1;
            }
            "--help" => {
                print_help();
                process::exit(0);
            }
            _ => {
                eprintln!("Unknown option: {}", args[i]);
                print_help();
                process::exit(1);
            }
        }
    }
    
    config
}

fn print_help() {
    println!("Quantum Entanglement Simulator");
    println!("===============================");
    println!("");
    println!("Usage: nightly-quantum-entanglement-simulator [OPTIONS]");
    println!("");
    println!("Options:");
    println!("  --particles N     Number of entangled particle pairs (default: 5)");
    println!("  --measurements N  Number of measurements to perform (default: 3)");
    println!("  --entanglement N  Entanglement strength (0.0-1.0, default: 0.9)");
    println!("  --verbose         Show detailed measurement information");
    println!("  --help            Show this help message");
    println!("");
    println!("Examples:");
    println!("  ./quantum_simulator");
    println!("  ./quantum_simulator --particles 10 --measurements 5");
    println!("  ./quantum_simulator --entanglement 0.5 --verbose");
}

fn main() {
    let config = parse_args();
    
    // Clear screen and print header
    clear_screen();
    print_header();
    
    println!("Configuration:");
    println!("  Particles: {} pairs", config.particles);
    println!("  Measurements: {} per pair", config.measurements);
    println!("  Entanglement Strength: {:.1}%", config.entanglement_strength * 100.0);
    if config.verbose {
        println!("  Mode: Verbose");
    }
    println!("");
    
    // Create entangled particle pairs
    let mut pairs: Vec<EntangledPair> = Vec::with_capacity(config.particles);
    for i in 0..config.particles {
        let pair = EntangledPair::new(config.entanglement_strength);
        pairs.push(pair);
        
        if config.verbose {
            println!("Particle Pair {}:", i + 1);
            print_particle_state(&pairs[i].alice);
            print_particle_state(&pairs[i].bob);
            println!("  Entanglement: {} ({:.0}%)",
                visualization::progress_bar(config.entanglement_strength),
                config.entanglement_strength * 100.0);
            println!("");
        }
    }
    
    // Perform measurements
    for measurement_num in 1..=config.measurements {
        println!("Measurement {}:", measurement_num);
        
        let start_time = Instant::now();
        
        for (i, pair) in pairs.iter_mut().enumerate() {
            // Randomly choose measurement basis
            let basis = MeasurementBasis::random();
            
            // Measure Alice's particle
            let alice_result = pair.measure_alice(basis);
            
            // Measure Bob's particle (with entanglement effect)
            let bob_result = pair.measure_bob(basis);
            
            // Check correlation
            let correlated = pair.check_correlation();
            
            if config.verbose {
                print_measurement_result(
                    i + 1,
                    basis,
                    &alice_result,
                    &bob_result,
                    correlated
                );
            }
        }
        
        let elapsed = start_time.elapsed();
        println!("  Measurement time: {:.2}ms", elapsed.as_secs_f64() * 1000.0);
        println!("");
        
        // Small delay to simulate quantum computation time
        std::thread::sleep(Duration::from_millis(100));
    }
    
    println!("=== Simulation Complete ===");
    println!("");
    println!("Key Concepts Demonstrated:");
    println!("  ✓ Superposition: Particles exist in multiple states");
    println!("  ✓ Entanglement: Particles become correlated");
    println!("  ✓ Measurement: Observing collapses the state");
    println!("  ✓ Non-locality: Instant correlation regardless of distance");
    println!("");
    println!("Remember: Spooky action at a distance is real! 🎃⚛️");
}
