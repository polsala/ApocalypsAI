use std::process::Command;
use std::time::{SystemTime, UNIX_EPOCH};

#[test]
fn test_help_output() {
    let output = Command::new("cargo")
        .args(&["run", "--bin", "nightly-quantum-quip-generator", "--", "--help"])
        .output()
        .expect("Failed to execute command");
    
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Quantum Quip Generator"));
    assert!(stdout.contains("--format"));
    assert!(stdout.contains("--help"));
}

#[test]
fn test_text_output() {
    let output = Command::new("cargo")
        .args(&["run", "--bin", "nightly-quantum-quip-generator"])
        .output()
        .expect("Failed to execute command");
    
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    
    // Check that output contains expected elements
    assert!(stdout.contains("🔮 Quantum Quip of the Moment:"));
    assert!(stdout.contains("📚 Explanation:"));
    assert!(stdout.contains("quantum"));
}

#[test]
fn test_json_output() {
    let output = Command::new("cargo")
        .args(&["run", "--bin", "nightly-quantum-quip-generator", "--", "--format", "json"])
        .output()
        .expect("Failed to execute command");
    
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    
    // Check JSON structure
    assert!(stdout.contains("{\"quip\":\""));
    assert!(stdout.contains("\",\"explanation\":\""));
    assert!(stdout.contains("\",\"timestamp\":"));
    assert!(stdout.contains("\",\"category\":\"quantum-computing\"}"));
}

#[test]
fn test_markdown_output() {
    let output = Command::new("cargo")
        .args(&["run", "--bin", "nightly-quantum-quip-generator", "--", "--format", "markdown"])
        .output()
        .expect("Failed to execute command");
    
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    
    // Check Markdown structure
    assert!(stdout.contains("# 🔮 Quantum Quip of the Moment"));
    assert!(stdout.contains("> "));
    assert!(stdout.contains("## 📚 Explanation"));
    assert!(stdout.contains("*Generated at "));
}

#[test]
fn test_output_consistency() {
    // Test that multiple runs produce valid output
    for _ in 0..5 {
        let output = Command::new("cargo")
            .args(&["run", "--bin", "nightly-quantum-quip-generator"])
            .output()
            .expect("Failed to execute command");
        
        assert!(output.status.success());
        let stdout = String::from_utf8_lossy(&output.stdout);
        assert!(stdout.contains("🔮 Quantum Quip of the Moment:"));
        assert!(stdout.contains("📚 Explanation:"));
    }
}

#[test]
fn test_json_timestamp_validity() {
    let output = Command::new("cargo")
        .args(&["run", "--bin", "nightly-quantum-quip-generator", "--", "--format", "json"])
        .output()
        .expect("Failed to execute command");
    
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    
    // Extract timestamp and verify it's reasonable
    let timestamp_start = stdout.find("\"timestamp\": ").unwrap() + 12;
    let timestamp_end = stdout[timestamp_start..].find(",").unwrap() + timestamp_start;
    let timestamp_str = &stdout[timestamp_start..timestamp_end];
    let timestamp: u64 = timestamp_str.parse().expect("Invalid timestamp");
    
    let current_time = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_secs();
    
    // Timestamp should be recent (within last hour)
    assert!(current_time - timestamp < 3600);
}

#[test]
fn test_different_outputs() {
    // Test that we get different jokes on multiple runs
    let mut jokes = Vec::new();
    
    for _ in 0..10 {
        let output = Command::new("cargo")
            .args(&["run", "--bin", "nightly-quantum-quip-generator"])
            .output()
            .expect("Failed to execute command");
        
        assert!(output.status.success());
        let stdout = String::from_utf8_lossy(&output.stdout);
        
        // Extract the joke line
        let joke_start = stdout.find("\n").unwrap() + 1;
        let joke_end = stdout[joke_start..].find("\n").unwrap() + joke_start;
        let joke = stdout[joke_start..joke_end].trim().to_string();
        
        jokes.push(joke);
    }
    
    // We should have at least 2 different jokes in 10 attempts
    let unique_jokes: std::collections::HashSet<_> = jokes.iter().collect();
    assert!(unique_jokes.len() >= 2, "Expected at least 2 different jokes, got {:?}", unique_jokes);
}

#[test]
fn test_no_secrets_in_output() {
    let output = Command::new("cargo")
        .args(&["run", "--bin", "nightly-quantum-quip-generator"])
        .output()
        .expect("Failed to execute command");
    
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    let stderr = String::from_utf8_lossy(&output.stderr);
    
    // Check that no secrets or sensitive information is leaked
    let sensitive_patterns = vec![
        "password",
        "secret",
        "key",
        "token",
        "auth",
        "credential",
    ];
    
    for pattern in sensitive_patterns {
        assert!(!stdout.to_lowercase().contains(pattern), "Found sensitive pattern '{}' in stdout", pattern);
        assert!(!stderr.to_lowercase().contains(pattern), "Found sensitive pattern '{}' in stderr", pattern);
    }
}

#[test]
fn test_execution_time() {
    use std::time::Instant;
    
    let start = Instant::now();
    
    let output = Command::new("cargo")
        .args(&["run", "--bin", "nightly-quantum-quip-generator"])
        .output()
        .expect("Failed to execute command");
    
    let duration = start.elapsed();
    
    assert!(output.status.success());
    assert!(duration.as_secs() < 5, "Execution took too long: {:?}", duration);
}

#[test]
fn test_json_category_field() {
    let output = Command::new("cargo")
        .args(&["run", "--bin", "nightly-quantum-quip-generator", "--", "--format", "json"])
        .output()
        .expect("Failed to execute command");
    
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    
    assert!(stdout.contains("\"category\":\"quantum-computing\""));
}
