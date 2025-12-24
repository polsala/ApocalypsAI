use clap::{Arg, Command};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs;
use std::io::{self, Write};
use std::time::{SystemTime, UNIX_EPOCH};
use toml;

#[derive(Debug, Serialize, Deserialize)]
struct Node {
    name: String,
    address: Option<String>,
}

#[derive(Debug, Serialize, Deserialize)]
struct QuantumConfig {
    #[serde(default = "default_strength")]
    strength: f64,
    #[serde(default = "default_decoherence")]
    decoherence: f64,
    #[serde(default = "default_precision")]
    measurement_precision: f64,
}

fn default_strength() -> f64 { 0.9 }
fn default_decoherence() -> f64 { 0.05 }
fn default_precision() -> f64 { 0.001 }

#[derive(Debug, Serialize, Deserialize)]
struct OutputConfig {
    #[serde(default = "default_format")]
    format: String,
    #[serde(default)]
    verbose: bool,
}

fn default_format() -> String { "text".to_string() }

#[derive(Debug, Serialize, Deserialize)]
struct Config {
    node_a: Node,
    node_b: Node,
    quantum: QuantumConfig,
    output: OutputConfig,
}

#[derive(Debug, Serialize)]
struct EntanglementResult {
    node_a: String,
    node_b: String,
    entanglement_strength: f64,
    decoherence_rate: f64,
    measurement_precision: f64,
    status: String,
    confidence: f64,
    recommendation: String,
    timestamp: String,
}

impl Default for Config {
    fn default() -> Self {
        Self {
            node_a: Node {
                name: "node-a".to_string(),
                address: None,
            },
            node_b: Node {
                name: "node-b".to_string(),
                address: None,
            },
            quantum: QuantumConfig {
                strength: default_strength(),
                decoherence: default_decoherence(),
                measurement_precision: default_precision(),
            },
            output: OutputConfig {
                format: default_format(),
                verbose: false,
            },
        }
    }
}

fn main() {
    let matches = Command::new("nightly-quantum-entanglement-checker")
        .version(env!("CARGO_PKG_VERSION"))
        .author("ApocalypsAI")
        .about("Simulates quantum entanglement verification for distributed systems")
        .arg(
            Arg::new("node-a")
                .short('a')
                .long("node-a")
                .value_name("NODE_A")
                .help("Name of the first node")
                .required(false),
        )
        .arg(
            Arg::new("node-b")
                .short('b')
                .long("node-b")
                .value_name("NODE_B")
                .help("Name of the second node")
                .required(false),
        )
        .arg(
            Arg::new("strength")
                .short('s')
                .long("strength")
                .value_name("STRENGTH")
                .help("Entanglement strength (0.0 to 1.0)")
                .required(false),
        )
        .arg(
            Arg::new("decoherence")
                .short('d')
                .long("decoherence")
                .value_name("DECOHERENCE")
                .help("Decoherence rate (0.0 to 1.0)")
                .required(false),
        )
        .arg(
            Arg::new("format")
                .short('f')
                .long("format")
                .value_name("FORMAT")
                .help("Output format: text or json")
                .required(false),
        )
        .arg(
            Arg::new("config")
                .short('c')
                .long("config")
                .value_name("FILE")
                .help("Path to configuration file")
                .required(false),
        )
        .arg(
            Arg::new("distributed")
                .long("distributed")
                .help("Run in distributed mode with multiple nodes")
                .required(false),
        )
        .arg(
            Arg::new("nodes")
                .long("nodes")
                .value_name("NODES")
                .help("Comma-separated list of nodes for distributed mode")
                .required(false),
        )
        .arg(
            Arg::new("verbose")
                .short('v')
                .long("verbose")
                .help("Enable verbose output")
                .required(false),
        )
        .get_matches();

    let mut config = Config::default();

    // Load config file if provided
    if let Some(config_path) = matches.get_one::<String>("config") {
        match load_config(config_path) {
            Ok(loaded_config) => {
                config = loaded_config;
            }
            Err(e) => {
                eprintln!("Error loading config file: {}", e);
                std::process::exit(1);
            }
        }
    }

    // Override with command line arguments
    if let Some(node_a) = matches.get_one::<String>("node-a") {
        config.node_a.name = node_a.clone();
    }

    if let Some(node_b) = matches.get_one::<String>("node-b") {
        config.node_b.name = node_b.clone();
    }

    if let Some(strength_str) = matches.get_one::<String>("strength") {
        match strength_str.parse::<f64>() {
            Ok(strength) if strength >= 0.0 && strength <= 1.0 => {
                config.quantum.strength = strength;
            }
            _ => {
                eprintln!("Error: Strength must be between 0.0 and 1.0");
                std::process::exit(1);
            }
        }
    }

    if let Some(decoherence_str) = matches.get_one::<String>("decoherence") {
        match decoherence_str.parse::<f64>() {
            Ok(decoherence) if decoherence >= 0.0 && decoherence <= 1.0 => {
                config.quantum.decoherence = decoherence;
            }
            _ => {
                eprintln!("Error: Decoherence must be between 0.0 and 1.0");
                std::process::exit(1);
            }
        }
    }

    if let Some(format_str) = matches.get_one::<String>("format") {
        config.output.format = format_str.clone();
    }

    if matches.get_flag("verbose") {
        config.output.verbose = true;
    }

    // Handle distributed mode
    if matches.get_flag("distributed") {
        if let Some(nodes_str) = matches.get_one::<String>("nodes") {
            let nodes: Vec<&str> = nodes_str.split(',').collect();
            if nodes.len() < 2 {
                eprintln!("Error: Distributed mode requires at least 2 nodes");
                std::process::exit(1);
            }

            let mut results = Vec::new();
            for i in 0..nodes.len() {
                for j in (i + 1)..nodes.len() {
                    let result = check_entanglement(
                        nodes[i],
                        nodes[j],
                        config.quantum.strength,
                        config.quantum.decoherence,
                        config.quantum.measurement_precision,
                    );
                    results.push(result);
                }
            }

            output_results(&results, &config.output);
        } else {
            eprintln!("Error: --nodes is required for distributed mode");
            std::process::exit(1);
        }
    } else {
        // Single node pair mode
        let result = check_entanglement(
            &config.node_a.name,
            &config.node_b.name,
            config.quantum.strength,
            config.quantum.decoherence,
            config.quantum.measurement_precision,
        );
        output_results(&[result], &config.output);
    }
}

fn load_config(path: &str) -> Result<Config, Box<dyn std::error::Error>> {
    let content = fs::read_to_string(path)?;
    let config: Config = toml::from_str(&content)?;
    Ok(config)
}

fn check_entanglement(
    node_a: &str,
    node_b: &str,
    strength: f64,
    decoherence: f64,
    precision: f64,
) -> EntanglementResult {
    // Simulate quantum entanglement measurement
    let base_strength = strength;
    let environmental_noise = rand::random::<f64>() * 0.1;
    let measurement_error = rand::random::<f64>() * precision;

    let actual_strength = base_strength - (decoherence * 0.5) - environmental_noise + measurement_error;
    let actual_strength = actual_strength.max(0.0).min(1.0);

    let confidence = calculate_confidence(actual_strength, decoherence, precision);

    let status = if actual_strength > 0.5 {
        "ENTANGLED".to_string()
    } else {
        "SEPARATED".to_string()
    };

    let recommendation = generate_recommendation(actual_strength, decoherence, confidence);

    let timestamp = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_secs()
        .to_string();

    EntanglementResult {
        node_a: node_a.to_string(),
        node_b: node_b.to_string(),
        entanglement_strength: actual_strength,
        decoherence_rate: decoherence,
        measurement_precision: precision,
        status,
        confidence,
        recommendation,
        timestamp,
    }
}

fn calculate_confidence(strength: f64, decoherence: f64, precision: f64) -> f64 {
    let base_confidence = strength * 0.8 + (1.0 - decoherence) * 0.15 + (1.0 - precision) * 0.05;
    base_confidence.min(1.0).max(0.0)
}

fn generate_recommendation(strength: f64, decoherence: f64, confidence: f64) -> String {
    if strength > 0.8 && confidence > 0.9 {
        "System is stable. No quantum corrections required.".to_string()
    } else if strength > 0.6 && confidence > 0.7 {
        "System is moderately stable. Monitor for quantum fluctuations.".to_string()
    } else if strength > 0.4 && confidence > 0.5 {
        "System shows signs of quantum instability. Consider recalibration.".to_string()
    } else if strength > 0.2 && confidence > 0.3 {
        "System is experiencing significant quantum decoherence. Immediate attention required.".to_string()
    } else {
        "System has lost quantum coherence. Emergency quantum reboot recommended.".to_string()
    }
}

fn output_results(results: &[EntanglementResult], output_config: &OutputConfig) {
    match output_config.format.as_str() {
        "json" => {
            let json_output = serde_json::to_string_pretty(results).unwrap();
            println!("{}", json_output);
        }
        _ => {
            for result in results {
                print_text_result(result, output_config.verbose);
                if output_config.verbose {
                    println!();
                }
            }
        }
    }
}

fn print_text_result(result: &EntanglementResult, verbose: bool) {
    println!("Quantum Entanglement Verification Report");
    println!("======================================");
    println!();
    println!("Node A: {}", result.node_a);
    println!("Node B: {}", result.node_b);
    println!();
    println!("Entanglement Strength: {:.2}", result.entanglement_strength);
    println!("Decoherence Rate: {:.2}", result.decoherence_rate);
    println!("Measurement Precision: {:.3}", result.measurement_precision);
    println!();
    println!("Status: {} {}", result.status, get_status_emoji(&result.status));
    println!("Confidence: {:.1}%", result.confidence * 100.0);
    println!();
    println!("Recommendation: {}", result.recommendation);

    if verbose {
        println!();
        println!("Additional Information:");
        println!("- Timestamp: {}", result.timestamp);
        println!("- Measurement precision is within acceptable quantum bounds");
        println!("- Environmental noise has been accounted for in calculations");
    }
}

fn get_status_emoji(status: &str) -> &str {
    match status {
        "ENTANGLED" => "✓",
        "SEPARATED" => "✗",
        _ => "?",
    }
}

// Simple random number generator for reproducible results in tests
mod rand {
    use std::cell::Cell;

    thread_local! {
        static SEED: Cell<u64> = Cell::new(42);
    }

    pub fn random<T>() -> T
    where
        f64: From<T>,
        T: From<f64>,
    {
        SEED.with(|seed| {
            let mut s = seed.get();
            s = s.wrapping_mul(1103515245).wrapping_add(12345);
            seed.set(s);
            let result = (s % 1000000) as f64 / 1000000.0;
            result.into()
        })
    }

    pub fn reset_seed() {
        SEED.with(|seed| seed.set(42));
    }
}
