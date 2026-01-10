use crate::particles::Particle;
use crate::verification::VerificationAlgorithm;
use crate::output::QuantumOutput;
use std::collections::HashMap;
use std::time::{Duration, Instant};
use tokio::time::sleep;
use rand::Rng;

#[derive(Debug)]
pub struct VerificationResult {
    pub node_id: String,
    pub entangled: bool,
    pub fidelity: f64,
    pub decoherence: f64,
    pub response_time: Duration,
    pub error: Option<String>,
}

#[derive(Debug)]
pub struct VerificationResults {
    pub nodes: Vec<VerificationResult>,
    pub overall_fidelity: f64,
    pub average_response_time: Duration,
}

impl VerificationResults {
    pub fn all_entangled(&self) -> bool {
        self.nodes.iter().all(|r| r.entangled)
    }
    
    pub fn success_rate(&self) -> f64 {
        let total = self.nodes.len() as f64;
        let successful = self.nodes.iter().filter(|r| r.entangled).count() as f64;
        (successful / total) * 100.0
    }
}

pub struct NetworkManager {
    nodes: Vec<String>,
    topology: crate::config::NetworkTopology,
    output: QuantumOutput,
    network_delay: Duration,
}

impl NetworkManager {
    pub fn new(topology: crate::config::NetworkTopology, output: QuantumOutput) -> Self {
        Self {
            nodes: Vec::new(),
            topology,
            output,
            network_delay: Duration::from_millis(100),
        }
    }
    
    pub fn add_node(&mut self, node: String) {
        self.nodes.push(node);
    }
    
    pub fn get_node_count(&self) -> usize {
        self.nodes.len()
    }
    
    pub fn set_network_delay(&mut self, delay: Duration) {
        self.network_delay = delay;
    }
    
    pub async fn simulate_entanglement_verification(
        &self,
        particles: &[Particle],
        verifier: &mut dyn VerificationAlgorithm,
        timeout: Duration,
    ) -> VerificationResults {
        let start_time = Instant::now();
        let mut results = Vec::new();
        
        for (i, node) in self.nodes.iter().enumerate() {
            let particle = &particles[i % particles.len()];
            let result = self.verify_node_entanglement(
                node,
                particle,
                verifier,
                timeout,
            ).await;
            
            results.push(result);
            
            if self.output.config.verbose {
                self.output.show_node_status(&results.last().unwrap());
            }
        }
        
        let elapsed = start_time.elapsed();
        let overall_fidelity = self.calculate_overall_fidelity(&results);
        let average_response_time = self.calculate_average_response_time(&results);
        
        VerificationResults {
            nodes: results,
            overall_fidelity,
            average_response_time,
        }
    }
    
    async fn verify_node_entanglement(
        &self,
        node: &str,
        particle: &Particle,
        verifier: &mut dyn VerificationAlgorithm,
        timeout: Duration,
    ) -> VerificationResult {
        let start_time = Instant::now();
        
        // Simulate network delay
        sleep(self.network_delay).await;
        
        // Simulate quantum measurement
        let measurement_result = self.simulate_quantum_measurement(particle, timeout);
        
        let elapsed = start_time.elapsed();
        
        // Apply decoherence based on response time
        let decoherence = self.calculate_decoherence(elapsed);
        let fidelity = 100.0 - decoherence;
        
        // Verify entanglement
        let entangled = verifier.verify_entanglement(fidelity, decoherence);
        
        VerificationResult {
            node_id: node.to_string(),
            entangled,
            fidelity,
            decoherence,
            response_time: elapsed,
            error: if entangled { None } else { Some("Decoherence detected".to_string()) },
        }
    }
    
    fn simulate_quantum_measurement(&self, _particle: &Particle, timeout: Duration) -> bool {
        let mut rng = rand::thread_rng();
        
        // Simulate measurement time
        let measurement_time = Duration::from_millis(rng.gen_range(50..200));
        
        if measurement_time > timeout {
            return false; // Timeout
        }
        
        // Simulate quantum randomness
        rng.gen_bool(0.95) // 95% success rate for measurement
    }
    
    fn calculate_decoherence(&self, response_time: Duration) -> f64 {
        let base_decoherence = 1.0;
        let time_factor = response_time.as_millis() as f64 / 1000.0;
        
        // Exponential decoherence based on response time
        base_decoherence + (time_factor * time_factor * 2.0)
    }
    
    fn calculate_overall_fidelity(&self, results: &[VerificationResult]) -> f64 {
        let total_fidelity: f64 = results.iter().map(|r| r.fidelity).sum();
        total_fidelity / results.len() as f64
    }
    
    fn calculate_average_response_time(&self, results: &[VerificationResult]) -> Duration {
        let total_nanos: u128 = results.iter().map(|r| r.response_time.as_nanos()).sum();
        Duration::from_nanos((total_nanos / results.len() as u128) as u64)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::verification::{BellStateVerifier, VerificationAlgorithm};
    use crate::output::{QuantumOutput, OutputConfig};
    use std::time::Duration;
    
    #[tokio::test]
    async fn test_network_verification_success() {
        let output_config = OutputConfig {
            verbose: false,
            metrics: false,
            animations: false,
            debug: false,
        };
        let output = QuantumOutput::new(output_config);
        
        let mut network = NetworkManager::new(crate::config::NetworkTopology::Star, output);
        network.add_node("node1:8080".to_string());
        network.add_node("node2:8080".to_string());
        
        let particles = vec![
            Particle::new(crate::config::ParticleType::Photon, crate::particles::QuantumState::SpinUp, 1),
            Particle::new(crate::config::ParticleType::Photon, crate::particles::QuantumState::SpinDown, 2),
        ];
        
        let mut verifier = BellStateVerifier::new();
        let results = network.simulate_entanglement_verification(
            &particles,
            &mut verifier,
            Duration::from_secs(5),
        ).await;
        
        assert_eq!(results.nodes.len(), 2);
        assert!(results.overall_fidelity > 90.0);
        assert!(results.average_response_time.as_millis() > 0);
    }
    
    #[tokio::test]
    async fn test_network_decoherence_calculation() {
        let output_config = OutputConfig {
            verbose: false,
            metrics: false,
            animations: false,
            debug: false,
        };
        let output = QuantumOutput::new(output_config);
        
        let network = NetworkManager::new(crate::config::NetworkTopology::Star, output);
        
        // Test decoherence with different response times
        let short_time = Duration::from_millis(100);
        let long_time = Duration::from_millis(1000);
        
        let short_decoherence = network.calculate_decoherence(short_time);
        let long_decoherence = network.calculate_decoherence(long_time);
        
        assert!(short_decoherence < long_decoherence);
        assert!(short_decoherence > 0.0);
        assert!(long_decoherence > 0.0);
    }
}
