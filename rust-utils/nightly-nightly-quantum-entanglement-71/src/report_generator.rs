use crate::quantum_simulator::{EntanglementResult, DecoherenceRisk, QuantumState};
use std::time::Duration;
use crate::config::Config;

pub struct ReportGenerator;

impl ReportGenerator {
    pub fn new() -> Self {
        ReportGenerator
    }

    pub fn generate_report(
        &self,
        nodes: &[&str],
        result: &EntanglementResult,
        duration: Duration,
        config: &Config,
    ) -> String {
        let mut report = String::new();
        
        // Header
        report.push_str("🔬 Quantum Entanglement Verification Report\n");
        report.push_str("==========================================\n\n");
        
        // Basic info
        report.push_str(&format!("📍 Nodes: {}\n", nodes.join(" ↔ ")));
        report.push_str(&format!("⚡ Entanglement Strength: {:.2}\n", config.quantum.entanglement_strength));
        report.push_str(&format!("🔮 Quantum Coherence: {:.2}\n", result.quantum_coherence));
        report.push_str(&format!("⏱️  Verification Time: {}ms\n\n", duration.as_millis()));
        
        // Result
        if result.entanglement_confirmed {
            report.push_str("✅ ENTANGLEMENT CONFIRMED\n");
            report.push_str("\"Spooky action at a distance\" detected!\n\n");
        } else {
            report.push_str("❌ ENTANGLEMENT FAILED\n");
            report.push_str("Quantum decoherence detected!\n\n");
            report.push_str("⚠️  Warning: Measurement collapse probability high\n\n");
        }
        
        // Metrics
        report.push_str("📊 Metrics:\n");
        report.push_str(&format!("  - Bell State Fidelity: {:.0}%\n", result.bell_state_fidelity));
        report.push_str(&format!("  - Quantum Correlation: {:.2}\n", result.quantum_correlation));
        
        // Decoherence risk
        let risk_str = match result.decoherence_risk {
            DecoherenceRisk::Low => "LOW",
            DecoherenceRisk::Medium => "MEDIUM",
            DecoherenceRisk::High => "HIGH",
        };
        report.push_str(&format!("  - Decoherence Risk: {}\n", risk_str));
        
        // Measurement outcomes
        if config.verbose {
            report.push_str("\n⚛️  Measurement Outcomes:\n");
            for (node, state) in &result.measurement_outcomes {
                let state_str = match state {
                    QuantumState::Entangled => "Entangled",
                    QuantumState::Superposition => "Superposition",
                    QuantumState::Collapsed => "Collapsed",
                };
                report.push_str(&format!("  - {}: {}\n", node, state_str));
            }
        }
        
        // Additional info for detailed reports
        if config.report_type == "detailed" {
            report.push_str("\n🔬 Additional Analysis:\n");
            report.push_str(&format!("  - Entanglement Threshold: {:.2}\n", config.quantum.coherence_threshold));
            report.push_str(&format!("  - Distributed Mode: {}\n", if config.distributed { "Enabled" } else { "Disabled" }));
            if config.distributed {
                report.push_str(&format!("  - Latency Simulation: {}\n", config.quantum.latency_simulation));
            }
        }
        
        report
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::quantum_simulator::{DecoherenceRisk, QuantumState};
    use std::collections::HashMap;
    use std::time::Duration;
    
    #[test]
    fn test_generate_success_report() {
        let generator = ReportGenerator::new();
        let nodes = vec!["node1", "node2"];
        
        let mut measurement_outcomes = HashMap::new();
        measurement_outcomes.insert("node1".to_string(), QuantumState::Entangled);
        measurement_outcomes.insert("node2".to_string(), QuantumState::Entangled);
        
        let result = EntanglementResult {
            entanglement_confirmed: true,
            quantum_coherence: 0.92,
            bell_state_fidelity: 92.0,
            quantum_correlation: 0.87,
            decoherence_risk: DecoherenceRisk::Low,
            measurement_outcomes,
        };
        
        let config = Config {
            nodes: vec!["node1", "node2"],
            quantum: crate::config::QuantumConfig {
                entanglement_strength: 0.85,
                coherence_threshold: 0.8,
                latency_simulation: Duration::from_millis(0),
            },
            distributed: false,
            report_type: "simple".to_string(),
            verbose: false,
        };
        
        let report = generator.generate_report(&nodes, &result, Duration::from_millis(42), &config);
        
        assert!(report.contains("✅ ENTANGLEMENT CONFIRMED"));
        assert!(report.contains("Bell State Fidelity: 92%"));
        assert!(report.contains("Decoherence Risk: LOW"));
    }
    
    #[test]
    fn test_generate_failure_report() {
        let generator = ReportGenerator::new();
        let nodes = vec!["node1", "node2"];
        
        let mut measurement_outcomes = HashMap::new();
        measurement_outcomes.insert("node1".to_string(), QuantumState::Collapsed);
        measurement_outcomes.insert("node2".to_string(), QuantumState::Collapsed);
        
        let result = EntanglementResult {
            entanglement_confirmed: false,
            quantum_coherence: 0.45,
            bell_state_fidelity: 45.0,
            quantum_correlation: 0.32,
            decoherence_risk: DecoherenceRisk::High,
            measurement_outcomes,
        };
        
        let config = Config {
            nodes: vec!["node1", "node2"],
            quantum: crate::config::QuantumConfig {
                entanglement_strength: 0.3,
                coherence_threshold: 0.8,
                latency_simulation: Duration::from_millis(0),
            },
            distributed: false,
            report_type: "simple".to_string(),
            verbose: false,
        };
        
        let report = generator.generate_report(&nodes, &result, Duration::from_millis(150), &config);
        
        assert!(report.contains("❌ ENTANGLEMENT FAILED"));
        assert!(report.contains("Decoherence Risk: HIGH"));
        assert!(report.contains("Measurement collapse probability high"));
    }
}
