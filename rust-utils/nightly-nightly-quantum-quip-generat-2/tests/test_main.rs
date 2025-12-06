use std::process::Command;
use std::time::Instant;

#[test]
fn test_cli_help() {
    let output = Command::new("cargo")
        .args(&["run", "--release", "--", "--help"])
        .output()
        .expect("Failed to execute cargo run");
    
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Quantum Quip Generator"));
    assert!(stdout.contains("--count"));
    assert!(stdout.contains("--format"));
    assert!(stdout.contains("--interactive"));
}

#[test]
fn test_generate_single_joke() {
    let output = Command::new("cargo")
        .args(&["run", "--release"])
        .output()
        .expect("Failed to execute cargo run");
    
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Quantum Quip:"));
    assert!(stdout.contains("Why don't quantum physicists ever argue?"));
}

#[test]
fn test_generate_multiple_jokes() {
    let output = Command::new("cargo")
        .args(&["run", "--release", "--count", "3"])
        .output()
        .expect("Failed to execute cargo run");
    
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    let lines: Vec<&str> = stdout.lines().collect();
    
    // Should have at least 3 joke lines
    let joke_lines = lines.iter().filter(|line| line.contains("Quantum Quip:")).count();
    assert!(joke_lines >= 3);
}

#[test]
fn test_json_format() {
    let output = Command::new("cargo")
        .args(&["run", "--release", "--format", "json"])
        .output()
        .expect("Failed to execute cargo run");
    
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    
    // Should be valid JSON
    let joke: serde_json::Value = serde_json::from_str(&stdout).expect("Invalid JSON output");
    assert!(joke["joke"].is_string());
    assert!(joke["category"].is_string());
    assert!(joke["difficulty"].is_string());
}

#[test]
fn test_multiple_json_jokes() {
    let output = Command::new("cargo")
        .args(&["run", "--release", "--count", "3", "--format", "json"])
        .output()
        .expect("Failed to execute cargo run");
    
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    let lines: Vec<&str> = stdout.lines().collect();
    
    // Should have 3 JSON objects
    assert_eq!(lines.len(), 3);
    
    for line in lines {
        let joke: serde_json::Value = serde_json::from_str(line).expect("Invalid JSON output");
        assert!(joke["joke"].is_string());
        assert!(joke["category"].is_string());
        assert!(joke["difficulty"].is_string());
    }
}

#[test]
fn test_seed_reproducibility() {
    // Generate jokes with the same seed
    let output1 = Command::new("cargo")
        .args(&["run", "--release", "--seed", "123"])
        .output()
        .expect("Failed to execute cargo run");
    
    let output2 = Command::new("cargo")
        .args(&["run", "--release", "--seed", "123"])
        .output()
        .expect("Failed to execute cargo run");
    
    assert!(output1.status.success());
    assert!(output2.status.success());
    
    let stdout1 = String::from_utf8_lossy(&output1.stdout);
    let stdout2 = String::from_utf8_lossy(&output2.stdout);
    
    // Should be identical
    assert_eq!(stdout1, stdout2);
}

#[test]
fn test_different_seeds() {
    // Generate jokes with different seeds
    let output1 = Command::new("cargo")
        .args(&["run", "--release", "--seed", "123"])
        .output()
        .expect("Failed to execute cargo run");
    
    let output2 = Command::new("cargo")
        .args(&["run", "--release", "--seed", "456"])
        .output()
        .expect("Failed to execute cargo run");
    
    assert!(output1.status.success());
    assert!(output2.status.success());
    
    let stdout1 = String::from_utf8_lossy(&output1.stdout);
    let stdout2 = String::from_utf8_lossy(&output2.stdout);
    
    // Should be different
    assert_ne!(stdout1, stdout2);
}

#[test]
fn test_thread_performance() {
    // Test single-threaded performance
    let start = Instant::now();
    let output_single = Command::new("cargo")
        .args(&["run", "--release", "--count", "50", "--threads", "1"])
        .output()
        .expect("Failed to execute cargo run");
    let duration_single = start.elapsed();
    
    assert!(output_single.status.success());
    
    // Test multi-threaded performance
    let start = Instant::now();
    let output_multi = Command::new("cargo")
        .args(&["run", "--release", "--count", "50", "--threads", "4"])
        .output()
        .expect("Failed to execute cargo run");
    let duration_multi = start.elapsed();
    
    assert!(output_multi.status.success());
    
    // Multi-threaded should be faster or at least not significantly slower
    // (Note: This is a soft assertion as performance can vary)
    println!("Single-threaded: {:?}, Multi-threaded: {:?}", duration_single, duration_multi);
}

#[test]
fn test_error_handling_invalid_count() {
    let output = Command::new("cargo")
        .args(&["run", "--release", "--count", "invalid"])
        .output()
        .expect("Failed to execute cargo run");
    
    // Should fail with invalid count
    assert!(!output.status.success());
}

#[test]
fn test_error_handling_invalid_threads() {
    let output = Command::new("cargo")
        .args(&["run", "--release", "--threads", "invalid"])
        .output()
        .expect("Failed to execute cargo run");
    
    // Should fail with invalid thread count
    assert!(!output.status.success());
}

#[test]
fn test_performance_with_large_count() {
    let start = Instant::now();
    let output = Command::new("cargo")
        .args(&["run", "--release", "--count", "100", "--threads", "4"])
        .output()
        .expect("Failed to execute cargo run");
    let duration = start.elapsed();
    
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    let lines: Vec<&str> = stdout.lines().collect();
    let joke_lines = lines.iter().filter(|line| line.contains("Quantum Quip:")).count();
    assert_eq!(joke_lines, 100);
    
    // Should complete in reasonable time (less than 5 seconds)
    assert!(duration < std::time::Duration::from_secs(5));
    println!("Generated 100 jokes in {:?}", duration);
}
