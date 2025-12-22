use clap::{Arg, Command};
use rand::prelude::*;
use std::collections::HashMap;

mod quantum;
mod bell_states;
mod statistics;

use quantum::{QuantumState, MeasurementBasis};
use bell_states::{BellState, BellStateType};
use statistics::Statistics;

fn main() {
    let matches = Command::new("Nightly Quantum Entanglement Checker")
        .version("1.0.0")
        .author("ApocalypsAI")
        .about("Simulates quantum entanglement verification using Bell state measurements")
        .subcommand(
            Command::new("check-entanglement")
                .about("Check entanglement between simulated qubits")
                .arg(
                    Arg::new("qubits")
                        .short('q')
                        .long("qubits")
                        .value_name("NUMBER")
                        .help("Number of qubits to simulate")
                        .default_value("2")
                )
                .arg(
                    Arg::new("trials")
                        .short('t')
                        .long("trials")
                        .value_name("NUMBER")
                        .help("Number of measurement trials")
                        .default_value("1000")
                )
        )
        .subcommand(
            Command::new("distributed")
                .about("Simulate entanglement across distributed nodes")
                .arg(
                    Arg::new("nodes")
                        .short('n')
                        .long("nodes")
                        .value_name("NUMBER")
                        .help("Number of distributed nodes")
                        .default_value("4")
                )
                .arg(
                    Arg::new("trials")
                        .short('t')
                        .long("trials")
                        .value_name("NUMBER")
                        .help("Number of trials per node")
                        .default_value("500")
                )
        )
        .subcommand(
            Command::new("bell-state")
                .about("Analyze Bell state measurements")
                .arg(
                    Arg::new("state")
                        .short('s')
                        .long("state")
                        .value_name("STATE")
                        .help("Bell state type (phi-plus, phi-minus, psi-plus, psi-minus)")
                        .default_value("phi-plus")
                )
                .arg(
                    Arg::new("measurements")
                        .short('m')
                        .long("measurements")
                        .value_name("NUMBER")
                        .help("Number of measurements")
                        .default_value("100")
                )
        )
        .get_matches();

    match matches.subcommand() {
        Some(("check-entanglement", sub_matches)) => {
            let qubits: usize = sub_matches.get_one::<String>("qubits").unwrap().parse().unwrap();
            let trials: usize = sub_matches.get_one::<String>("trials").unwrap().parse().unwrap();
            
            println!("\nQuantum Entanglement Verification Results:");
            println!("----------------------------------------");
            println!("Qubits: {}", qubits);
            println!("Trials: {}", trials);
            
            let fidelity = simulate_entanglement_check(qubits, trials);
            println!("Entanglement Fidelity: {:.3}", fidelity);
            
            let bell_violation = calculate_bell_inequality_violation(trials);
            println!("Bell Inequality Violation: {:.2}", bell_violation);
            
            if bell_violation > 2.0 {
                println!("\nInterpretation: Strong entanglement detected!");
                println!("Classical limit: 2.0, Quantum result: {:.2}", bell_violation);
            } else {
                println!("\nInterpretation: No significant entanglement detected.");
                println!("Result within classical bounds.");
            }
        }
        Some(("distributed", sub_matches)) => {
            let nodes: usize = sub_matches.get_one::<String>("nodes").unwrap().parse().unwrap();
            let trials: usize = sub_matches.get_one::<String>("trials").unwrap().parse().unwrap();
            
            println!("\nDistributed Entanglement Simulation:");
            println!("-----------------------------------");
            println!("Nodes: {}", nodes);
            println!("Trials per node: {}", trials);
            
            let results = simulate_distributed_entanglement(nodes, trials);
            
            let global_fidelity: f64 = results.values().sum::<f64>() / nodes as f64;
            println!("Global entanglement fidelity: {:.3}", global_fidelity);
            
            let sync_rate = calculate_synchronization_rate(&results);
            println!("Network synchronization: {:.1}%", sync_rate * 100.0);
            
            println!("\nNode Results:");
            for (node, fidelity) in results {
                println!("Node {}: Fidelity {:.3}", node, fidelity);
            }
        }
        Some(("bell-state", sub_matches)) => {
            let state_str = sub_matches.get_one::<String>("state").unwrap();
            let measurements: usize = sub_matches.get_one::<String>("measurements").unwrap().parse().unwrap();
            
            let bell_state = match state_str.as_str() {
                "phi-plus" => BellState::new(BellStateType::PhiPlus),
                "phi-minus" => BellState::new(BellStateType::PhiMinus),
                "psi-plus" => BellState::new(BellStateType::PsiPlus),
                "psi-minus" => BellState::new(BellStateType::PsiMinus),
                _ => {
                    eprintln!("Invalid Bell state. Use: phi-plus, phi-minus, psi-plus, psi-minus");
                    return;
                }
            };
            
            println!("\nBell State Analysis:");
            println!("-------------------");
            println!("State: {}", bell_state.get_type());
            println!("Measurements: {}", measurements);
            
            let correlations = bell_state.analyze_measurements(measurements);
            
            println!("\nMeasurement Correlations:");
            for (basis, correlation) in correlations {
                println!("{}: {:.3}", basis, correlation);
            }
            
            let chsh_value = calculate_chsh_inequality(&correlations);
            println!("\nCHSH Inequality Value: {:.3}", chsh_value);
            
            if chsh_value > 2.0 {
                println!("Result violates classical CHSH inequality!");
                println!("Quantum entanglement confirmed.");
            } else {
                println!("Result within classical bounds.");
            }
        }
        _ => {
            println!("Use --help for usage information.");
        }
    }
}

fn simulate_entanglement_check(qubits: usize, trials: usize) -> f64 {
    let mut rng = thread_rng();
    let mut entangled_pairs = 0;
    
    for _ in 0..trials {
        // Create entangled qubit pair
        let state1 = QuantumState::random(&mut rng);
        let state2 = QuantumState::entangled_copy(&state1);
        
        // Measure in random basis
        let basis = MeasurementBasis::random(&mut rng);
        let result1 = state1.measure(&basis);
        let result2 = state2.measure(&basis);
        
        // Check if measurements are correlated (entangled)
        if result1 == result2 {
            entangled_pairs += 1;
        }
    }
    
    entangled_pairs as f64 / trials as f64
}

fn calculate_bell_inequality_violation(trials: usize) -> f64 {
    let mut rng = thread_rng();
    let mut correlations = HashMap::new();
    
    // Measure in different basis combinations
    let bases = [
        (MeasurementBasis::Z, MeasurementBasis::Z),
        (MeasurementBasis::X, MeasurementBasis::X),
        (MeasurementBasis::Z, MeasurementBasis::X),
        (MeasurementBasis::X, MeasurementBasis::Z),
    ];
    
    for (basis_a, basis_b) in bases.iter() {
        let mut correlation = 0.0;
        
        for _ in 0..trials {
            let state = QuantumState::random(&mut rng);
            let entangled = QuantumState::entangled_copy(&state);
            
            let result_a = state.measure(basis_a);
            let result_b = entangled.measure(basis_b);
            
            // Calculate correlation
            correlation += if result_a == result_b { 1.0 } else { -1.0 };
        }
        
        let key = format!("{:?}-{:?}", basis_a, basis_b);
        correlations.insert(key, correlation / trials as f64);
    }
    
    // Calculate CHSH inequality
    let chsh = correlations["Z-Z"].abs() + correlations["X-X"].abs() + 
               correlations["Z-X"].abs() + correlations["X-Z"].abs();
    
    chsh
}

fn simulate_distributed_entanglement(nodes: usize, trials: usize) -> HashMap<usize, f64> {
    let mut results = HashMap::new();
    
    for node in 1..=nodes {
        let fidelity = simulate_entanglement_check(2, trials);
        results.insert(node, fidelity);
    }
    
    results
}

fn calculate_synchronization_rate(results: &HashMap<usize, f64>) -> f64 {
    let values: Vec<f64> = results.values().cloned().collect();
    let mean = values.iter().sum::<f64>() / values.len() as f64;
    
    let variance = values.iter().map(|&x| (x - mean).powi(2)).sum::<f64>() / values.len() as f64;
    let std_dev = variance.sqrt();
    
    // Synchronization rate based on standard deviation
    1.0 - (std_dev / mean).min(1.0)
}

fn calculate_chsh_inequality(correlations: &HashMap<String, f64>) -> f64 {
    // CHSH inequality: |E(a,b) - E(a,b') + E(a',b) + E(a',b')| <= 2
    let e_ab = correlations.get("Z-Z").unwrap_or(&0.0);
    let e_ab_prime = correlations.get("Z-X").unwrap_or(&0.0);
    let e_a_prime_b = correlations.get("X-Z").unwrap_or(&0.0);
    let e_a_prime_b_prime = correlations.get("X-X").unwrap_or(&0.0);
    
    (e_ab - e_ab_prime + e_a_prime_b + e_a_prime_b_prime).abs()
}
