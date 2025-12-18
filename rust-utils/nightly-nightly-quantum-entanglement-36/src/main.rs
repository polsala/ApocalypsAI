use std::collections::HashMap;
use std::env;
use std::time::Instant;
use clap::{App, Arg};

mod quantum_simulator;
mod measurement;
mod fidelity_calculator;

use quantum_simulator::QuantumSimulator;
use measurement::{MeasurementBasis, MeasurementOutcome};
use fidelity_calculator::FidelityCalculator;

const VERSION: &str = env!("CARGO_PKG_VERSION");
const AUTHORS: &str = env!("CARGO_PKG_AUTHORS");

fn main() {
    let matches = App::new("Nightly Quantum Entanglement Checker")
        .version(VERSION)
        .author(AUTHORS)
        .about("Simulates quantum entanglement verification for distributed systems")
        .arg(
            Arg::with_name("nodes")
                .short("n")
                .long("nodes")
                .value_name("NUMBER")
                .help("Number of nodes in the system")
                .takes_value(true)
                .default_value("4"),
        )
        .arg(
            Arg::with_name("measurements")
                .short("m")
                .long("measurements")
                .value_name("NUMBER")
                .help("Number of measurements per node pair")
                .takes_value(true)
                .default_value("1000"),
        )
        .arg(
            Arg::with_name("fidelity-threshold")
                .short("t")
                .long("fidelity-threshold")
                .value_name("THRESHOLD")
                .help("Fidelity threshold for entanglement detection (0.0-1.0)")
                .takes_value(true)
                .default_value("0.80"),
        )
        .arg(
            Arg::with_name("output-format")
                .short("f")
                .long("output-format")
                .value_name("FORMAT")
                .help("Output format: text or json")
                .takes_value(true)
                .default_value("text"),
        )
        .arg(
            Arg::with_name("quiet")
                .short("q")
                .long("quiet")
                .help("Suppress whimsical output messages")
                .takes_value(false),
        )
        .get_matches();

    // Parse arguments
    let num_nodes: usize = matches
        .value_of("nodes")
        .unwrap()
        .parse()
        .expect("Nodes must be a positive integer");

    let num_measurements: usize = matches
        .value_of("measurements")
        .unwrap()
        .parse()
        .expect("Measurements must be a positive integer");

    let fidelity_threshold: f64 = matches
        .value_of("fidelity-threshold")
        .unwrap()
        .parse()
        .expect("Fidelity threshold must be a float between 0.0 and 1.0");

    let output_format = matches.value_of("output-format").unwrap();
    let quiet = matches.is_present("quiet");

    // Validate inputs
    if num_nodes < 2 {
        eprintln!("Error: Number of nodes must be at least 2");
        std::process::exit(1);
    }

    if num_measurements == 0 {
        eprintln!("Error: Number of measurements must be greater than 0");
        std::process::exit(1);
    }

    if fidelity_threshold < 0.0 || fidelity_threshold > 1.0 {
        eprintln!("Error: Fidelity threshold must be between 0.0 and 1.0");
        std::process::exit(1);
    }

    // Run the quantum entanglement checker
    let start_time = Instant::now();
    
    let simulator = QuantumSimulator::new(num_nodes, num_measurements);
    let measurements = simulator.simulate_entanglement();
    
    let calculator = FidelityCalculator::new(fidelity_threshold);
    let results = calculator.calculate_fidelities(&measurements);
    
    let duration = start_time.elapsed();

    // Output results
    if output_format == "json" {
        output_json(&results, num_nodes, num_measurements, fidelity_threshold, duration);
    } else {
        output_text(&results, num_nodes, num_measurements, fidelity_threshold, duration, quiet);
    }
}

fn output_text(
    results: &HashMap<(usize, usize), f64>,
    num_nodes: usize,
    num_measurements: usize,
    fidelity_threshold: f64,
    duration: std::time::Duration,
    quiet: bool,
) {
    println!("🌌 Quantum Entanglement Verification Report 🌌\n");
    
    println!(
        "Nodes: {} | Measurements: {} | Fidelity Threshold: {:.2}",
        num_nodes, num_measurements, fidelity_threshold
    );
    println!();
    
    let mut entangled_pairs = 0;
    let mut total_pairs = 0;
    
    println!("📊 Entanglement Fidelity Scores:");
    
    for ((node1, node2), fidelity) in results.iter().sorted() {
        total_pairs += 1;
        
        let status = if *fidelity >= fidelity_threshold {
            entangled_pairs += 1;
            "✨ (Strongly entangled)"
        } else {
            "❌ (Not entangled)"
        };
        
        println!(
            "• Node {} ↔ Node {}: {:.3} {}",
            node1, node2, fidelity, status
        );
    }
    
    let spooky_action = entangled_pairs;
    let classical_correlation = total_pairs - entangled_pairs;
    
    println!();
    println!("🔮 Spooky Action Detected: {} pairs", spooky_action);
    println!("⚠️  Classical Correlation: {} pairs", classical_correlation);
    
    let entanglement_percentage = if total_pairs > 0 {
        (entangled_pairs as f64 / total_pairs as f64) * 100.0
    } else {
        0.0
    };
    
    println!();
    println!(
        "🎉 Overall System Entanglement: {:.1}% ({}.{})",
        entanglement_percentage, entangled_pairs, total_pairs
    );
    
    if !quiet {
        println!();
        println!(
            "\"The universe is not only stranger than we imagine,"
        );
        println!(
            " it is stranger than we *can* imagine." - J.B.S. Haldane"
        );
    }
    
    println!();
    println!("⏱️  Simulation completed in {:.2?}", duration);
}

fn output_json(
    results: &HashMap<(usize, usize), f64>,
    num_nodes: usize,
    num_measurements: usize,
    fidelity_threshold: f64,
    duration: std::time::Duration,
) {
    let mut entangled_pairs = 0;
    let mut total_pairs = 0;
    
    let mut fidelity_details = Vec::new();
    
    for ((node1, node2), fidelity) in results.iter() {
        total_pairs += 1;
        if *fidelity >= fidelity_threshold {
            entangled_pairs += 1;
        }
        
        fidelity_details.push(serde_json::json!({
            "node1": node1,
            "node2": node2,
            "fidelity": fidelity,
            "entangled": fidelity >= &fidelity_threshold
        }));
    }
    
    let entanglement_percentage = if total_pairs > 0 {
        (entangled_pairs as f64 / total_pairs as f64) * 100.0
    } else {
        0.0
    };
    
    let output = serde_json::json!({
        "simulation": {
            "nodes": num_nodes,
            "measurements": num_measurements,
            "fidelity_threshold": fidelity_threshold,
            "duration_ms": duration.as_millis()
        },
        "results": {
            "total_pairs": total_pairs,
            "entangled_pairs": entangled_pairs,
            "classical_correlation_pairs": total_pairs - entangled_pairs,
            "entanglement_percentage": entanglement_percentage,
            "fidelity_details": fidelity_details
        }
    });
    
    println!("{}", serde_json::to_string_pretty(&output).unwrap());
}
