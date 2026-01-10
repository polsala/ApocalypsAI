use clap::{Arg, Command};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::time::Instant;
use std::fs;
use std::path::Path;

mod quantum_simulator;
mod report_generator;
mod config;

use quantum_simulator::QuantumSimulator;
use report_generator::ReportGenerator;
use config::Config;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let matches = Command::new("Quantum Entanglement Checker")
        .version(env!("CARGO_PKG_VERSION"))
        .author("ApocalypsAI")
        .about("A whimsical CLI tool that simulates quantum entanglement verification for distributed systems")
        .arg(
            Arg::new("nodes")
                .short('n')
                .long("nodes")
                .value_name("NODES")
                .help("Comma-separated list of nodes to check entanglement between")
                .required_unless_present("config")
        )
        .arg(
            Arg::new("strength")
                .short('s')
                .long("strength")
                .value_name("STRENGTH")
                .help("Entanglement strength (0.0 to 1.0)")
                .default_value("0.75")
        )
        .arg(
            Arg::new("coherence-threshold")
                .long("coherence-threshold")
                .value_name("THRESHOLD")
                .help("Quantum coherence threshold for success (0.0 to 1.0)")
                .default_value("0.8")
        )
        .arg(
            Arg::new("distributed")
                .long("distributed")
                .help("Enable distributed mode with network simulation")
                .action(clap::ArgAction::SetTrue)
        )
        .arg(
            Arg::new("latency")
                .long("latency")
                .value_name("LATENCY")
                .help("Network latency simulation (e.g., 50ms, 100ms)")
                .default_value("0ms")
        )
        .arg(
            Arg::new("report")
                .long("report")
                .value_name("TYPE")
                .help("Report type: simple or detailed")
                .default_value("simple")
        )
        .arg(
            Arg::new("config")
                .short('c')
                .long("config")
                .value_name("FILE")
                .help("Configuration file path")
        )
        .arg(
            Arg::new("verbose")
                .short('v')
                .long("verbose")
                .help("Enable verbose output")
                .action(clap::ArgAction::SetTrue)
        )
        .get_matches();

    // Load configuration
    let config = if let Some(config_path) = matches.get_one::<String>("config") {
        Config::from_file(config_path)?
    } else {
        Config::from_args(&matches)?
    };

    if config.verbose {
        println!("🔬 Initializing Quantum Entanglement Checker...");
        println!("📍 Nodes: {}", config.nodes.join(" ↔ "));
        println!("⚡ Entanglement Strength: {}", config.quantum.entanglement_strength);
        println!("🔮 Coherence Threshold: {}", config.quantum.coherence_threshold);
    }

    // Initialize quantum simulator
    let mut simulator = QuantumSimulator::new(config.quantum.entanglement_strength);
    
    if config.distributed {
        simulator.enable_distributed_mode();
        if config.verbose {
            println!("🌐 Distributed mode enabled with latency simulation: {}", config.quantum.latency_simulation);
        }
    }

    // Run entanglement verification
    let start_time = Instant::now();
    let results = simulator.verify_entanglement(&config.nodes);
    let duration = start_time.elapsed();

    // Generate report
    let mut generator = ReportGenerator::new();
    let report = generator.generate_report(&config.nodes, &results, duration, &config);

    println!("{}", report);

    // Exit with appropriate code
    if results.entanglement_confirmed {
        Ok(())
    } else {
        std::process::exit(1);
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::io::Write;
    use tempfile::NamedTempFile;

    #[test]
    fn test_config_from_file() {
        let mut temp_file = NamedTempFile::new().unwrap();
        writeln!(temp_file, r#"
[nodes]
primary = "node1"
secondary = "node2"

[quantum]
entanglement_strength = 0.85
coherence_threshold = 0.9
latency_simulation = "100ms"
"#).unwrap();
        
        let config = Config::from_file(temp_file.path().to_str().unwrap()).unwrap();
        assert_eq!(config.nodes, vec!["node1", "node2"]);
        assert_eq!(config.quantum.entanglement_strength, 0.85);
        assert_eq!(config.quantum.coherence_threshold, 0.9);
    }

    #[test]
    fn test_config_from_args() {
        let matches = Command::new("test")
            .arg(Arg::new("nodes").required(true))
            .get_matches_from(vec!["test", "--nodes", "node1,node2"]);
        
        let config = Config::from_args(&matches).unwrap();
        assert_eq!(config.nodes, vec!["node1", "node2"]);
    }
}
