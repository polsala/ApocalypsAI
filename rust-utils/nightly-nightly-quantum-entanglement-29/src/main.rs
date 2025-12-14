use std::env;
use std::time::Instant;
use std::collections::HashMap;

mod quantum_simulator;
mod bell_test;
mod visualization;

use quantum_simulator::QuantumSimulator;
use bell_test::BellTest;
use visualization::Visualizer;

const DEFAULT_NODES: usize = 4;
const DEFAULT_TRIALS: usize = 1000;
const DEFAULT_SEED: u64 = 12345;

#[derive(Debug)]
struct Config {
    nodes: usize,
    trials: usize,
    seed: u64,
    visualize: bool,
}

impl Default for Config {
    fn default() -> Self {
        Self {
            nodes: DEFAULT_NODES,
            trials: DEFAULT_TRIALS,
            seed: DEFAULT_SEED,
            visualize: false,
        }
    }
}

fn parse_args() -> Config {
    let mut config = Config::default();
    let args: Vec<String> = env::args().collect();
    
    let mut i = 1;
    while i < args.len() {
        match args[i].as_str() {
            "--nodes" => {
                if i + 1 < args.len() {
                    config.nodes = args[i + 1].parse().expect("--nodes must be a number");
                    i += 2;
                } else {
                    print_usage();
                    std::process::exit(1);
                }
            },
            "--trials" => {
                if i + 1 < args.len() {
                    config.trials = args[i + 1].parse().expect("--trials must be a number");
                    i += 2;
                } else {
                    print_usage();
                    std::process::exit(1);
                }
            },
            "--seed" => {
                if i + 1 < args.len() {
                    config.seed = args[i + 1].parse().expect("--seed must be a number");
                    i += 2;
                } else {
                    print_usage();
                    std::process::exit(1);
                }
            },
            "--visualize" => {
                config.visualize = true;
                i += 1;
            },
            "--help" | "-h" => {
                print_usage();
                std::process::exit(0);
            },
            _ => {
                eprintln!("Unknown argument: {}", args[i]);
                print_usage();
                std::process::exit(1);
            },
        }
    }
    
    config
}

fn print_usage() {
    println!("Quantum Entanglement Checker - Verify quantum correlations across distributed nodes\n");
    println!("Usage: nightly-quantum-entanglement-checker [OPTIONS]\n");
    println!("Options:");
    println!("  --nodes N      Number of entangled nodes (default: {})", DEFAULT_NODES);
    println!("  --trials N     Number of measurement trials (default: {})", DEFAULT_TRIALS);
    println!("  --seed N       Random seed for deterministic results (default: {})", DEFAULT_SEED);
    println!("  --visualize    Enable ASCII visualization of quantum states");
    println!("  --help, -h     Show this help message\n");
    println!("Example:");
    println!("  cargo run -- --nodes 4 --trials 1000 --seed 42 --visualize");
}

fn main() {
    let config = parse_args();
    
    println!("=== Quantum Entanglement Verification ===");
    println!("Nodes: {}, Trials: {}, Seed: {}", config.nodes, config.trials, config.seed);
    println!();
    
    let mut simulator = QuantumSimulator::new(config.seed);
    let mut bell_test = BellTest::new();
    let mut visualizer = Visualizer::new(config.visualize);
    
    // Generate entangled states across nodes
    let start_time = Instant::now();
    let entangled_states = simulator.generate_entangled_states(config.nodes, config.trials);
    let generation_time = start_time.elapsed();
    
    // Perform Bell test
    let start_time = Instant::now();
    let chsh_result = bell_test.test_chsh_inequality(&entangled_states);
    let test_time = start_time.elapsed();
    
    // Visualize results
    visualizer.show_entangled_states(&entangled_states);
    println!();
    
    // Show Bell test results
    visualizer.show_bell_test_results(&chsh_result);
    println!();
    
    // Performance metrics
    let total_time = generation_time + test_time;
    let throughput = config.trials as f64 / total_time.as_secs_f64();
    
    println!("Performance:");
    println!("Latency: {}ms, Throughput: {:.0} ops/sec", 
             total_time.as_millis(), throughput);
    
    // Determine entanglement status
    if chsh_result.s_value > 2.0 {
        println!("\n✓ Entanglement verified! (S > 2.0)");
        println!("Quantum correlations detected above classical limits.");
    } else {
        println!("\n✗ No entanglement detected (S ≤ 2.0)");
        println!("Results consistent with classical correlations.");
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_parse_args_default() {
        // Test with no arguments (uses defaults)
        let config = Config::default();
        assert_eq!(config.nodes, DEFAULT_NODES);
        assert_eq!(config.trials, DEFAULT_TRIALS);
        assert_eq!(config.seed, DEFAULT_SEED);
        assert_eq!(config.visualize, false);
    }
    
    #[test]
    fn test_quantum_simulation_deterministic() {
        // Test that same seed produces same results
        let mut sim1 = QuantumSimulator::new(42);
        let mut sim2 = QuantumSimulator::new(42);
        
        let states1 = sim1.generate_entangled_states(3, 100);
        let states2 = sim2.generate_entangled_states(3, 100);
        
        assert_eq!(states1, states2);
    }
    
    #[test]
    fn test_chsh_classical_limit() {
        // Test with classical (non-entangled) data
        let classical_states = vec![
            (0.0, 0.0, 1.0, 1.0), // Classical correlation
            (1.0, 1.0, 0.0, 0.0),
        ];
        
        let mut bell_test = BellTest::new();
        let result = bell_test.test_chsh_inequality(&classical_states);
        
        // Classical limit should be ≤ 2.0
        assert!(result.s_value <= 2.0);
    }
}
