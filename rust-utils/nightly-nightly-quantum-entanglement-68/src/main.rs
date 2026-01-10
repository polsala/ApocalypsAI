use clap::{Arg, Command};
use std::collections::HashMap;
use std::time::{Duration, Instant};
use rand::Rng;
use serde::{Deserialize, Serialize};

mod quantum_simulator;
mod entanglement_checker;
mod metrics;

use quantum_simulator::QuantumSimulator;
use entanglement_checker::EntanglementChecker;
use metrics::QuantumMetrics;

#[derive(Debug, Clone)]
struct AppConfig {
    node_a: Option<String>,
    node_b: Option<String>,
    nodes: Vec<String>,
    state_size: usize,
    duration: u64,
    node_count: usize,
    verbose: bool,
}

fn main() {
    let matches = Command::new("Nightly Quantum Entanglement Checker")
        .version(env!("CARGO_PKG_VERSION"))
        .author("ApocalypsAI")
        .about("Simulates quantum entanglement verification for distributed systems")
        .subcommand(
            Command::new("check")
                .about("Verify entanglement between two specific nodes")
                .arg(Arg::new("node-a")
                    .short('a')
                    .long("node-a")
                    .value_name("NODE")
                    .help("First node for entanglement check")
                    .required(true))
                .arg(Arg::new("node-b")
                    .short('b')
                    .long("node-b")
                    .value_name("NODE")
                    .help("Second node for entanglement check")
                    .required(true))
                .arg(Arg::new("state-size")
                    .short('s')
                    .long("state-size")
                    .value_name("SIZE")
                    .help("Size of quantum states")
                    .default_value("512"))
                .arg(Arg::new("verbose")
                    .short('v')
                    .long("verbose")
                    .help("Enable verbose quantum state output"))
        )
        .subcommand(
            Command::new("metrics")
                .about("Generate quantum metrics across multiple nodes")
                .arg(Arg::new("node-count")
                    .short('c')
                    .long("node-count")
                    .value_name("COUNT")
                    .help("Number of nodes for metrics generation")
                    .default_value("5"))
                .arg(Arg::new("duration")
                    .short('d')
                    .long("duration")
                    .value_name("SECONDS")
                    .help("Simulation duration in seconds")
                    .default_value("10"))
                .arg(Arg::new("state-size")
                    .short('s')
                    .long("state-size")
                    .value_name("SIZE")
                    .help("Size of quantum states")
                    .default_value("512"))
        )
        .subcommand(
            Command::new("verify")
                .about("Validate entanglement across a cluster of nodes")
                .arg(Arg::new("nodes")
                    .short('n')
                    .long("nodes")
                    .value_name("NODES")
                    .help("Comma-separated list of nodes for cluster verification")
                    .required(true))
                .arg(Arg::new("state-size")
                    .short('s')
                    .long("state-size")
                    .value_name("SIZE")
                    .help("Size of quantum states")
                    .default_value("512"))
        )
        .subcommand(
            Command::new("simulate")
                .about("Run a full quantum simulation with configurable parameters")
                .arg(Arg::new("node-count")
                    .short('c')
                    .long("node-count")
                    .value_name("COUNT")
                    .help("Number of nodes in simulation")
                    .default_value("5"))
                .arg(Arg::new("duration")
                    .short('d')
                    .long("duration")
                    .value_name("SECONDS")
                    .help("Simulation duration in seconds")
                    .default_value("10"))
                .arg(Arg::new("state-size")
                    .short('s')
                    .long("state-size")
                    .value_name("SIZE")
                    .help("Size of quantum states")
                    .default_value("512"))
                .arg(Arg::new("verbose")
                    .short('v')
                    .long("verbose")
                    .help("Enable verbose quantum state output"))
        )
        .get_matches();

    match matches.subcommand() {
        Some(("check", sub_matches)) => {
            let config = AppConfig {
                node_a: Some(sub_matches.get_one::<String>("node-a").unwrap().clone()),
                node_b: Some(sub_matches.get_one::<String>("node-b").unwrap().clone()),
                nodes: vec![],
                state_size: sub_matches.get_one::<String>("state-size").unwrap().parse().unwrap_or(512),
                duration: 0,
                node_count: 0,
                verbose: sub_matches.get_flag("verbose"),
            };
            run_check(config);
        }
        Some(("metrics", sub_matches)) => {
            let config = AppConfig {
                node_a: None,
                node_b: None,
                nodes: vec![],
                state_size: sub_matches.get_one::<String>("state-size").unwrap().parse().unwrap_or(512),
                duration: sub_matches.get_one::<String>("duration").unwrap().parse().unwrap_or(10),
                node_count: sub_matches.get_one::<String>("node-count").unwrap().parse().unwrap_or(5),
                verbose: false,
            };
            run_metrics(config);
        }
        Some(("verify", sub_matches)) => {
            let nodes_str = sub_matches.get_one::<String>("nodes").unwrap();
            let nodes: Vec<String> = nodes_str.split(',').map(|s| s.trim().to_string()).collect();
            let config = AppConfig {
                node_a: None,
                node_b: None,
                nodes,
                state_size: sub_matches.get_one::<String>("state-size").unwrap().parse().unwrap_or(512),
                duration: 0,
                node_count: 0,
                verbose: false,
            };
            run_verify(config);
        }
        Some(("simulate", sub_matches)) => {
            let config = AppConfig {
                node_a: None,
                node_b: None,
                nodes: vec![],
                state_size: sub_matches.get_one::<String>("state-size").unwrap().parse().unwrap_or(512),
                duration: sub_matches.get_one::<String>("duration").unwrap().parse().unwrap_or(10),
                node_count: sub_matches.get_one::<String>("node-count").unwrap().parse().unwrap_or(5),
                verbose: sub_matches.get_flag("verbose"),
            };
            run_simulation(config);
        }
        _ => {
            println!("Use --help for usage information");
        }
    }
}

fn run_check(config: AppConfig) {
    println!("🔬 Initializing Quantum Entanglement Check...");
    println!("📡 Node A: {}", config.node_a.as_ref().unwrap());
    println!("📡 Node B: {}", config.node_b.as_ref().unwrap());
    println!("⚛️  State Size: {} qubits", config.state_size);

    let mut simulator = QuantumSimulator::new();
    let mut checker = EntanglementChecker::new();

    // Generate quantum states for both nodes
    let state_a = simulator.generate_quantum_state(config.state_size);
    let state_b = simulator.generate_quantum_state(config.state_size);

    if config.verbose {
        println!("\n📊 Quantum State A: {}", state_a.to_string());
        println!("📊 Quantum State B: {}", state_b.to_string());
    }

    // Check entanglement
    let result = checker.check_entanglement(&state_a, &state_b);

    println!("\n🔍 Entanglement Analysis:");
    println!("   Entanglement Score: {:.2}%", result.entanglement_score * 100.0);
    println!("   Bell State Fidelity: {:.2}%", result.bell_state_fidelity * 100.0);
    println!("   Decoherence Level: {:.2}%", result.decoherence_level * 100.0);

    if result.is_entangled {
        println!("✅ Nodes are quantumly entangled!");
    } else {
        println!("❌ No entanglement detected");
    }
}

fn run_metrics(config: AppConfig) {
    println!("📈 Generating Quantum Metrics...");
    println!("📡 Node Count: {}", config.node_count);
    println!("⏱️  Duration: {} seconds", config.duration);
    println!("⚛️  State Size: {} qubits", config.state_size);

    let mut metrics = QuantumMetrics::new();
    let mut simulator = QuantumSimulator::new();

    let start_time = Instant::now();
    let mut iteration = 0;

    while start_time.elapsed() < Duration::from_secs(config.duration) {
        iteration += 1;
        
        // Simulate quantum states for all nodes
        let mut states = Vec::new();
        for i in 0..config.node_count {
            let state = simulator.generate_quantum_state(config.state_size);
            states.push((format!("node_{}", i), state));
        }

        // Calculate metrics
        let avg_entanglement = calculate_average_entanglement(&states);
        let coherence_score = calculate_coherence_score(&states);
        
        metrics.record_iteration(iteration, avg_entanglement, coherence_score);

        if iteration % 10 == 0 {
            println!("   Iteration {}: Avg Entanglement = {:.2}%, Coherence = {:.2}%", 
                iteration, avg_entanglement * 100.0, coherence_score * 100.0);
        }
    }

    let final_metrics = metrics.get_final_metrics();
    println!("\n📊 Final Quantum Metrics:");
    println!("   Total Iterations: {}", final_metrics.iterations);
    println!("   Average Entanglement: {:.2}%", final_metrics.avg_entanglement * 100.0);
    println!("   Average Coherence: {:.2}%", final_metrics.avg_coherence * 100.0);
    println!("   Peak Entanglement: {:.2}%", final_metrics.peak_entanglement * 100.0);
    println!("   Peak Coherence: {:.2}%", final_metrics.peak_coherence * 100.0);
}

fn run_verify(config: AppConfig) {
    println!("🔬 Verifying Quantum Entanglement Across Cluster...");
    println!("📡 Nodes: {}", config.nodes.join(", "));
    println!("⚛️  State Size: {} qubits", config.state_size);

    let mut simulator = QuantumSimulator::new();
    let mut checker = EntanglementChecker::new();

    // Generate quantum states for all nodes
    let mut states = Vec::new();
    for node in &config.nodes {
        let state = simulator.generate_quantum_state(config.state_size);
        states.push((node.clone(), state));
    }

    // Check pairwise entanglement
    let mut entanglement_matrix = HashMap::new();
    let mut total_entanglement = 0.0;
    let mut entangled_pairs = 0;

    for i in 0..states.len() {
        for j in (i + 1)..states.len() {
            let (node_a, state_a) = &states[i];
            let (node_b, state_b) = &states[j];
            
            let result = checker.check_entanglement(state_a, state_b);
            entanglement_matrix.insert(format!("{}-{}", node_a, node_b), result.clone());
            
            total_entanglement += result.entanglement_score;
            if result.is_entangled {
                entangled_pairs += 1;
            }
        }
    }

    let total_pairs = (states.len() * (states.len() - 1)) / 2;
    let cluster_entanglement_score = total_entanglement / total_pairs as f64;

    println!("\n📊 Cluster Entanglement Report:");
    println!("   Total Node Pairs: {}", total_pairs);
    println!("   Entangled Pairs: {}", entangled_pairs);
    println!("   Cluster Entanglement Score: {:.2}%", cluster_entanglement_score * 100.0);

    if cluster_entanglement_score > 0.5 {
        println!("✅ Cluster shows strong quantum entanglement!");
    } else {
        println!("⚠️  Cluster entanglement is below optimal threshold");
    }
}

fn run_simulation(config: AppConfig) {
    println!("🔬 Running Full Quantum Simulation...");
    println!("📡 Node Count: {}", config.node_count);
    println!("⏱️  Duration: {} seconds", config.duration);
    println!("⚛️  State Size: {} qubits", config.state_size);

    let mut simulator = QuantumSimulator::new();
    let mut checker = EntanglementChecker::new();
    let mut metrics = QuantumMetrics::new();

    let start_time = Instant::now();
    let mut iteration = 0;

    while start_time.elapsed() < Duration::from_secs(config.duration) {
        iteration += 1;
        
        // Generate quantum states
        let mut states = Vec::new();
        for i in 0..config.node_count {
            let state = simulator.generate_quantum_state(config.state_size);
            states.push((format!("node_{}", i), state));
        }

        // Calculate entanglement metrics
        let avg_entanglement = calculate_average_entanglement(&states);
        let coherence_score = calculate_coherence_score(&states);
        
        metrics.record_iteration(iteration, avg_entanglement, coherence_score);

        // Simulate quantum operations
        for (node, state) in &mut states {
            simulator.apply_quantum_gate(state);
            simulator.introduce_decoherence(state, 0.01);
        }

        if config.verbose && iteration % 5 == 0 {
            println!("   Iteration {}: Avg Entanglement = {:.2}%, Coherence = {:.2}%", 
                iteration, avg_entanglement * 100.0, coherence_score * 100.0);
        }
    }

    let final_metrics = metrics.get_final_metrics();
    println!("\n📊 Simulation Results:");
    println!("   Total Iterations: {}", final_metrics.iterations);
    println!("   Final Average Entanglement: {:.2}%", final_metrics.avg_entanglement * 100.0);
    println!("   Final Average Coherence: {:.2}%", final_metrics.avg_coherence * 100.0);
    println!("   Quantum Stability: {}", if final_metrics.avg_coherence > 0.7 { "STABLE" } else { "UNSTABLE" });
}

fn calculate_average_entanglement(states: &[(String, Vec<f64>)]) -> f64 {
    let mut total_score = 0.0;
    let mut pairs = 0;
    
    for i in 0..states.len() {
        for j in (i + 1)..states.len() {
            let (_, state_a) = &states[i];
            let (_, state_b) = &states[j];
            
            // Simple entanglement calculation based on state correlation
            let correlation = state_a.iter()
                .zip(state_b.iter())
                .map(|(a, b)| a * b)
                .sum::<f64>() / state_a.len() as f64;
            
            total_score += correlation.abs();
            pairs += 1;
        }
    }
    
    if pairs > 0 { total_score / pairs as f64 } else { 0.0 }
}

fn calculate_coherence_score(states: &[(String, Vec<f64>)]) -> f64 {
    // Calculate average coherence based on state uniformity
    let mut total_coherence = 0.0;
    
    for (_, state) in states {
        let mean = state.iter().sum::<f64>() / state.len() as f64;
        let variance = state.iter().map(|x| (x - mean).powi(2)).sum::<f64>() / state.len() as f64;
        let coherence = 1.0 / (1.0 + variance);
        total_coherence += coherence;
    }
    
    total_coherence / states.len() as f64
}
