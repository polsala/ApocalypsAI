use nightly_quantum_entanglement_checker::*;
use quantum_sim::QuantumEntanglementSimulator;
use std::net::IpAddr;

#[tokio::test]
async fn test_quantum_measurement_range() {
    let simulator = QuantumEntanglementSimulator::new();
    
    for _ in 0..100 {
        let measurement = simulator.measure_entanglement();
        assert!(measurement.coherence >= 0.0 && measurement.coherence <= 1.0,
                "Coherence out of range: {}", measurement.coherence);
        assert!(measurement.timestamp > 0,
                "Invalid timestamp: {}", measurement.timestamp);
    }
}

#[tokio::test]
async fn test_entanglement_strength_calculation() {
    let simulator = QuantumEntanglementSimulator::new();
    
    let measurements = vec![
        quantum_sim::QuantumMeasurement { coherence: 0.8, superposition: true, timestamp: 1 },
        quantum_sim::QuantumMeasurement { coherence: 0.9, superposition: true, timestamp: 2 },
        quantum_sim::QuantumMeasurement { coherence: 0.7, superposition: true, timestamp: 3 },
    ];
    
    let strength = simulator.calculate_entanglement_strength(&measurements);
    assert_eq!(strength, 0.8);
}

#[tokio::test]
async fn test_empty_measurements_strength() {
    let simulator = QuantumEntanglementSimulator::new();
    let measurements = vec![];
    
    let strength = simulator.calculate_entanglement_strength(&measurements);
    assert_eq!(strength, 0.0);
}

#[tokio::test]
async fn test_quantum_anomaly_detection() {
    let simulator = QuantumEntanglementSimulator::new();
    
    // Test normal measurement
    let normal = quantum_sim::QuantumMeasurement {
        coherence: 0.5,
        superposition: true,
        timestamp: 1,
    };
    assert!(!simulator.detect_quantum_anomaly(&normal));
    
    // Test anomaly (too perfect)
    let perfect = quantum_sim::QuantumMeasurement {
        coherence: 0.995,
        superposition: true,
        timestamp: 1,
    };
    assert!(simulator.detect_quantum_anomaly(&perfect));
    
    // Test anomaly (too chaotic)
    let chaotic = quantum_sim::QuantumMeasurement {
        coherence: 0.005,
        superposition: false,
        timestamp: 1,
    };
    assert!(simulator.detect_quantum_anomaly(&chaotic));
}

#[tokio::test]
async fn test_config_parsing() {
    // Test that we can parse basic configuration
    let config = super::parse_args();
    assert!(config.threshold >= 0.0 && config.threshold <= 1.0);
    assert!(config.timeout_ms > 0);
    assert!(!config.nodes.is_empty());
}

#[tokio::test]
async fn test_network_checker_timeout() {
    use network_checker::NetworkChecker;
    
    let checker = NetworkChecker::new(100); // 100ms timeout
    let invalid_ip: IpAddr = "192.0.2.1".parse().unwrap(); // TEST-NET-1 (should be unreachable)
    
    let result = checker.ping(&invalid_ip).await;
    assert!(result.is_ok());
    assert!(!result.unwrap()); // Should return false for unreachable host
}
