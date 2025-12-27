use clap::{Arg, Command};
use rand::Rng;
use serde::{Deserialize, Serialize};
use std::time::Instant;

#[derive(Debug, Serialize, Deserialize)]
struct QuantumNode {
    id: String,
    quantum_state: f64,
    position: (f64, f64, f64),
}

#[derive(Debug, Serialize, Deserialize)]
struct EntanglementResult {
    node_a: String,
    node_b: String,
    correlation: f64,
    entangled: bool,
}

#[derive(Debug, Serialize, Deserialize)]
struct SimulationReport {
    timestamp: String,
    nodes_count: usize,
    distance_km: f64,
    entanglement_strength: f64,
    iterations: usize,
    results: Vec<EntanglementResult>,
    average_correlation: f64,
    system_coherence: String,
}

fn main() {
    let matches = Command::new("Nightly Quantum Entanglement Checker")
        .version(env!("CARGO_PKG_VERSION"))
        .author("ApocalypsAI")
        .about("Simulates quantum entanglement verification for distributed systems")
        .arg(
            Arg::new("nodes")
                .short('n')
                .long("nodes")
                .value_name("COUNT")
                .help("Number of quantum nodes to simulate")
                .default_value("4")
        )
        .arg(
            Arg::new("distance")
                .short('d')
                .long("distance")
                .value_name("KM")
                .help("Distance between nodes in kilometers")
                .default_value("1000")
        )
        .arg(
            Arg::new("entanglement-strength")
                .short('s')
                .long("entanglement-strength")
                .value_name("STRENGTH")
                .help("Quantum entanglement strength (0.0-1.0)")
                .default_value("0.8")
        )
        .arg(
            Arg::new("iterations")
                .short('i')
                .long("iterations")
                .value_name("COUNT")
                .help("Number of simulation iterations")
                .default_value("100")
        )
        .arg(
            Arg::new("output-format")
                .short('o')
                .long("output-format")
                .value_name("FORMAT")
                .help("Output format (text, json, yaml)")
                .default_value("text")
        )
        .get_matches();

    let nodes_count: usize = matches
        .get_one::<String>("nodes")
        .unwrap()
        .parse()
        .expect("Nodes must be a valid number");

    let distance_km: f64 = matches
        .get_one::<String>("distance")
        .unwrap()
        .parse()
        .expect("Distance must be a valid number");

    let entanglement_strength: f64 = matches
        .get_one::<String>("entanglement-strength")
        .unwrap()
        .parse()
        .expect("Entanglement strength must be a valid number");

    let iterations: usize = matches
        .get_one::<String>("iterations")
        .unwrap()
        .parse()
        .expect("Iterations must be a valid number");

    let output_format = matches
        .get_one::<String>("output-format")
        .unwrap()
        .as_str();

    println!("🔬 Quantum Entanglement Verification Protocol");
    println!("==========================================");
    println!();

    let start_time = Instant::now();

    // Generate quantum nodes
    let nodes = generate_quantum_nodes(nodes_count, distance_km);
    
    // Run entanglement simulation
    let results = simulate_entanglement(&nodes, entanglement_strength, iterations);
    
    // Calculate statistics
    let average_correlation = calculate_average_correlation(&results);
    let system_coherence = determine_system_coherence(average_correlation);
    
    let report = SimulationReport {
        timestamp: chrono::Utc::now().to_rfc3339(),
        nodes_count,
        distance_km,
        entanglement_strength,
        iterations,
        results: results.clone(),
        average_correlation,
        system_coherence: system_coherence.clone(),
    };

    // Output results
    match output_format {
        "json" => println!("{}", serde_json::to_string_pretty(&report).unwrap()),
        "yaml" => println!("{}", serde_yaml::to_string(&report).unwrap()),
        _ => display_text_output(&results, average_correlation, &system_coherence),
    }

    let duration = start_time.elapsed();
    println!("\n⏱️  Simulation completed in {:.2?}", duration);
}

fn generate_quantum_nodes(count: usize, distance_km: f64) -> Vec<QuantumNode> {
    let mut rng = rand::thread_rng();
    let mut nodes = Vec::new();

    for i in 0..count {
        let node = QuantumNode {
            id: format!("Node {}", (b'A' + i as u8) as char),
            quantum_state: rng.gen_range(0.0..1.0),
            position: (
                rng.gen_range(0.0..distance_km),
                rng.gen_range(0.0..distance_km),
                rng.gen_range(0.0..distance_km),
            ),
        };
        nodes.push(node);
    }

    nodes
}

fn simulate_entanglement(
    nodes: &[QuantumNode],
    base_strength: f64,
    iterations: usize,
) -> Vec<EntanglementResult> {
    let mut results = Vec::new();
    let mut rng = rand::thread_rng();

    for i in 0..nodes.len() {
        for j in (i + 1)..nodes.len() {
            let distance = calculate_distance(
                nodes[i].position,
                nodes[j].position,
            );
            
            let mut total_correlation = 0.0;
            
            for _ in 0..iterations {
                let quantum_fluctuation = rng.gen_range(-0.1..0.1);
                let distance_factor = 1.0 / (1.0 + distance / 1000.0);
                
                let correlation = base_strength * distance_factor + quantum_fluctuation;
                let clamped_correlation = correlation.max(0.0).min(1.0);
                
                total_correlation += clamped_correlation;
            }
            
            let average_correlation = total_correlation / iterations as f64;
            let entangled = average_correlation > 0.5;
            
            results.push(EntanglementResult {
                node_a: nodes[i].id.clone(),
                node_b: nodes[j].id.clone(),
                correlation: average_correlation,
                entangled,
            });
        }
    }

    results
}

fn calculate_distance(pos1: (f64, f64, f64), pos2: (f64, f64, f64)) -> f64 {
    ((pos2.0 - pos1.0).powi(2) + (pos2.1 - pos1.1).powi(2) + (pos2.2 - pos1.2).powi(2)).sqrt()
}

fn calculate_average_correlation(results: &[EntanglementResult]) -> f64 {
    if results.is_empty() {
        0.0
    } else {
        let total: f64 = results.iter().map(|r| r.correlation).sum();
        total / results.len() as f64
    }
}

fn determine_system_coherence(average_correlation: f64) -> String {
    if average_correlation > 0.8 {
        "STABLE".to_string()
    } else if average_correlation > 0.6 {
        "CAUTION".to_string()
    } else {
        "UNSTABLE".to_string()
    }
}

fn display_text_output(
    results: &[EntanglementResult],
    average_correlation: f64,
    system_coherence: &str,
) {
    println!("🎉 Quantum entanglement verification successful!");
    println!("📊 Average correlation: {:.3}", average_correlation);
    println!("🔒 System coherence: {}", system_coherence);
    
    if system_coherence == "STABLE" {
        println!("🚀 Ready for quantum computing operations!");
    } else if system_coherence == "CAUTION" {
        println!("⚠️  Monitor system for quantum decoherence");
    } else {
        println!("🚨 System requires quantum recalibration");
    }
}
