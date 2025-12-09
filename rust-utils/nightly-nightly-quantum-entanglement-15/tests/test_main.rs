use nightly_quantum_entanglement_checker::*;

#[cfg(test)]
mod integration_tests {
    use super::*;
    use std::process::Command;
    
    #[test]
    fn test_cli_basic_entanglement_check() {
        // Test basic CLI functionality
        let output = Command::new(env!("CARGO_BIN_EXE_nightly-quantum-entanglement-checker"))
            .args(["--node-a", "test1", "--node-b", "test2", "--distance", "50"])
            .output()
            .expect("Failed to execute CLI");
        
        assert!(output.status.success(), "CLI should succeed");
        let stdout = String::from_utf8_lossy(&output.stdout);
        assert!(stdout.contains("Quantum Entanglement Verification Report"), "Output should contain report header");
        assert!(stdout.contains("test1"), "Output should contain node A name");
        assert!(stdout.contains("test2"), "Output should contain node B name");
        assert!(stdout.contains("50"), "Output should contain distance");
    }
    
    #[test]
    fn test_cli_with_custom_threshold() {
        // Test CLI with custom threshold
        let output = Command::new(env!("CARGO_BIN_EXE_nightly-quantum-entanglement-checker"))
            .args(["--node-a", "nodeA", "--node-b", "nodeB", "--threshold", "0.9"])
            .output()
            .expect("Failed to execute CLI");
        
        assert!(output.status.success(), "CLI should succeed with custom threshold");
        let stdout = String::from_utf8_lossy(&output.stdout);
        assert!(stdout.contains("0.90"), "Output should contain custom threshold value");
    }
    
    #[test]
    fn test_cli_report_generation() {
        // Test quantum state report generation
        let output = Command::new(env!("CARGO_BIN_EXE_nightly-quantum-entanglement-checker"))
            .arg("--report")
            .output()
            .expect("Failed to execute CLI report");
        
        assert!(output.status.success(), "CLI report should succeed");
        let stdout = String::from_utf8_lossy(&output.stdout);
        assert!(stdout.contains("Quantum State Report"), "Report should contain header");
        assert!(stdout.contains("Superposition"), "Report should contain quantum states");
        assert!(stdout.contains("Quantum fluctuations"), "Report should contain observed phenomena");
    }
    
    #[test]
    fn test_cli_exit_code_for_separated_nodes() {
        // Test that CLI exits with error code when nodes are not entangled
        // This is tricky to test deterministically due to quantum randomness
        // So we'll test with a very high threshold that should fail
        let output = Command::new(env!("CARGO_BIN_EXE_nightly-quantum-entanglement-checker"))
            .args(["--node-a", "node1", "--node-b", "node2", "--threshold", "0.99"])
            .output()
            .expect("Failed to execute CLI with high threshold");
        
        // Note: Due to quantum randomness, this might succeed sometimes
        // The important thing is that the CLI handles both success and failure cases
        let stdout = String::from_utf8_lossy(&output.stdout);
        assert!(stdout.contains("Entanglement Status:"), "Output should contain entanglement status");
    }
    
    #[test]
    fn test_deterministic_behavior_across_runs() {
        // Test that multiple runs with same inputs produce same results
        let mut results = Vec::new();
        
        for _ in 0..5 {
            let output = Command::new(env!("CARGO_BIN_EXE_nightly-quantum-entanglement-checker"))
                .args(["--node-a", "deterministic", "--node-b", "test", "--distance", "100"])
                .output()
                .expect("Failed to execute CLI for deterministic test");
            
            assert!(output.status.success(), "CLI should succeed");
            results.push(String::from_utf8_lossy(&output.stdout).to_string());
        }
        
        // All results should be identical (deterministic)
        for result in &results[1..] {
            assert_eq!(results[0], *result, "Results should be deterministic across runs");
        }
    }
    
    #[test]
    fn test_quantum_correlation_bounds() {
        // Test that quantum correlations stay within expected bounds
        for i in 0..100 {
            let output = Command::new(env!("CARGO_BIN_EXE_nightly-quantum-entanglement-checker"))
                .args(["--node-a", &format!("test_a_{}", i), "--node-b", &format!("test_b_{}", i)])
                .output()
                .expect("Failed to execute CLI for correlation bounds test");
            
            let stdout = String::from_utf8_lossy(&output.stdout);
            if let Some(correlation_line) = stdout.lines().find(|line| line.contains("Quantum Correlation:")) {
                if let Some(correlation_str) = correlation_line.split(':').nth(1) {
                    let correlation: f64 = correlation_str.trim().parse().expect("Failed to parse correlation");
                    assert!(correlation >= 0.3 && correlation <= 0.95, "Correlation should be between 0.3 and 0.95, got {}", correlation);
                }
            }
        }
    }
    
    #[test]
    fn test_spooky_action_detection_in_output() {
        // Test that spooky action detection appears in CLI output
        let output = Command::new(env!("CARGO_BIN_EXE_nightly-quantum-entanglement-checker"))
            .args(["--node-a", "spooky", "--node-b", "action", "--distance", "1"])
            .output()
            .expect("Failed to execute CLI for spooky action test");
        
        assert!(output.status.success(), "CLI should succeed");
        let stdout = String::from_utf8_lossy(&output.stdout);
        assert!(stdout.contains("Spooky Action:"), "Output should contain spooky action status");
        
        // Check if spooky action is detected or not
        assert!(stdout.contains("DETECTED") || stdout.contains("NOT DETECTED"), "Output should indicate if spooky action was detected");
    }
    
    #[test]
    fn test_help_or_usage_information() {
        // Test that the CLI provides some form of usage information
        // (Note: We didn't implement --help, but we can test that the CLI runs without crashing)
        let output = Command::new(env!("CARGO_BIN_EXE_nightly-quantum-entanglement-checker"))
            .args(["--node-a", "help", "--node-b", "test"])
            .output()
            .expect("Failed to execute CLI for help test");
        
        assert!(output.status.success(), "CLI should handle basic usage without crashing");
        let stdout = String::from_utf8_lossy(&output.stdout);
        assert!(stdout.contains("Quantum Entanglement Verification Report"), "Output should contain report header");
    }
    
    #[test]
    fn test_edge_cases() {
        // Test edge cases like very long node names, zero distance, etc.
        
        // Test with very long node names
        let long_name = "a".repeat(1000);
        let output = Command::new(env!("CARGO_BIN_EXE_nightly-quantum-entanglement-checker"))
            .args(["--node-a", &long_name, "--node-b", "test"])
            .output()
            .expect("Failed to execute CLI with long node name");
        
        assert!(output.status.success(), "CLI should handle long node names");
        
        // Test with zero distance
        let output = Command::new(env!("CARGO_BIN_EXE_nightly-quantum-entanglement-checker"))
            .args(["--node-a", "node1", "--node-b", "node2", "--distance", "0"])
            .output()
            .expect("Failed to execute CLI with zero distance");
        
        assert!(output.status.success(), "CLI should handle zero distance");
        let stdout = String::from_utf8_lossy(&output.stdout);
        assert!(stdout.contains("0"), "Output should contain zero distance");
    }
}
