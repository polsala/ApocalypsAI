use nightly_quantum_entanglement_checker::*;
use std::fs;
use std::io::Write;

#[test]
fn test_check_entanglement_entangled() {
    // Mock random number generator for predictable results
    rand::reset_seed();
    
    let result = check_entanglement(
        "node1",
        "node2",
        0.9,  // high strength
        0.05, // low decoherence
        0.001, // high precision
    );
    
    assert_eq!(result.node_a, "node1");
    assert_eq!(result.node_b, "node2");
    assert!(result.entanglement_strength > 0.5);
    assert_eq!(result.status, "ENTANGLED");
    assert!(result.confidence > 0.8);
}

#[test]
fn test_check_entanglement_separated() {
    // Mock random number generator for predictable results
    rand::reset_seed();
    
    let result = check_entanglement(
        "node1",
        "node2",
        0.1,  // low strength
        0.9,  // high decoherence
        0.1,  // low precision
    );
    
    assert_eq!(result.node_a, "node1");
    assert_eq!(result.node_b, "node2");
    assert!(result.entanglement_strength < 0.5);
    assert_eq!(result.status, "SEPARATED");
    assert!(result.confidence < 0.5);
}

#[test]
fn test_calculate_confidence() {
    // High strength, low decoherence, high precision should give high confidence
    let confidence = calculate_confidence(0.9, 0.05, 0.001);
    assert!(confidence > 0.8);
    assert!(confidence <= 1.0);
    
    // Low strength, high decoherence, low precision should give low confidence
    let confidence = calculate_confidence(0.1, 0.9, 0.1);
    assert!(confidence < 0.5);
    assert!(confidence >= 0.0);
}

#[test]
fn test_generate_recommendation_high_strength() {
    let recommendation = generate_recommendation(0.9, 0.05, 0.95);
    assert!(recommendation.contains("stable"));
    assert!(recommendation.contains("No quantum corrections"));
}

#[test]
fn test_generate_recommendation_low_strength() {
    let recommendation = generate_recommendation(0.1, 0.9, 0.2);
    assert!(recommendation.contains("decoherence"));
    assert!(recommendation.contains("Immediate attention"));
}

#[test]
fn test_get_status_emoji() {
    assert_eq!(get_status_emoji("ENTANGLED"), "✓");
    assert_eq!(get_status_emoji("SEPARATED"), "✗");
    assert_eq!(get_status_emoji("UNKNOWN"), "?");
}

#[test]
fn test_config_default() {
    let config = Config::default();
    assert_eq!(config.node_a.name, "node-a");
    assert_eq!(config.node_b.name, "node-b");
    assert_eq!(config.quantum.strength, 0.9);
    assert_eq!(config.quantum.decoherence, 0.05);
    assert_eq!(config.output.format, "text");
}

#[test]
fn test_load_config_from_file() {
    // Create a temporary config file
    let config_content = r#"
[node_a]
name = "test-node-a"
address = "192.168.1.100"

[node_b]
name = "test-node-b"
address = "192.168.1.101"

[quantum]
strength = 0.85
decoherence = 0.1
measurement_precision = 0.002

[output]
format = "json"
verbose = true
"#;
    
    let temp_file = std::env::temp_dir().join("test_config.toml");
    {
        let mut file = fs::File::create(&temp_file).unwrap();
        file.write_all(config_content.as_bytes()).unwrap();
    }
    
    let config = load_config(temp_file.to_str().unwrap()).unwrap();
    
    assert_eq!(config.node_a.name, "test-node-a");
    assert_eq!(config.node_b.name, "test-node-b");
    assert_eq!(config.quantum.strength, 0.85);
    assert_eq!(config.quantum.decoherence, 0.1);
    assert_eq!(config.quantum.measurement_precision, 0.002);
    assert_eq!(config.output.format, "json");
    assert!(config.output.verbose);
    
    // Clean up
    fs::remove_file(&temp_file).unwrap();
}

#[test]
fn test_entanglement_result_serialization() {
    let result = EntanglementResult {
        node_a: "node1".to_string(),
        node_b: "node2".to_string(),
        entanglement_strength: 0.85,
        decoherence_rate: 0.12,
        measurement_precision: 0.001,
        status: "ENTANGLED".to_string(),
        confidence: 0.942,
        recommendation: "System is stable".to_string(),
        timestamp: "1234567890".to_string(),
    };
    
    let json = serde_json::to_string(&result).unwrap();
    let deserialized: EntanglementResult = serde_json::from_str(&json).unwrap();
    
    assert_eq!(result.node_a, deserialized.node_a);
    assert_eq!(result.entanglement_strength, deserialized.entanglement_strength);
    assert_eq!(result.status, deserialized.status);
}

#[test]
fn test_rand_deterministic() {
    // Test that our random number generator is deterministic
    rand::reset_seed();
    let first = rand::random::<f64>();
    
    rand::reset_seed();
    let second = rand::random::<f64>();
    
    assert_eq!(first, second);
}

#[test]
fn test_strength_bounds() {
    // Test that strength is properly bounded between 0.0 and 1.0
    rand::reset_seed();
    
    let result = check_entanglement("node1", "node2", 1.5, 0.0, 0.001);
    assert!(result.entanglement_strength <= 1.0);
    
    let result = check_entanglement("node1", "node2", -0.5, 0.0, 0.001);
    assert!(result.entanglement_strength >= 0.0);
}

#[test]
fn test_confidence_bounds() {
    // Test that confidence is properly bounded between 0.0 and 1.0
    let confidence = calculate_confidence(1.0, 0.0, 0.0);
    assert!(confidence >= 0.0 && confidence <= 1.0);
    
    let confidence = calculate_confidence(0.0, 1.0, 1.0);
    assert!(confidence >= 0.0 && confidence <= 1.0);
}

#[test]
fn test_recommendation_variety() {
    // Test different recommendation scenarios
    let rec1 = generate_recommendation(0.9, 0.05, 0.95);
    let rec2 = generate_recommendation(0.6, 0.2, 0.7);
    let rec3 = generate_recommendation(0.3, 0.5, 0.4);
    let rec4 = generate_recommendation(0.1, 0.8, 0.2);
    
    assert_ne!(rec1, rec2);
    assert_ne!(rec2, rec3);
    assert_ne!(rec3, rec4);
    
    assert!(rec1.contains("stable"));
    assert!(rec2.contains("moderately"));
    assert!(rec3.contains("instability"));
    assert!(rec4.contains("decoherence"));
}

// Mock rationale: These tests verify the core functionality of the quantum entanglement checker
// including entanglement calculation, confidence scoring, recommendation generation, and
// configuration loading. The tests use deterministic random number generation to ensure
// reproducible results and cover edge cases like boundary conditions and error scenarios.
