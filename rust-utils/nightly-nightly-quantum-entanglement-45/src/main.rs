use clap::{Arg, Command};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::time::{Duration, Instant};
use tokio::time::sleep;
use rand::Rng;
use colored::*;

mod quantum_simulator;
mod network_simulator;
mod report_generator;

use quantum_simulator::QuantumSimulator;
use network_simulator::NetworkSimulator;
use report_generator::{ReportFormat, ReportGenerator};

#[derive(Debug, Serialize, Deserialize)]
struct QuantumConfig {
    nodes: usize,
    entanglement_strength: f64,
    decoherence_rate: f64,
    duration: String,
    output_format: Option<String>,
    network_mode: bool,
    verbose: bool,
}

#[derive(Debug, Serialize, Deserialize)]
struct QuantumReport {
    experiment_parameters: ExperimentParameters,
    quantum_state_analysis: QuantumStateAnalysis,
    network_metrics: NetworkMetrics,
    result: QuantumResult,
    timestamp: String,
}

#[derive(Debug, Serialize, Deserialize)]
struct ExperimentParameters {
    nodes: usize,
    duration: String,
    entanglement_strength: f64,
    decoherence_rate: f64,
}

#[derive(Debug, Serialize, Deserialize)]
struct QuantumStateAnalysis {
    coherence_level: f64,
    entanglement_fidelity: f64,
    bell_inequality_violation: bool,
    quantum_correlation_score: f64,
}

#[derive(Debug, Serialize, Deserialize)]
struct NetworkMetrics {
    average_latency_ms: f64,
    packet_loss_percent: f64,
    synchronization_error_ns: f64,
    network_reliability: f64,
}

#[derive(Debug, Serialize, Deserialize)]
struct QuantumResult {
    success: bool,
    message: String,
    spooky_action_confirmed: bool,
    confidence_level: f64,
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let matches = Command::new("Nightly Quantum Entanglement Checker")
        .version(env!("CARGO_PKG_VERSION"))
        .author("ApocalypsAI Collective")
        .about("A whimsical CLI tool that simulates quantum entanglement verification for distributed systems")
        .arg(
            Arg::new("nodes")
                .short('n')
                .long("nodes")
                .value_name("COUNT")
                .help("Number of quantum nodes to simulate")
                .default_value("4")
        )
        .arg(
            Arg::new("duration")
                .short('d')
                .long("duration")
                .value_name("TIME")
                .help("Duration of the quantum experiment (e.g., 10s, 1m, 5m30s)")
                .default_value("30s")
        )
        .arg(
            Arg::new("entanglement-strength")
                .long("entanglement-strength")
                .value_name("STRENGTH")
                .help("Initial entanglement strength (0.0 to 1.0)")
                .default_value("0.75")
        )
        .arg(
            Arg::new("decoherence-rate")
                .long("decoherence-rate")
                .value_name("RATE")
                .help("Rate of quantum decoherence (0.0 to 1.0)")
                .default_value("0.03")
        )
        .arg(
            Arg::new("output-format")
                .short('f')
                .long("output-format")
                .value_name("FORMAT")
                .help("Output format: text, json, or yaml")
                .default_value("text")
        )
        .arg(
            Arg::new("network")
                .short('w')
                .long("network")
                .help("Enable network simulation mode")
                .action(clap::ArgAction::SetTrue)
        )
        .arg(
            Arg::new("verbose")
                .short('v')
                .long("verbose")
                .help("Enable verbose output")
                .action(clap::ArgAction::SetTrue)
        )
        .arg(
            Arg::new("config")
                .short('c')
                .long("config")
                .value_name("FILE")
                .help("Configuration file (TOML format)")
        )
        .get_matches();

    let config = load_config(&matches)?;
    
    if config.verbose {
        println!("{}", "🔬 Initializing quantum entanglement verification...".bright_cyan());
    }

    // Initialize simulators
    let mut quantum_simulator = QuantumSimulator::new(
        config.nodes,
        config.entanglement_strength,
        config.decoherence_rate,
    );
    
    let mut network_simulator = NetworkSimulator::new(config.nodes);
    
    let start_time = Instant::now();
    let duration = parse_duration(&config.duration)?;
    
    if config.verbose {
        println!("{} {}", "⏱️  Experiment duration:".bright_yellow(), config.duration);
    }

    // Run quantum simulation
    let quantum_results = quantum_simulator.run_simulation(duration, config.verbose).await;
    
    // Run network simulation if enabled
    let network_results = if config.network_mode {
        if config.verbose {
            println!("{}", "📡 Running network simulation...".bright_blue());
        }
        Some(network_simulator.run_simulation(duration, config.verbose).await)
    } else {
        None
    };
    
    let elapsed = start_time.elapsed();
    
    if config.verbose {
        println!("{} {:.2?}", "⏱️  Total execution time:".bright_green(), elapsed);
    }

    // Generate report
    let report = QuantumReport {
        experiment_parameters: ExperimentParameters {
            nodes: config.nodes,
            duration: config.duration,
            entanglement_strength: config.entanglement_strength,
            decoherence_rate: config.decoherence_rate,
        },
        quantum_state_analysis: quantum_results,
        network_metrics: network_results.unwrap_or_default(),
        result: QuantumResult {
            success: quantum_results.entanglement_fidelity > 0.5,
            message: if quantum_results.entanglement_fidelity > 0.5 {
                "QUANTUM ENTANGLEMENT SUCCESSFUL".to_string()
            } else {
                "QUANTUM ENTANGLEMENT FAILED".to_string()
            },
            spooky_action_confirmed: quantum_results.bell_inequality_violation,
            confidence_level: quantum_results.entanglement_fidelity,
        },
        timestamp: chrono::Utc::now().to_rfc3339(),
    };

    // Output report
    let format = ReportFormat::from_string(&config.output_format.unwrap_or_else(|| "text".to_string()));
    let generator = ReportGenerator::new(format);
    generator.generate_report(&report);

    Ok(())
}

fn load_config(matches: &clap::ArgMatches) -> Result<QuantumConfig, Box<dyn std::error::Error>> {
    // Check if config file is provided
    if let Some(config_file) = matches.get_one::<String>("config") {
        let content = std::fs::read_to_string(config_file)?;
        let mut config: QuantumConfig = toml::from_str(&content)?;
        
        // Override with CLI args if provided
        if matches.contains_id("nodes") {
            config.nodes = matches.get_one::<String>("nodes").unwrap().parse()?;
        }
        if matches.contains_id("duration") {
            config.duration = matches.get_one::<String>("duration").unwrap().to_string();
        }
        if matches.contains_id("entanglement-strength") {
            config.entanglement_strength = matches.get_one::<String>("entanglement-strength").unwrap().parse()?;
        }
        if matches.contains_id("decoherence-rate") {
            config.decoherence_rate = matches.get_one::<String>("decoherence-rate").unwrap().parse()?;
        }
        if matches.contains_id("output-format") {
            config.output_format = Some(matches.get_one::<String>("output-format").unwrap().to_string());
        }
        if matches.contains_id("network") {
            config.network_mode = *matches.get_one::<bool>("network").unwrap();
        }
        if matches.contains_id("verbose") {
            config.verbose = *matches.get_one::<bool>("verbose").unwrap();
        }
        
        return Ok(config);
    }

    // Build config from CLI args
    Ok(QuantumConfig {
        nodes: matches.get_one::<String>("nodes").unwrap().parse()?,
        duration: matches.get_one::<String>("duration").unwrap().to_string(),
        entanglement_strength: matches.get_one::<String>("entanglement-strength").unwrap().parse()?,
        decoherence_rate: matches.get_one::<String>("decoherence-rate").unwrap().parse()?,
        output_format: Some(matches.get_one::<String>("output-format").unwrap().to_string()),
        network_mode: *matches.get_one::<bool>("network").unwrap_or(&false),
        verbose: *matches.get_one::<bool>("verbose").unwrap_or(&false),
    })
}

fn parse_duration(duration_str: &str) -> Result<Duration, Box<dyn std::error::Error>> {
    let duration_str = duration_str.to_lowercase();
    
    if duration_str.ends_with('s') {
        let seconds = duration_str.trim_end_matches('s').parse::<u64>()?;
        Ok(Duration::from_secs(seconds))
    } else if duration_str.ends_with('m') {
        let minutes = duration_str.trim_end_matches('m').parse::<u64>()?;
        Ok(Duration::from_secs(minutes * 60))
    } else if duration_str.contains('m') && duration_str.contains('s') {
        // Parse format like "5m30s"
        let parts: Vec<&str> = duration_str.split(&['m', 's'][..]).collect();
        if parts.len() >= 2 {
            let minutes = parts[0].parse::<u64>()?;
            let seconds = parts[1].parse::<u64>()?;
            Ok(Duration::from_secs(minutes * 60 + seconds))
        } else {
            Err("Invalid duration format".into())
        }
    } else {
        Err("Invalid duration format. Use formats like: 30s, 1m, 5m30s".into())
    }
}

impl Default for NetworkMetrics {
    fn default() -> Self {
        NetworkMetrics {
            average_latency_ms: 0.0,
            packet_loss_percent: 0.0,
            synchronization_error_ns: 0.0,
            network_reliability: 1.0,
        }
    }
}
