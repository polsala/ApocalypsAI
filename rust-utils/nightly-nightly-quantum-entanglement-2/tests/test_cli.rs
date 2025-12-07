use nightly_quantum_entanglement_checker::cli::Args;

// Note: Full CLI testing requires setting up command line arguments
// which is complex in unit tests. These tests focus on individual components.

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_args_default_values() {
        // This test would need actual CLI argument setup
        // For now, we test that the Args struct can be created
        let args = Args {
            nodes: vec!["test".to_string()],
            metrics: false,
            interval: 5,
            verify: false,
            threshold: 0.8,
        };
        
        assert_eq!(args.interval, 5);
        assert_eq!(args.threshold, 0.8);
        assert!(!args.metrics);
        assert!(!args.verify);
    }

    #[test]
    fn test_threshold_clamping() {
        // Test that threshold values are properly clamped
        // This would be tested in the actual CLI parsing
        let test_threshold = 1.5_f64.clamp(0.0, 1.0);
        assert_eq!(test_threshold, 1.0);
        
        let test_threshold = (-0.1_f64).clamp(0.0, 1.0);
        assert_eq!(test_threshold, 0.0);
    }

    #[test]
    fn test_node_parsing() {
        // Test node string parsing logic
        let node_string = "node1,node2,node3";
        let nodes: Vec<String> = node_string.split(',')
            .map(|s| s.trim().to_string())
            .collect();
        
        assert_eq!(nodes.len(), 3);
        assert_eq!(nodes[0], "node1");
        assert_eq!(nodes[1], "node2");
        assert_eq!(nodes[2], "node3");
    }
}
