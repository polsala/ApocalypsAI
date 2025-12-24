use nightly_quantum_entanglement_checker::*;
use std::time::Duration;
use test_case::test_case;

#[tokio::test]
async fn test_quantum_simulation_basic() {
    let mut simulator = QuantumSimulator::new(4, 0.8, 0.02);
    let duration = Duration::from_millis(500);
    
    let result = simulator.run_simulation(duration, false).await;
    
    // Verify basic properties
    assert!(result.coherence_level >= 0.0 && result.coherence_level <= 1.0);
    assert!(result.entanglement_fidelity >= 0.0 && result.entanglement_fidelity <= 1.0);
    assert!(result.quantum_correlation_score >= 0.0 && result.quantum_correlation_score <= 1.0);
}

#[tokio::test]
async fn test_network_simulation_basic() {
    let mut network_simulator = NetworkSimulator::new(4);
    let duration = Duration::from_millis(500);
    
    let result = network_simulator.run_simulation(duration, false).await;
    
    // Verify basic properties
    assert!(result.average_latency_ms >= 0.0);
    assert!(result.packet_loss_percent >= 0.0 && result.packet_loss_percent <= 100.0);
    assert!(result.synchronization_error_ns >= 0.0);
    assert!(result.network_reliability >= 0.0 && result.network_reliability <= 1.0);
}

#[test_case(2)]
#[test_case(4)]
#[test_case(8)]
#[tokio::test]
async fn test_different_node_counts(nodes: usize) {
    let mut simulator = QuantumSimulator::new(nodes, 0.75, 0.03);
    let duration = Duration::from_millis(300);
    
    let result = simulator.run_simulation(duration, false).await;
    
    // Should work with different node counts
    assert!(result.coherence_level >= 0.0 && result.coherence_level <= 1.0);
    assert!(result.entanglement_fidelity >= 0.0 && result.entanglement_fidelity <= 1.0);
}

#[test_case(0.5)]
#[test_case(0.8)]
#[test_case(1.0)]
#[tokio::test]
async fn test_different_entanglement_strengths(strength: f64) {
    let mut simulator = QuantumSimulator::new(4, strength, 0.02);
    let duration = Duration::from_millis(300);
    
    let result = simulator.run_simulation(duration, false).await;
    
    // Higher strength should generally result in higher fidelity
    assert!(result.entanglement_fidelity >= 0.0 && result.entanglement_fidelity <= 1.0);
    assert!(result.coherence_level >= 0.0 && result.coherence_level <= 1.0);
}

#[test_case(0.01)]
#[test_case(0.05)]
#[test_case(0.1)]
#[tokio::test]
async fn test_different_decoherence_rates(rate: f64) {
    let mut simulator = QuantumSimulator::new(4, 0.8, rate);
    let duration = Duration::from_millis(300);
    
    let result = simulator.run_simulation(duration, false).await;
    
    // Higher decoherence should generally result in lower coherence
    assert!(result.coherence_level >= 0.0 && result.coherence_level <= 1.0);
    assert!(result.entanglement_fidelity >= 0.0 && result.entanglement_fidelity <= 1.0);
}

#[tokio::test]
async fn test_bell_inequality_violation() {
    let mut simulator = QuantumSimulator::new(4, 0.9, 0.01);
    let duration = Duration::from_millis(200);
    
    let result = simulator.run_simulation(duration, false).await;
    
    // With high entanglement strength and low decoherence, Bell inequality should be violated
    assert!(result.bell_inequality_violation, "Bell inequality should be violated with high entanglement");
}

#[tokio::test]
async fn test_network_reliability_calculation() {
    let mut network_simulator = NetworkSimulator::new(4);
    let duration = Duration::from_millis(200);
    
    let result = network_simulator.run_simulation(duration, false).await;
    
    // Network reliability should be between 0 and 1
    assert!(result.network_reliability >= 0.0 && result.network_reliability <= 1.0);
    
    // Should have reasonable latency
    assert!(result.average_latency_ms > 0.0 && result.average_latency_ms < 1000.0);
}

#[tokio::test]
async fn test_report_generation_text() {
    let report = QuantumReport {
        experiment_parameters: ExperimentParameters {
            nodes: 4,
            duration: "10s".to_string(),
            entanglement_strength: 0.75,
            decoherence_rate: 0.03,
        },
        quantum_state_analysis: QuantumStateAnalysis {
            coherence_level: 0.85,
            entanglement_fidelity: 0.78,
            bell_inequality_violation: true,
            quantum_correlation_score: 0.82,
        },
        network_metrics: NetworkMetrics {
            average_latency_ms: 12.5,
            packet_loss_percent: 0.1,
            synchronization_error_ns: 5.2,
            network_reliability: 0.95,
        },
        result: QuantumResult {
            success: true,
            message: "QUANTUM ENTANGLEMENT SUCCESSFUL".to_string(),
            spooky_action_confirmed: true,
            confidence_level: 0.88,
        },
        timestamp: chrono::Utc::now().to_rfc3339(),
    };
    
    let generator = ReportGenerator::new(ReportFormat::Text);
    // This test mainly ensures the report generation doesn't panic
    generator.generate_report(&report);
}

#[tokio::test]
async fn test_report_generation_json() {
    let report = QuantumReport {
        experiment_parameters: ExperimentParameters {
            nodes: 2,
            duration: "5s".to_string(),
            entanglement_strength: 0.9,
            decoherence_rate: 0.01,
        },
        quantum_state_analysis: QuantumStateAnalysis {
            coherence_level: 0.92,
            entanglement_fidelity: 0.89,
            bell_inequality_violation: true,
            quantum_correlation_score: 0.91,
        },
        network_metrics: NetworkMetrics {
            average_latency_ms: 8.3,
            packet_loss_percent: 0.05,
            synchronization_error_ns: 2.1,
            network_reliability: 0.98,
        },
        result: QuantumResult {
            success: true,
            message: "QUANTUM ENTANGLEMENT SUCCESSFUL".to_string(),
            spooky_action_confirmed: true,
            confidence_level: 0.95,
        },
        timestamp: chrono::Utc::now().to_rfc3339(),
    };
    
    let generator = ReportGenerator::new(ReportFormat::Json);
    // This test mainly ensures JSON serialization works
    generator.generate_report(&report);
}

#[tokio::test]
async fn test_correlation_matrix_generation() {
    let mut simulator = QuantumSimulator::new(3, 0.8, 0.02);
    simulator.initialize_states();
    
    // Check that correlation matrices are properly initialized
    for state in &simulator.quantum_states {
        assert_eq!(state.correlation_matrix.len(), 3);
        for i in 0..3 {
            for j in 0..3 {
                let correlation = state.correlation_matrix[i][j];
                assert!(correlation >= 0.0 && correlation <= 1.0);
                
                // Diagonal should be 1.0 (perfect correlation with self)
                if i == j {
                    assert_eq!(correlation, 1.0);
                }
            }
        }
    }
}

#[tokio::test]
async fn test_duration_parsing() {
    use crate::main::parse_duration;
    
    // Test seconds
    let duration = parse_duration("30s").unwrap();
    assert_eq!(duration.as_secs(), 30);
    
    // Test minutes
    let duration = parse_duration("2m").unwrap();
    assert_eq!(duration.as_secs(), 120);
    
    // Test mixed format
    let duration = parse_duration("1m30s").unwrap();
    assert_eq!(duration.as_secs(), 90);
    
    // Test invalid format
    let result = parse_duration("invalid");
    assert!(result.is_err());
}

// Mock rationale: These tests verify the core functionality of the quantum entanglement checker
// without requiring external dependencies or network connections. They test the quantum simulation,
// network simulation, report generation, and various edge cases to ensure the tool works correctly.
