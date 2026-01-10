use crate::config::{QuantumConfig, NetworkTopology, VerificationAlgorithm, ParticleType};
use crate::network::VerificationResult;
use crate::particles::Particle;
use crate::network::VerificationResults;
use std::time::Duration;
use colored::*;

#[derive(Debug, Clone)]
pub struct OutputConfig {
    pub verbose: bool,
    pub metrics: bool,
    pub animations: bool,
    pub debug: bool,
}

pub struct QuantumOutput {
    pub config: OutputConfig,
}

impl QuantumOutput {
    pub fn new(config: OutputConfig) -> Self {
        Self { config }
    }
    
    pub fn show_header(&self) {
        println!("{}", "🔬 Quantum Entanglement Verification".bright_cyan().bold());
        println!("{}", "=".repeat(45).bright_cyan());
        println!();
    }
    
    pub fn show_verification_start(&self, config: &QuantumConfig) {
        println!("{}", "📡 Sending entangled particles...".bright_yellow());
        println!();
        
        if self.config.verbose {
            println!("Configuration:");
            println!("  Particle Type: {}", format!("{:?}", config.particles.particle_type).bright_green());
            println!("  Algorithm: {}", format!("{:?}", config.network.algorithm).bright_green());
            println!("  Topology: {}", format!("{:?}", config.network.topology).bright_green());
            println!("  Nodes: {}", config.network.nodes.len());
            println!();
        }
    }
    
    pub fn show_particle_generation(&self, particles: &[Particle]) {
        println!("{}", "⚛️ Generated entangled particles:".bright_magenta());
        for particle in particles {
            println!("  {}", particle.to_string().bright_cyan());
        }
        println!();
    }
    
    pub fn show_node_status(&self, result: &VerificationResult) {
        let status = if result.entangled {
            "✓ Entangled".bright_green()
        } else {
            "✗ Decoherence".bright_red()
        };
        
        println!(
            "{} Node {} ({}ms) - {}",
            result.node_id.bright_yellow(),
            result.node_id,
            result.response_time.as_millis(),
            status,
        );
    }
    
    pub fn show_verification_results(&self, results: &VerificationResults, elapsed: Duration) {
        println!();
        
        if results.all_entangled() {
            println!("{}", "🎉 All particles successfully entangled!".bright_green().bold());
        } else {
            println!("{}", "❌ Entanglement verification failed!".bright_red().bold());
        }
        
        println!("{}: {:.1}%", "Fidelity".bright_cyan(), results.overall_fidelity);
        println!("{}: {:.1}%", "Success Rate".bright_cyan(), results.success_rate());
        println!("{}: {:.2?}", "Total Time".bright_cyan(), elapsed);
        println!("{}: {:.2?}", "Avg Response".bright_cyan(), results.average_response_time);
        
        if !results.all_entangled() {
            println!();
            println!("{}:", "Failed Nodes".bright_red().bold());
            for result in &results.nodes {
                if !result.entangled {
                    println!("  - {} (Decoherence: {:.1}%)", 
                        result.node_id.bright_yellow(),
                        result.decoherence);
                }
            }
        }
    }
    
    pub fn show_entanglement_art(&self, results: &VerificationResults) {
        println!();
        println!("{}", "ASCII Art:".bright_magenta().bold());
        println!();
        
        if results.all_entangled() {
            println!("    ⚛️  ⚛️  ⚛️");
            println!("     \ | /");
            println!("      \|/");
            println!("       ✦");
            println!("      /|\");
            println!("     / | \");
            println!("    ⚛️  ⚛️  ⚛️");
        } else {
            println!("    ⚛️  ⚛️  ⚛️");
            println!("     \ | /");
            println!("      \|/");
            println!("       ✗");
            println!("      /|\");
            println!("     / | \");
            println!("    ⚛️  ⚛️  ⚛️");
        }
        println!();
    }
    
    pub fn show_metrics(&self, results: &VerificationResults, elapsed: Duration) {
        println!();
        println!("{}", "Detailed Metrics:".bright_blue().bold());
        println!("{}", "=".repeat(20).bright_blue());
        
        for (i, result) in results.nodes.iter().enumerate() {
            println!("Node {}:", i + 1);
            println!("  ID: {}", result.node_id.bright_yellow());
            println!("  Status: {}", if result.entangled { "ENTANGLED".bright_green() } else { "DECOHERED".bright_red() });
            println!("  Fidelity: {:.1}%", result.fidelity);
            println!("  Decoherence: {:.1}%", result.decoherence);
            println!("  Response Time: {:.2?}", result.response_time);
            if let Some(error) = &result.error {
                println!("  Error: {}", error.bright_red());
            }
            println!();
        }
        
        println!("Summary:");
        println!("  Total Nodes: {}", results.nodes.len());
        println!("  Successful: {}", results.nodes.iter().filter(|r| r.entangled).count());
        println!("  Failed: {}", results.nodes.iter().filter(|r| !r.entangled).count());
        println!("  Overall Fidelity: {:.1}%", results.overall_fidelity);
        println!("  Average Response Time: {:.2?}", results.average_response_time);
        println!("  Total Execution Time: {:.2?}", elapsed);
    }
    
    pub fn show_debug_info(&self, message: &str) {
        if self.config.debug {
            println!("{} {}", "[DEBUG]".bright_black(), message.bright_black());
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::network::VerificationResult;
    use std::time::Duration;
    
    #[test]
    fn test_output_config_default() {
        let config = OutputConfig {
            verbose: false,
            metrics: false,
            animations: false,
            debug: false,
        };
        
        assert!(!config.verbose);
        assert!(!config.metrics);
        assert!(!config.animations);
        assert!(!config.debug);
    }
    
    #[test]
    fn test_verification_results_display() {
        let results = VerificationResults {
            nodes: vec![
                VerificationResult {
                    node_id: "node1:8080".to_string(),
                    entangled: true,
                    fidelity: 95.0,
                    decoherence: 5.0,
                    response_time: Duration::from_millis(100),
                    error: None,
                },
                VerificationResult {
                    node_id: "node2:8080".to_string(),
                    entangled: false,
                    fidelity: 45.0,
                    decoherence: 55.0,
                    response_time: Duration::from_millis(150),
                    error: Some("Decoherence detected".to_string()),
                },
            ],
            overall_fidelity: 70.0,
            average_response_time: Duration::from_millis(125),
        };
        
        assert!(!results.all_entangled());
        assert_eq!(results.success_rate(), 50.0);
    }
}
