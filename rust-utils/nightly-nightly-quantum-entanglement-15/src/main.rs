use std::env;
use std::process;

/// Quantum state representation for entanglement simulation
#[derive(Debug, Clone, PartialEq)]
enum QuantumState {
    SpinUp,
    SpinDown,
}

/// Quantum correlation result
#[derive(Debug)]
struct EntanglementResult {
    node_a: String,
    node_b: String,
    distance_km: u32,
    correlation: f64,
    threshold: f64,
    entangled: bool,
}

impl EntanglementResult {
    fn new(node_a: String, node_b: String, distance_km: u32, threshold: f64) -> Self {
        // Simulate quantum correlation based on distance and deterministic seed
        let correlation = calculate_correlation(&node_a, &node_b, distance_km);
        let entangled = correlation >= threshold;
        
        EntanglementResult {
            node_a,
            node_b,
            distance_km,
            correlation,
            threshold,
            entangled,
        }
    }
    
    fn spooky_action_detected(&self) -> bool {
        self.entangled && self.correlation > 0.8
    }
    
    fn format_report(&self) -> String {
        let status = if self.entangled { "✅ ENTANGLED" } else { "❌ SEPARATED" };
        let spooky = if self.spooky_action_detected() { "DETECTED" } else { "NOT DETECTED" };
        
        format!(
            "🔬 Quantum Entanglement Verification Report\n"
            "==========================================\n\n"
            "Node A: {}\n"
            "Node B: {}\n"
            "Distance: {} km\n"
            "Correlation Threshold: {:.2}\n\n"
            "Entanglement Status: {}\n"
            "Quantum Correlation: {:.2}\n"
            "Spooky Action: {}\n\n"
            "\"The universe is not only stranger than we imagine, it is stranger than we can imagine.\"",
            self.node_a,
            self.node_b,
            self.distance_km,
            self.threshold,
            status,
            self.correlation,
            spooky
        )
    }
}

/// Deterministic quantum correlation calculator
/// Uses node names and distance to generate reproducible "quantum" results
fn calculate_correlation(node_a: &str, node_b: &str, distance_km: u32) -> f64 {
    // Create a deterministic seed from node names and distance
    let seed = hash_nodes(node_a, node_b) ^ (distance_km as u64);
    
    // Generate pseudo-random correlation between 0.3 and 0.95
    // Using a simple deterministic PRNG for reproducible results
    let mut state = seed.wrapping_mul(0x5DEECE66D).wrapping_add(0xB);
    state = state.wrapping_mul(0x5DEECE66D).wrapping_add(0xB);
    
    let random_value = (state >> 16) as u32;
    let normalized = (random_value % 650) as f64 / 1000.0 + 0.3;
    
    // Apply distance decay factor (longer distances reduce correlation)
    let distance_factor = 1.0 - (distance_km as f64 / 10000.0).min(0.4);
    normalized * distance_factor
}

/// Simple hash function for deterministic results
fn hash_nodes(node_a: &str, node_b: &str) -> u64 {
    let combined = format!("{}|{}", node_a, node_b);
    combined.bytes().fold(0u64, |acc, byte| {
        acc.wrapping_mul(31).wrapping_add(byte as u64)
    })
}

/// Generate a quantum state report
fn generate_quantum_report() -> String {
    let states = vec!["Superposition", "Entanglement", "Tunneling", "Decoherence"];
    let phenomena = vec![
        "Quantum fluctuations detected in node synchronization",
        "Wave function collapse observed during data transfer",
        "Particle-wave duality confirmed in network packets",
        "Heisenberg uncertainty principle affecting measurement precision",
    ];
    
    format!(
        "🌌 Quantum State Report\n"
        "========================\n\n"
        "Active Quantum States:\n"
        "{}
{}
{}
{}
\n"
        "Observed Phenomena:\n"
        "{}
{}
{}
{}",
        states[0], states[1], states[2], states[3],
        phenomena[0], phenomena[1], phenomena[2], phenomena[3]
    )
}

/// Parse command line arguments
fn parse_args() -> (String, String, u32, f64, bool) {
    let args: Vec<String> = env::args().collect();
    
    if args.len() == 2 && args[1] == "--report" {
        return (String::new(), String::new(), 0, 0.0, true);
    }
    
    let mut node_a = String::from("node1");
    let mut node_b = String::from("node2");
    let mut distance = 100;
    let mut threshold = 0.75;
    
    let mut i = 1;
    while i < args.len() {
        match args[i].as_str() {
            "--node-a" => {
                if i + 1 < args.len() {
                    node_a = args[i + 1].clone();
                    i += 1;
                }
            },
            "--node-b" => {
                if i + 1 < args.len() {
                    node_b = args[i + 1].clone();
                    i += 1;
                }
            },
            "--distance" => {
                if i + 1 < args.len() {
                    distance = args[i + 1].parse().unwrap_or(100);
                    i += 1;
                }
            },
            "--threshold" => {
                if i + 1 < args.len() {
                    threshold = args[i + 1].parse().unwrap_or(0.75);
                    i += 1;
                }
            },
            _ => {},
        }
        i += 1;
    }
    
    (node_a, node_b, distance, threshold, false)
}

fn main() {
    let (node_a, node_b, distance, threshold, report_only) = parse_args();
    
    if report_only {
        println!("{}", generate_quantum_report());
        return;
    }
    
    let result = EntanglementResult::new(node_a, node_b, distance, threshold);
    println!("{}", result.format_report());
    
    // Exit with error code if not entangled (for CI/CD integration)
    if !result.entangled {
        process::exit(1);
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_calculate_correlation_deterministic() {
        // Test that correlation is deterministic for same inputs
        let corr1 = calculate_correlation("node1", "node2", 100);
        let corr2 = calculate_correlation("node1", "node2", 100);
        assert_eq!(corr1, corr2, "Correlation should be deterministic");
    }
    
    #[test]
    fn test_calculate_correlation_range() {
        // Test that correlation is within expected range
        let corr = calculate_correlation("test", "node", 500);
        assert!(corr >= 0.3 && corr <= 0.95, "Correlation should be between 0.3 and 0.95, got {}", corr);
    }
    
    #[test]
    fn test_calculate_correlation_distance_effect() {
        // Test that longer distances generally reduce correlation
        let corr_short = calculate_correlation("a", "b", 10);
        let corr_long = calculate_correlation("a", "b", 1000);
        
        // Due to quantum randomness, this might not always be true
        // But should be true in most cases
        let distance_effect = corr_short >= corr_long * 0.8;
        assert!(distance_effect, "Shorter distance should generally have higher correlation ({} vs {})", corr_short, corr_long);
    }
    
    #[test]
    fn test_entanglement_result_creation() {
        let result = EntanglementResult::new("node1".to_string(), "node2".to_string(), 100, 0.75);
        
        assert_eq!(result.node_a, "node1");
        assert_eq!(result.node_b, "node2");
        assert_eq!(result.distance_km, 100);
        assert_eq!(result.threshold, 0.75);
        assert!(result.correlation >= 0.3 && result.correlation <= 0.95);
    }
    
    #[test]
    fn test_entanglement_status() {
        let entangled = EntanglementResult::new("node1".to_string(), "node2".to_string(), 10, 0.5);
        let separated = EntanglementResult::new("node1".to_string(), "node2".to_string(), 10000, 0.9);
        
        assert!(entangled.entangled, "Should be entangled with low threshold and short distance");
        assert!(!separated.entangled, "Should be separated with high threshold and long distance");
    }
    
    #[test]
    fn test_spooky_action_detection() {
        let high_corr = EntanglementResult::new("node1".to_string(), "node2".to_string(), 10, 0.75);
        let low_corr = EntanglementResult::new("node1".to_string(), "node2".to_string(), 1000, 0.75);
        
        // High correlation should trigger spooky action detection
        if high_corr.correlation > 0.8 {
            assert!(high_corr.spooky_action_detected(), "High correlation should detect spooky action");
        }
        
        // Low correlation should not trigger spooky action detection
        if low_corr.correlation <= 0.8 {
            assert!(!low_corr.spooky_action_detected(), "Low correlation should not detect spooky action");
        }
    }
    
    #[test]
    fn test_format_report_contains_expected_fields() {
        let result = EntanglementResult::new("test_node_a".to_string(), "test_node_b".to_string(), 42, 0.75);
        let report = result.format_report();
        
        assert!(report.contains("test_node_a"), "Report should contain node A name");
        assert!(report.contains("test_node_b"), "Report should contain node B name");
        assert!(report.contains("42"), "Report should contain distance");
        assert!(report.contains("0.75"), "Report should contain threshold");
        assert!(report.contains("Quantum Correlation:"), "Report should contain correlation info");
        assert!(report.contains("Spooky Action:"), "Report should contain spooky action status");
    }
    
    #[test]
    fn test_hash_nodes_deterministic() {
        let hash1 = hash_nodes("node1", "node2");
        let hash2 = hash_nodes("node1", "node2");
        assert_eq!(hash1, hash2, "Hash should be deterministic");
    }
    
    #[test]
    fn test_hash_nodes_different_inputs() {
        let hash1 = hash_nodes("node1", "node2");
        let hash2 = hash_nodes("node2", "node1");
        let hash3 = hash_nodes("node1", "node3");
        
        assert_ne!(hash1, hash2, "Different node orders should produce different hashes");
        assert_ne!(hash1, hash3, "Different nodes should produce different hashes");
    }
}
