use std::env;
use std::process;

mod quantum_simulator;
mod utils;

use quantum_simulator::{QuantumSimulator, SimulationResult};
use utils::{display_ascii_art, display_measurement_result, get_random_particle_name};

fn main() {
    let args: Vec<String> = env::args().collect();
    
    if args.len() > 1 {
        match args[1].as_str() {
            "measure" => run_measurement(),
            "--help" | "-h" => show_help(),
            _ => run_simulation(args),
        }
    } else {
        run_simulation(args);
    }
}

fn run_simulation(args: Vec<String>) {
    println!("{}", display_ascii_art());
    
    let verbose = args.contains(&"--verbose".to_string()) || args.contains(&"-v".to_string());
    
    let particle_count = if let Some(particles_arg) = args.iter().find(|&arg| arg.starts_with("--particles=")) {
        particles_arg.trim_start_matches("--particles=").parse::<usize>().unwrap_or(2)
    } else {
        2
    };
    
    if particle_count < 2 {
        eprintln!("Error: At least 2 particles are required for entanglement");
        process::exit(1);
    }
    
    println!("\n=== QUANTUM ENTANGLEMENT SIMULATION ===\n");
    
    let mut simulator = QuantumSimulator::new(particle_count);
    let result = simulator.simulate_entanglement();
    
    display_simulation_result(&result, verbose);
}

fn run_measurement() {
    println!("{}", display_ascii_art());
    println!("\n=== QUANTUM MEASUREMENT ===\n");
    
    let simulator = QuantumSimulator::new(1);
    let measurement = simulator.measure_particle();
    
    display_measurement_result(&measurement);
}

fn show_help() {
    println!("Nightly Quantum Entanglement Simulator");
    println!("\nUsage:");
    println!("  quantum-entanglement-simulator [OPTIONS]");
    println!("  quantum-entanglement-simulator measure");
    println!("  quantum-entanglement-simulator --help");
    println!("\nOptions:");
    println!("  --particles=N    Number of particles to simulate (default: 2)");
    println!("  --verbose, -v    Enable verbose output");
    println!("  --help, -h       Show this help message");
    println!("\nCommands:");
    println!("  measure          Perform a quantum measurement");
}

fn display_simulation_result(result: &SimulationResult, verbose: bool) {
    println!("Entanglement Status: ✨ QUANTUMLY CONNECTED ✨\n");
    
    for (i, particle) in result.particles.iter().enumerate() {
        let name = get_random_particle_name(i);
        println!("Particle {} ({}): {}", i + 1, name, particle.state);
    }
    
    println!("\nMeasurement Result: {}", result.measurement_outcome);
    
    if verbose {
        println!("\nDetailed Analysis:");
        println!("  - Entanglement strength: {:.2}%", result.entanglement_strength);
        println!("  - Coherence time: {:.2} femtoseconds", result.coherence_time);
        println!("  - Quantum correlation: {}", result.quantum_correlation);
    }
    
    println!("\nExplanation: {}", result.explanation);
    
    if verbose {
        println!("\nFun Facts:");
        for fact in &result.fun_facts {
            println!("  • {}", fact);
        }
    }
}
