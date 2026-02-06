use nightly_quantum_entanglement_checker::*;

#[cfg(test)]
mod integration_tests {
    use super::*;
    use std::process::Command;
    use std::fs;
    
    #[test]
    fn test_cli_verify_command() {
        // Test that the CLI can run the verify command
        let output = Command::new("cargo")
            .args(&["run", "--bin", "nightly-quantum-entanglement-checker", "verify", "--measurements", "100"])
            .output()
            .expect("Failed to execute command");
        
        assert!(output.status.success());
        let stdout = String::from_utf8_lossy(&output.stdout);
        assert!(stdout.contains("Correlation:"));
        assert!(stdout.contains("CHSH Violation:"));
    }
    
    #[test]
    fn test_cli_network_command() {
        let output = Command::new("cargo")
            .args(&["run", "--bin", "nightly-quantum-entanglement-checker", "network", "--nodes", "3"])
            .output()
            .expect("Failed to execute command");
        
        assert!(output.status.success());
        let stdout = String::from_utf8_lossy(&output.stdout);
        assert!(stdout.contains("Decoherence Rate:"));
        assert!(stdout.contains("Fidelity:"));
    }
    
    #[test]
    fn test_cli_circuit_command() {
        let output = Command::new("cargo")
            .args(&["run", "--bin", "nightly-quantum-entanglement-checker", "circuit", "--bell-state", "psi-plus"])
            .output()
            .expect("Failed to execute command");
        
        assert!(output.status.success());
        let stdout = String::from_utf8_lossy(&output.stdout);
        assert!(stdout.contains("●"));
        assert!(stdout.contains("⊕"));
    }
    
    #[test]
    fn test_circuit_diagram_save() {
        let temp_file = "/tmp/test_circuit.txt";
        
        let output = Command::new("cargo")
            .args(&[
                "run", 
                "--bin", 
                "nightly-quantum-entanglement-checker", 
                "circuit", 
                "--save", temp_file
            ])
            .output()
            .expect("Failed to execute command");
        
        assert!(output.status.success());
        
        // Check that file was created
        assert!(fs::metadata(temp_file).is_ok());
        
        let content = fs::read_to_string(temp_file).expect("Failed to read file");
        assert!(content.contains("●"));
        
        // Clean up
        fs::remove_file(temp_file).expect("Failed to remove temp file");
    }
    
    #[test]
    fn test_performance_benchmark() {
        use std::time::Instant;
        
        let start = Instant::now();
        let _results = verify_entanglement(2, 10000, "phi-plus", 3);
        let duration = start.elapsed();
        
        // Should complete within reasonable time (less than 1 second)
        assert!(duration.as_secs() < 1);
        
        println!("Performance test: {:?} for 10,000 measurements", duration);
    }
    
    #[test]
    fn test_statistical_consistency() {
        // Run multiple verification tests and check consistency
        let mut correlations = Vec::new();
        let mut fidelities = Vec::new();
        
        for _ in 0..5 {
            let results = verify_entanglement(2, 1000, "phi-plus", 3);
            correlations.push(results.correlation);
            fidelities.push(results.fidelity);
        }
        
        // Check that results are reasonably consistent
        let avg_correlation: f64 = correlations.iter().sum::<f64>() / correlations.len() as f64;
        let avg_fidelity: f64 = fidelities.iter().sum::<f64>() / fidelities.len() as f64;
        
        assert!(avg_correlation > 0.8); // Should be highly correlated
        assert!(avg_fidelity > 0.8);    // Should have high fidelity
        
        // Check variance is reasonable
        let correlation_variance: f64 = correlations.iter()
            .map(|&c| (c - avg_correlation).powi(2))
            .sum::<f64>() / correlations.len() as f64;
        
        assert!(correlation_variance < 0.1); // Variance should be small
    }
    
    #[test]
    fn test_network_scaling() {
        // Test that network simulation scales reasonably
        let nodes_list = vec![2, 4, 8, 16];
        let mut times = Vec::new();
        
        for nodes in nodes_list {
            let start = Instant::now();
            let _results = simulate_network_entanglement(nodes, 100.0, 0.001, "direct");
            times.push(start.elapsed());
        }
        
        // Times should generally increase but remain reasonable
        for time in &times {
            assert!(time.as_secs() < 1);
        }
    }
}
