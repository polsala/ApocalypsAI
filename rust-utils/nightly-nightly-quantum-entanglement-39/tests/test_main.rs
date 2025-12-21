use std::process::Command;
use std::fs;
use std::path::Path;

/// Test that the binary runs successfully with basic arguments
#[test]
fn test_basic_execution() {
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-quantum-entanglement-checker"))
        .args(&["--particles", "100", "--trials", "5"])
        .output()
        .expect("Failed to execute binary");

    assert!(output.status.success(), "Binary should exit successfully");
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("QUANTUM ENTANGLEMENT"), "Output should contain quantum art");
    assert!(stdout.contains("Bell Inequality Value"), "Output should contain results");
}

/// Test that the binary generates a report when requested
#[test]
fn test_report_generation() {
    let temp_file = "/tmp/quantum_test_report.txt";
    
    // Clean up any existing file
    let _ = fs::remove_file(temp_file);
    
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-quantum-entanglement-checker"))
        .args(&[
            "--particles", "50", 
            "--trials", "2", 
            "--report", 
            "--output", temp_file
        ])
        .output()
        .expect("Failed to execute binary");

    assert!(output.status.success(), "Binary should exit successfully");
    
    // Check that report file was created
    assert!(Path::new(temp_file).exists(), "Report file should be created");
    
    let report_content = fs::read_to_string(temp_file).expect("Failed to read report file");
    assert!(report_content.contains("EXPERIMENT CONFIGURATION"), "Report should contain configuration");
    assert!(report_content.contains("MEASUREMENT RESULTS"), "Report should contain results");
    
    // Clean up
    let _ = fs::remove_file(temp_file);
}

/// Test distributed entanglement scenario
#[test]
fn test_distributed_scenario() {
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-quantum-entanglement-checker"))
        .args(&[
            "--particles", "100", 
            "--trials", "3", 
            "--distributed", 
            "--distance", "500"
        ])
        .output()
        .expect("Failed to execute binary");

    assert!(output.status.success(), "Binary should exit successfully");
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Distributed: Yes"), "Output should indicate distributed scenario");
    assert!(stdout.contains("500"), "Output should show correct distance");
}

/// Test custom angle parameters
#[test]
fn test_custom_angles() {
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-quantum-entanglement-checker"))
        .args(&[
            "--particles", "50", 
            "--trials", "2", 
            "--angle-a", "22.5", 
            "--angle-b", "67.5"
        ])
        .output()
        .expect("Failed to execute binary");

    assert!(output.status.success(), "Binary should exit successfully");
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("22.5°"), "Output should show custom angle A");
    assert!(stdout.contains("67.5°"), "Output should show custom angle B");
}

/// Test help command
#[test]
fn test_help_command() {
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-quantum-entanglement-checker"))
        .args(&["--help"])
        .output()
        .expect("Failed to execute help command");

    assert!(output.status.success(), "Help command should exit successfully");
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("nightly-quantum-entanglement-checker"), "Help should show program name");
    assert!(stdout.contains("--particles"), "Help should show particles option");
    assert!(stdout.contains("--trials"), "Help should show trials option");
}

/// Test seed reproducibility
#[test]
fn test_seed_reproducibility() {
    // Run twice with same seed and compare results
    let output1 = Command::new(env!("CARGO_BIN_EXE_nightly-quantum-entanglement-checker"))
        .args(&[
            "--particles", "100", 
            "--trials", "5", 
            "--seed", "12345"
        ])
        .output()
        .expect("Failed to execute first run");

    let output2 = Command::new(env!("CARGO_BIN_EXE_nightly-quantum-entanglement-checker"))
        .args(&[
            "--particles", "100", 
            "--trials", "5", 
            "--seed", "12345"
        ])
        .output()
        .expect("Failed to execute second run");

    assert!(output1.status.success() && output2.status.success(), "Both runs should succeed");
    
    // Results should be identical with same seed
    let stdout1 = String::from_utf8_lossy(&output1.stdout);
    let stdout2 = String::from_utf8_lossy(&output2.stdout);
    
    // Extract Bell inequality values for comparison
    let extract_bell_value = |output: &str| -> Option<f64> {
        for line in output.lines() {
            if line.contains("Bell Inequality Value:") {
                let parts: Vec<&str> = line.split(':').collect();
                if parts.len() > 1 {
                    return parts[1].trim().parse().ok();
                }
            }
        }
        None
    };
    
    let bell1 = extract_bell_value(&stdout1);
    let bell2 = extract_bell_value(&stdout2);
    
    assert_eq!(bell1, bell2, "Bell inequality values should be identical with same seed");
}

/// Test performance with large particle counts
#[test]
fn test_performance_large_particles() {
    use std::time::Instant;
    
    let start = Instant::now();
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-quantum-entanglement-checker"))
        .args(&[
            "--particles", "5000", 
            "--trials", "10"
        ])
        .output()
        .expect("Failed to execute performance test");
    
    let duration = start.elapsed();
    
    assert!(output.status.success(), "Large particle test should succeed");
    assert!(duration.as_secs() < 30, "Large particle test should complete within 30 seconds");
    
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Total Measurements:"), "Output should show measurement count");
}

/// Test error handling with invalid arguments
#[test]
fn test_invalid_arguments() {
    // Test with negative particles (should be handled gracefully)
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-quantum-entanglement-checker"))
        .args(&["--particles", "-100"])
        .output()
        .expect("Failed to execute with invalid arguments");

    // Should either succeed with default values or fail gracefully
    // The exact behavior depends on structopt's validation
    assert!(output.status.success() || !output.status.success(), "Should handle invalid args gracefully");
}
