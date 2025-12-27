use nightly_quantum_entanglement_checker::*;
use std::fs;
use tempfile::NamedTempFile;

#[test]
fn test_quantum_checker_basic() {
    let checker = QuantumChecker::new(
        "NodeA".to_string(),
        "NodeB".to_string(),
        VerificationMode::Quantum,
        0.8,
        MeasurementPrecision::Medium,
        OutputFormat::Text,
        None,
        false,
    );

    let report = checker.generate_entanglement_report();
    
    assert_eq!(report.node_a, "NodeA");
    assert_eq!(report.node_b, "NodeB");
    assert_eq!(report.verification_mode, "Quantum");
    assert!(report.correlation_coefficient >= 0.0 && report.correlation_coefficient <= 1.0);
    assert!(report.bell_inequality_violation >= 0.0 && report.bell_inequality_violation <= 4.0);
    assert!(report.quantum_correlations.len() > 0);
}

#[test]
fn test_classical_vs_quantum_correlation() {
    let classical_checker = QuantumChecker::new(
        "NodeA".to_string(),
        "NodeB".to_string(),
        VerificationMode::Classical,
        0.8,
        MeasurementPrecision::Medium,
        OutputFormat::Text,
        None,
        false,
    );

    let quantum_checker = QuantumChecker::new(
        "NodeA".to_string(),
        "NodeB".to_string(),
        VerificationMode::Quantum,
        0.8,
        MeasurementPrecision::Medium,
        OutputFormat::Text,
        None,
        false,
    );

    let classical_report = classical_checker.generate_entanglement_report();
    let quantum_report = quantum_checker.generate_entanglement_report();

    // Quantum mode should generally produce higher correlations
    assert!(quantum_report.correlation_coefficient >= classical_report.correlation_coefficient);
}

#[test]
fn test_measurement_precision() {
    let low_precision_checker = QuantumChecker::new(
        "NodeA".to_string(),
        "NodeB".to_string(),
        VerificationMode::Quantum,
        0.8,
        MeasurementPrecision::Low,
        OutputFormat::Text,
        None,
        false,
    );

    let high_precision_checker = QuantumChecker::new(
        "NodeA".to_string(),
        "NodeB".to_string(),
        VerificationMode::Quantum,
        0.8,
        MeasurementPrecision::High,
        OutputFormat::Text,
        None,
        false,
    );

    let low_report = low_precision_checker.generate_entanglement_report();
    let high_report = high_precision_checker.generate_entanglement_report();

    // High precision should have more measurements
    assert!(high_report.quantum_correlations.len() > low_report.quantum_correlations.len());
}

#[test]
fn test_bell_inequality_calculation() {
    let checker = QuantumChecker::new(
        "NodeA".to_string(),
        "NodeB".to_string(),
        VerificationMode::Quantum,
        0.8,
        MeasurementPrecision::Medium,
        OutputFormat::Text,
        None,
        false,
    );

    // Test with high correlation
    let high_violation = checker.calculate_bell_violation(0.95);
    assert!(high_violation > 2.0, "High correlation should violate Bell's inequality");

    // Test with low correlation
    let low_violation = checker.calculate_bell_violation(0.5);
    assert!(low_violation <= 2.0, "Low correlation should not violate Bell's inequality");
}

#[test]
fn test_quantum_state_generation() {
    let checker = QuantumChecker::new(
        "NodeA".to_string(),
        "NodeB".to_string(),
        VerificationMode::Quantum,
        0.8,
        MeasurementPrecision::Medium,
        OutputFormat::Text,
        None,
        false,
    );

    let state = checker.generate_quantum_state(0.9);
    assert!(state.contains("|ψ⟩"));
    assert!(state.contains("|00⟩"));
    assert!(state.contains("|11⟩"));
}

#[test]
fn test_entanglement_status() {
    let high_correlation_checker = QuantumChecker::new(
        "NodeA".to_string(),
        "NodeB".to_string(),
        VerificationMode::Quantum,
        0.8,
        MeasurementPrecision::Medium,
        OutputFormat::Text,
        None,
        false,
    );

    let low_correlation_checker = QuantumChecker::new(
        "NodeA".to_string(),
        "NodeB".to_string(),
        VerificationMode::Quantum,
        0.95, // High threshold
        MeasurementPrecision::Medium,
        OutputFormat::Text,
        None,
        false,
    );

    let high_report = high_correlation_checker.generate_entanglement_report();
    let low_report = low_correlation_checker.generate_entanglement_report();

    // With default threshold (0.8), high correlation should pass
    assert_eq!(high_report.entanglement_status, "✅ VERIFIED");
    
    // With high threshold (0.95), low correlation should fail
    assert_eq!(low_report.entanglement_status, "❌ NOT ENTANGLED");
}

#[test]
fn test_report_saving() {
    let temp_file = NamedTempFile::new().unwrap();
    let temp_path = temp_file.path().to_str().unwrap().to_string();

    let checker = QuantumChecker::new(
        "NodeA".to_string(),
        "NodeB".to_string(),
        VerificationMode::Quantum,
        0.8,
        MeasurementPrecision::Medium,
        OutputFormat::Text,
        Some(temp_path.clone()),
        false,
    );

    let report = checker.generate_entanglement_report();
    checker.save_report_to_file(&report, &temp_path).unwrap();

    // Verify file was created and contains expected content
    let content = fs::read_to_string(&temp_path).unwrap();
    assert!(content.contains("Quantum Entanglement Verification Report"));
    assert!(content.contains("Node A: NodeA"));
    assert!(content.contains("Node B: NodeB"));
}

#[test]
fn test_json_output() {
    let checker = QuantumChecker::new(
        "NodeA".to_string(),
        "NodeB".to_string(),
        VerificationMode::Quantum,
        0.8,
        MeasurementPrecision::Medium,
        OutputFormat::Json,
        None,
        false,
    );

    let report = checker.generate_entanglement_report();
    let json_output = serde_json::to_string_pretty(&report).unwrap();
    
    assert!(json_output.contains("node_a"));
    assert!(json_output.contains("node_b"));
    assert!(json_output.contains("correlation_coefficient"));
}

#[test]
fn test_yaml_output() {
    let checker = QuantumChecker::new(
        "NodeA".to_string(),
        "NodeB".to_string(),
        VerificationMode::Quantum,
        0.8,
        MeasurementPrecision::Medium,
        OutputFormat::Yaml,
        None,
        false,
    );

    let report = checker.generate_entanglement_report();
    let yaml_output = serde_yaml::to_string(&report).unwrap();
    
    assert!(yaml_output.contains("node_a:"));
    assert!(yaml_output.contains("node_b:"));
    assert!(yaml_output.contains("correlation_coefficient:"));
}

#[test]
fn test_argument_parsing() {
    // Test verification mode parsing
    assert!(parse_verification_mode("quantum").is_ok());
    assert!(parse_verification_mode("classical").is_ok());
    assert!(parse_verification_mode("invalid").is_err());

    // Test measurement precision parsing
    assert!(parse_measurement_precision("high").is_ok());
    assert!(parse_measurement_precision("medium").is_ok());
    assert!(parse_measurement_precision("low").is_ok());
    assert!(parse_measurement_precision("invalid").is_err());

    // Test output format parsing
    assert!(parse_output_format("text").is_ok());
    assert!(parse_output_format("json").is_ok());
    assert!(parse_output_format("yaml").is_ok());
    assert!(parse_output_format("invalid").is_err());
}
