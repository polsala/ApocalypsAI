use clap::{Parser, ValueEnum};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::time::{Duration, Instant};
use tokio::time::sleep;
use rand::Rng;
use colored::*;

mod config;
mod network;
mod particles;
mod verification;
mod output;

use config::QuantumConfig;
use network::NetworkManager;
use particles::{Particle, ParticleType, QuantumState};
use verification::{VerificationAlgorithm, BellStateVerifier, GHZStateVerifier, WStateVerifier};
use output::{QuantumOutput, OutputConfig};

/// Nightly Quantum Entanglement Checker
/// A whimsical CLI tool for simulating quantum entanglement verification
#[derive(Parser, Debug)]
#[command(name = "nightly-quantum-entanglement-checker")]
#[command(about = "A whimsical CLI tool that simulates quantum entanglement verification for distributed systems")]
#[command(version = "1.0.0")]
struct Args {
    /// Comma-separated list of nodes in format host:port
    #[arg(short, long, value_delimiter = ',')]
    nodes: Vec<String>,
    
    /// Particle type for entanglement
    #[arg(short, long, value_enum, default_value_t = ParticleType::Photon)]
    particle_type: ParticleType,
    
    /// Verification algorithm to use
    #[arg(short, long, value_enum, default_value_t = VerificationAlgorithm::BellState)]
    algorithm: VerificationAlgorithm,
    
    /// Network topology
    #[arg(short, long, value_enum, default_value_t = NetworkTopology::Star)]
    topology: NetworkTopology,
    
    /// Verification timeout in seconds
    #[arg(short, long, default_value = "30")]
    timeout: u64,
    
    /// Path to configuration file
    #[arg(short, long)]
    config: Option<String>,
    
    /// Enable verbose output
    #[arg(short, long)]
    verbose: bool,
    
    /// Enable metrics output
    #[arg(short, long)]
    metrics: bool,
    
    /// Enable ASCII animations
    #[arg(short, long)]
    animations: bool,
    
    /// Enable debug mode
    #[arg(short, long)]
    debug: bool,
}

#[derive(Clone, Debug, ValueEnum)]
enum NetworkTopology {
    Star,
    Ring,
    Mesh,
    Tree,
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();
    
    // Load configuration
    let config = load_config(&args)?;
    
    // Initialize output
    let output_config = OutputConfig {
        verbose: args.verbose || config.output.verbose,
        metrics: args.metrics || config.output.metrics,
        animations: args.animations || config.output.animations,
        debug: args.debug,
    };
    let mut output = QuantumOutput::new(output_config);
    
    // Display header
    output.show_header();
    
    // Initialize network
    let mut network = NetworkManager::new(config.network.topology, output.clone());
    for node in &config.network.nodes {
        network.add_node(node.clone());
    }
    
    // Generate entangled particles
    let particles = generate_entangled_particles(
        &config.particles.particle_type,
        network.get_node_count(),
    );
    
    if output.config.verbose {
        output.show_particle_generation(&particles);
    }
    
    // Initialize verification algorithm
    let mut verifier = create_verifier(&config.network.algorithm);
    
    // Start verification process
    let start_time = Instant::now();
    let timeout_duration = Duration::from_secs(config.network.timeout);
    
    output.show_verification_start(&config);
    
    // Simulate network communication and verification
    let results = network.simulate_entanglement_verification(
        &particles,
        &mut *verifier,
        timeout_duration,
    ).await;
    
    let elapsed = start_time.elapsed();
    
    // Display results
    output.show_verification_results(&results, elapsed);
    
    // Show ASCII art if enabled
    if output.config.animations {
        output.show_entanglement_art(&results);
    }
    
    // Show metrics if enabled
    if output.config.metrics {
        output.show_metrics(&results, elapsed);
    }
    
    // Exit with appropriate code
    if results.all_entangled() {
        std::process::exit(0);
    } else {
        std::process::exit(1);
    }
}

fn load_config(args: &Args) -> Result<QuantumConfig, Box<dyn std::error::Error>> {
    if let Some(config_path) = &args.config {
        QuantumConfig::from_file(config_path)
    } else {
        // Create config from args
        let mut config = QuantumConfig::default();
        config.network.nodes = args.nodes.clone();
        config.network.algorithm = args.algorithm.clone();
        config.network.topology = args.topology.clone();
        config.network.timeout = args.timeout;
        config.particles.particle_type = args.particle_type.clone();
        config.output.verbose = args.verbose;
        config.output.metrics = args.metrics;
        config.output.animations = args.animations;
        Ok(config)
    }
}

fn generate_entangled_particles(
    particle_type: &ParticleType,
    count: usize,
) -> Vec<Particle> {
    let mut particles = Vec::new();
    let mut rng = rand::thread_rng();
    
    // Generate base state
    let base_state = if rng.gen_bool(0.5) {
        QuantumState::SpinUp
    } else {
        QuantumState::SpinDown
    };
    
    for i in 0..count {
        let state = if i == 0 {
            base_state
        } else {
            // Entangled particles have opposite states
            match base_state {
                QuantumState::SpinUp => QuantumState::SpinDown,
                QuantumState::SpinDown => QuantumState::SpinUp,
            }
        };
        
        particles.push(Particle::new(particle_type.clone(), state, i as u64));
    }
    
    particles
}

fn create_verifier(algorithm: &VerificationAlgorithm) -> Box<dyn verification::VerificationAlgorithm> {
    match algorithm {
        VerificationAlgorithm::BellState => Box::new(BellStateVerifier::new()),
        VerificationAlgorithm::GHZState => Box::new(GHZStateVerifier::new()),
        VerificationAlgorithm::WState => Box::new(WStateVerifier::new()),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::time::Duration;
    
    #[tokio::test]
    async fn test_entanglement_verification_success() {
        let mut config = QuantumConfig::default();
        config.network.nodes = vec!["localhost:8080".to_string(), "localhost:8081".to_string()];
        config.network.algorithm = VerificationAlgorithm::BellState;
        config.network.timeout = 5;
        
        let output_config = OutputConfig {
            verbose: false,
            metrics: false,
            animations: false,
            debug: false,
        };
        let output = QuantumOutput::new(output_config);
        
        let mut network = NetworkManager::new(config.network.topology, output);
        for node in &config.network.nodes {
            network.add_node(node.clone());
        }
        
        let particles = generate_entangled_particles(&config.particles.particle_type, 2);
        let mut verifier = create_verifier(&config.network.algorithm);
        
        let results = network.simulate_entanglement_verification(
            &particles,
            &mut *verifier,
            Duration::from_secs(5),
        ).await;
        
        assert!(results.all_entangled());
        assert_eq!(results.nodes.len(), 2);
    }
    
    #[tokio::test]
    async fn test_entanglement_verification_timeout() {
        let mut config = QuantumConfig::default();
        config.network.nodes = vec!["localhost:8080".to_string()];
        config.network.algorithm = VerificationAlgorithm::BellState;
        config.network.timeout = 1; // Very short timeout
        
        let output_config = OutputConfig {
            verbose: false,
            metrics: false,
            animations: false,
            debug: false,
        };
        let output = QuantumOutput::new(output_config);
        
        let mut network = NetworkManager::new(config.network.topology, output);
        for node in &config.network.nodes {
            network.add_node(node.clone());
        }
        
        let particles = generate_entangled_particles(&config.particles.particle_type, 1);
        let mut verifier = create_verifier(&config.network.algorithm);
        
        // Simulate slow network
        network.set_network_delay(Duration::from_secs(2));
        
        let results = network.simulate_entanglement_verification(
            &particles,
            &mut *verifier,
            Duration::from_secs(1),
        ).await;
        
        assert!(!results.all_entangled());
        assert!(results.nodes[0].decoherence > 50.0); // High decoherence due to timeout
    }
}
