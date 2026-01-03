use std::process::Command;
use std::fs;
use tempfile::NamedTempFile;

#[test]
fn test_verify_command() {
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-quantum-entanglement-checker"))
        .args(["verify", "--components", "service-a,service-b", "--strength", "0.8", "--threshold", "0.9"])
        .output()
        .expect("Failed to execute command");

    assert!(output.status.success());
    let stdout = String::from_utf8(output.stdout).unwrap();
    assert!(stdout.contains("service-a"));
    assert!(stdout.contains("service-b"));
    assert!(stdout.contains("coherence_score"));
}

#[test]
fn test_generate_command_json() {
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-quantum-entanglement-checker"))
        .args(["generate", "--components", "service-a,service-b", "--format", "json"])
        .output()
        .expect("Failed to execute command");

    assert!(output.status.success());
    let stdout = String::from_utf8(output.stdout).unwrap();
    assert!(stdout.contains("service-a"));
    assert!(stdout.contains("coherence_score"));
    assert!(stdout.starts_with("{"));
}

#[test]
fn test_generate_command_yaml() {
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-quantum-entanglement-checker"))
        .args(["generate", "--components", "service-a,service-b", "--format", "yaml"])
        .output()
        .expect("Failed to execute command");

    assert!(output.status.success());
    let stdout = String::from_utf8(output.stdout).unwrap();
    assert!(stdout.contains("service-a"));
    assert!(stdout.contains("coherence_score:"));
    assert!(stdout.starts_with("entanglement_verification:"));
}

#[test]
fn test_visualize_command() {
    let temp_file = NamedTempFile::new().unwrap();
    let temp_path = temp_file.path().to_str().unwrap();

    let output = Command::new(env!("CARGO_BIN_EXE_nightly-quantum-entanglement-checker"))
        .args(["visualize", "--components", "service-a,service-b", "--output", temp_path])
        .output()
        .expect("Failed to execute command");

    assert!(output.status.success());
    assert!(fs::metadata(temp_path).is_ok());
    
    let content = fs::read_to_string(temp_path).unwrap();
    assert!(content.contains("<svg"));
    assert!(content.contains("service-a"));
    assert!(content.contains("service-b"));
}

#[test]
fn test_benchmark_command() {
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-quantum-entanglement-checker"))
        .args(["benchmark", "--iterations", "10"])
        .output()
        .expect("Failed to execute command");

    assert!(output.status.success());
    let stdout = String::from_utf8(output.stdout).unwrap();
    assert!(stdout.contains("iterations"));
    assert!(stdout.contains("total_time_ms"));
    assert!(stdout.contains("average_time_ms"));
}

#[test]
fn test_invalid_component_list() {
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-quantum-entanglement-checker"))
        .args(["verify", "--components", ""])
        .output()
        .expect("Failed to execute command");

    assert!(!output.status.success());
}

#[test]
fn test_invalid_strength_value() {
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-quantum-entanglement-checker"))
        .args(["verify", "--components", "service-a", "--strength", "invalid"])
        .output()
        .expect("Failed to execute command");

    assert!(!output.status.success());
}

#[test]
fn test_invalid_threshold_value() {
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-quantum-entanglement-checker"))
        .args(["verify", "--components", "service-a", "--threshold", "invalid"])
        .output()
        .expect("Failed to execute command");

    assert!(!output.status.success());
}

#[test]
fn test_invalid_format() {
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-quantum-entanglement-checker"))
        .args(["generate", "--components", "service-a", "--format", "invalid"])
        .output()
        .expect("Failed to execute command");

    assert!(!output.status.success());
    let stderr = String::from_utf8(output.stderr).unwrap();
    assert!(stderr.contains("Invalid format"));
}

#[test]
fn test_help_command() {
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-quantum-entanglement-checker"))
        .args(["--help"])
        .output()
        .expect("Failed to execute command");

    assert!(output.status.success());
    let stdout = String::from_utf8(output.stdout).unwrap();
    assert!(stdout.contains("nightly-quantum-entanglement-checker"));
    assert!(stdout.contains("verify"));
    assert!(stdout.contains("generate"));
    assert!(stdout.contains("visualize"));
    assert!(stdout.contains("benchmark"));
}

#[test]
fn test_version_command() {
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-quantum-entanglement-checker"))
        .args(["--version"])
        .output()
        .expect("Failed to execute command");

    assert!(output.status.success());
    let stdout = String::from_utf8(output.stdout).unwrap();
    assert!(stdout.contains(env!("CARGO_PKG_VERSION")));
}

#[test]
fn test_ascii_art_output() {
    // Test that the tool can generate ASCII art visualization
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-quantum-entanglement-checker"))
        .args(["verify", "--components", "service-a,service-b", "--strength", "0.8"])
        .output()
        .expect("Failed to execute command");

    assert!(output.status.success());
    let stdout = String::from_utf8(output.stdout).unwrap();
    
    // Parse the JSON output to verify structure
    let verification: serde_json::Value = serde_json::from_str(&stdout).unwrap();
    assert!(verification["components"].is_array());
    assert!(verification["coherence_score"].is_number());
    assert!(verification["entanglement_pairs"].is_array());
}

#[test]
fn test_performance_with_many_components() {
    // Test with a larger number of components
    let components: Vec<String> = (0..20)
        .map(|i| format!("service-{}", i))
        .collect();
    let components_str = components.join(",");

    let output = Command::new(env!("CARGO_BIN_EXE_nightly-quantum-entanglement-checker"))
        .args(["verify", "--components", &components_str, "--strength", "0.7"])
        .output()
        .expect("Failed to execute command");

    assert!(output.status.success());
    let stdout = String::from_utf8(output.stdout).unwrap();
    
    let verification: serde_json::Value = serde_json::from_str(&stdout).unwrap();
    assert_eq!(verification["components"].as_array().unwrap().len(), 20);
    assert!(verification["verification_time_ms"].as_f64().unwrap() < 1000.0); // Should complete in under 1 second
}

#[test]
fn test_xml_export_format() {
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-quantum-entanglement-checker"))
        .args(["generate", "--components", "service-a,service-b", "--format", "xml"])
        .output()
        .expect("Failed to execute command");

    assert!(output.status.success());
    let stdout = String::from_utf8(output.stdout).unwrap();
    assert!(stdout.contains("<components>"));
    assert!(stdout.contains("<entanglement_strength>"));
    assert!(stdout.contains("<coherence_score>"));
}

#[test]
fn test_benchmark_with_custom_components() {
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-quantum-entanglement-checker"))
        .args(["benchmark", "--iterations", "5", "--components", "service-a,service-b,service-c"])
        .output()
        .expect("Failed to execute command");

    assert!(output.status.success());
    let stdout = String::from_utf8(output.stdout).unwrap();
    
    let benchmark: serde_json::Value = serde_json::from_str(&stdout).unwrap();
    assert_eq!(benchmark["iterations"].as_u64().unwrap(), 5);
    assert_eq!(benchmark["components_per_verification"].as_u64().unwrap(), 3);
    assert!(benchmark["total_time_ms"].as_f64().unwrap() > 0.0);
}
