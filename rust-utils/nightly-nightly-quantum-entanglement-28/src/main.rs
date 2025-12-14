use std::collections::HashMap;
use std::env;
use std::fs;
use std::path::Path;
use uuid::Uuid;

#[derive(Debug, Clone, PartialEq)]
enum QuantumState {
    Zero,
    One,
    Superposition,
}

impl QuantumState {
    fn to_string(&self) -> String {
        match self {
            QuantumState::Zero => "|0⟩".to_string(),
            QuantumState::One => "|1⟩".to_string(),
            QuantumState::Superposition => "|ψ⟩".to_string(),
        }
    }
}

#[derive(Debug, Clone)]
struct QuantumEntanglementPair {
    id: String,
    particle_a: QuantumState,
    particle_b: QuantumState,
    entanglement_strength: f32,
    coherence: String,
    timestamp: String,
}

impl QuantumEntanglementPair {
    fn new() -> Self {
        let id = format!("QEP-{}", Uuid::new_v4());
        let particle_a = QuantumState::Zero;
        let particle_b = QuantumState::One;
        let entanglement_strength = 90.0 + (rand::random::<f32>() * 10.0);
        let coherence = "Stable".to_string();
        let timestamp = chrono::Utc::now().to_rfc3339();

        QuantumEntanglementPair {
            id,
            particle_a,
            particle_b,
            entanglement_strength,
            coherence,
            timestamp,
        }
    }

    fn verify(&self) -> bool {
        // Quantum verification algorithm (whimsical)
        match (&self.particle_a, &self.particle_b) {
            (QuantumState::Zero, QuantumState::One) => true,
            (QuantumState::One, QuantumState::Zero) => true,
            _ => false,
        }
    }

    fn visualize(&self) -> String {
        format!(
            "Quantum Entanglement Visualization\n\n"
            "Pair ID: {}\n"
            "Particle A: {}\n"
            "Particle B: {}\n"
            "Entanglement Strength: {:.1}%\n"
            "Quantum Coherence: {}\n"
            "Timestamp: {}\n\n"
            "Spacetime Entanglement Status: ✓ CONNECTED\n",
            self.id,
            self.particle_a.to_string(),
            self.particle_b.to_string(),
            self.entanglement_strength,
            self.coherence,
            self.timestamp
        )
    }
}

struct QuantumEntanglementChecker {
    pairs: HashMap<String, QuantumEntanglementPair>,
    data_file: String,
}

impl QuantumEntanglementChecker {
    fn new() -> Self {
        let data_file = "quantum_pairs.json".to_string();
        let pairs = Self::load_pairs(&data_file);
        QuantumEntanglementChecker { pairs, data_file }
    }

    fn load_pairs(data_file: &str) -> HashMap<String, QuantumEntanglementPair> {
        if Path::new(data_file).exists() {
            match fs::read_to_string(data_file) {
                Ok(content) => {
                    match serde_json::from_str::<HashMap<String, QuantumEntanglementPair>>(&content) {
                        Ok(pairs) => pairs,
                        Err(_) => HashMap::new(),
                    }
                }
                Err(_) => HashMap::new(),
            }
        } else {
            HashMap::new()
        }
    }

    fn save_pairs(&self) {
        let content = serde_json::to_string_pretty(&self.pairs).unwrap_or_default();
        fs::write(&self.data_file, content).ok();
    }

    fn generate_pair(&mut self) -> QuantumEntanglementPair {
        let mut pair = QuantumEntanglementPair::new();
        
        // Ensure unique ID
        while self.pairs.contains_key(&pair.id) {
            pair = QuantumEntanglementPair::new();
        }
        
        self.pairs.insert(pair.id.clone(), pair.clone());
        self.save_pairs();
        pair
    }

    fn verify_pair(&self, pair_id: &str) -> Option<bool> {
        self.pairs.get(pair_id).map(|pair| pair.verify())
    }

    fn list_pairs(&self) -> Vec<&QuantumEntanglementPair> {
        self.pairs.values().collect()
    }

    fn visualize_pair(&self, pair_id: &str) -> Option<String> {
        self.pairs.get(pair_id).map(|pair| pair.visualize())
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    
    if args.len() < 2 {
        print_usage();
        return;
    }

    let command = &args[1];
    let mut checker = QuantumEntanglementChecker::new();

    match command.as_str() {
        "generate" => {
            let pair = checker.generate_pair();
            println!("\nQuantum Entanglement Pair Generated!\n");
            println!("Pair ID: {}", pair.id);
            println!("Particle A: {}", pair.particle_a.to_string());
            println!("Particle B: {}", pair.particle_b.to_string());
            println!("Entanglement Strength: {:.1}%", pair.entanglement_strength);
            println!("Quantum Coherence: {}", pair.coherence);
            println!("\nThe particles are now quantumly entangled across spacetime!");
        }
        "verify" => {
            if args.len() < 3 {
                println!("Error: Please provide a pair ID to verify");
                println!("Usage: {} verify <pair_id>", args[0]);
                return;
            }
            let pair_id = &args[2];
            match checker.verify_pair(pair_id) {
                Some(true) => println!("✓ Quantum entanglement verified for pair: {}", pair_id),
                Some(false) => println!("✗ Quantum entanglement failed verification for pair: {}", pair_id),
                None => println!("✗ No quantum entanglement pair found with ID: {}", pair_id),
            }
        }
        "list" => {
            let pairs = checker.list_pairs();
            if pairs.is_empty() {
                println!("No quantum entanglement pairs found.");
            } else {
                println!("\nQuantum Entanglement Pairs ({} found):", pairs.len());
                for pair in pairs {
                    println!("- {} (A: {}, B: {}, Strength: {:.1}%)", 
                        pair.id, 
                        pair.particle_a.to_string(),
                        pair.particle_b.to_string(),
                        pair.entanglement_strength);
                }
            }
        }
        "visualize" => {
            if args.len() < 3 {
                println!("Error: Please provide a pair ID to visualize");
                println!("Usage: {} visualize <pair_id>", args[0]);
                return;
            }
            let pair_id = &args[2];
            match checker.visualize_pair(pair_id) {
                Some(visualization) => println!("{}", visualization),
                None => println!("✗ No quantum entanglement pair found with ID: {}", pair_id),
            }
        }
        _ => {
            println!("Unknown command: {}", command);
            print_usage();
        }
    }
}

fn print_usage() {
    println!("\nNightly Quantum Entanglement Checker");
    println!("=====================================");
    println!("\nUsage:");
    println!("  nightly-quantum-entanglement-checker generate    Generate a new entanglement pair");
    println!("  nightly-quantum-entanglement-checker verify <id>  Verify an existing entanglement pair");
    println!("  nightly-quantum-entanglement-checker list         List all entanglement pairs");
    println!("  nightly-quantum-entanglement-checker visualize <id>  Visualize quantum states");
    println!("\nExample:");
    println!("  nightly-quantum-entanglement-checker generate");
    println!("  nightly-quantum-entanglement-checker verify QEP-7f9c3e2a-4b1d-8f2e-9a6c-d3e5f7b9a1c8");
    println!("  nightly-quantum-entanglement-checker list");
    println!("  nightly-quantum-entanglement-checker visualize QEP-7f9c3e2a-4b1d-8f2e-9a6c-d3e5f7b9a1c8");
    println!();
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::fs;

    #[test]
    fn test_quantum_state_to_string() {
        assert_eq!(QuantumState::Zero.to_string(), "|0⟩");
        assert_eq!(QuantumState::One.to_string(), "|1⟩");
        assert_eq!(QuantumState::Superposition.to_string(), "|ψ⟩");
    }

    #[test]
    fn test_entanglement_pair_creation() {
        let pair = QuantumEntanglementPair::new();
        assert!(pair.id.starts_with("QEP-"));
        assert_eq!(pair.particle_a, QuantumState::Zero);
        assert_eq!(pair.particle_b, QuantumState::One);
        assert!(pair.entanglement_strength >= 90.0 && pair.entanglement_strength <= 100.0);
        assert_eq!(pair.coherence, "Stable");
        assert!(!pair.timestamp.is_empty());
    }

    #[test]
    fn test_entanglement_verification() {
        let pair = QuantumEntanglementPair::new();
        assert!(pair.verify());
        
        // Test invalid entanglement
        let mut invalid_pair = pair.clone();
        invalid_pair.particle_a = QuantumState::Superposition;
        assert!(!invalid_pair.verify());
    }

    #[test]
    fn test_quantum_checker_generate() {
        let mut checker = QuantumEntanglementChecker::new();
        let pair = checker.generate_pair();
        
        assert!(checker.pairs.contains_key(&pair.id));
        assert_eq!(checker.pairs.get(&pair.id).unwrap().id, pair.id);
    }

    #[test]
    fn test_quantum_checker_verify() {
        let mut checker = QuantumEntanglementChecker::new();
        let pair = checker.generate_pair();
        
        assert_eq!(checker.verify_pair(&pair.id), Some(true));
        assert_eq!(checker.verify_pair("nonexistent"), None);
    }

    #[test]
    fn test_quantum_checker_list() {
        let mut checker = QuantumEntanglementChecker::new();
        let pair1 = checker.generate_pair();
        let pair2 = checker.generate_pair();
        
        let pairs = checker.list_pairs();
        assert_eq!(pairs.len(), 2);
        assert!(pairs.iter().any(|p| p.id == pair1.id));
        assert!(pairs.iter().any(|p| p.id == pair2.id));
    }

    #[test]
    fn test_quantum_checker_visualize() {
        let mut checker = QuantumEntanglementChecker::new();
        let pair = checker.generate_pair();
        
        let visualization = checker.visualize_pair(&pair.id).unwrap();
        assert!(visualization.contains(&pair.id));
        assert!(visualization.contains("Quantum Entanglement Visualization"));
        assert!(visualization.contains("Spacetime Entanglement Status: ✓ CONNECTED"));
    }

    #[test]
    fn test_data_persistence() {
        // Clean up any existing test file
        let test_file = "test_quantum_pairs.json";
        if Path::new(test_file).exists() {
            fs::remove_file(test_file).ok();
        }
        
        // Create checker with test file
        let mut checker = QuantumEntanglementChecker {
            pairs: HashMap::new(),
            data_file: test_file.to_string(),
        };
        
        // Generate a pair
        let pair = checker.generate_pair();
        
        // Create new checker and verify persistence
        let checker2 = QuantumEntanglementChecker {
            pairs: HashMap::new(),
            data_file: test_file.to_string(),
        };
        
        assert!(checker2.pairs.contains_key(&pair.id));
        
        // Clean up
        fs::remove_file(test_file).ok();
    }
}

// Mock implementations for testing
#[cfg(test)]
mod mocks {
    use super::*;

    // Mock rand for deterministic testing
    pub mod rand {
        pub fn random<T: Random>() -> T {
            T::mock_value()
        }
    }

    pub trait Random {
        fn mock_value() -> Self;
    }

    impl Random for f32 {
        fn mock_value() -> Self {
            0.5 // Deterministic value for testing
        }
    }

    // Mock chrono for deterministic testing
    pub mod chrono {
        use super::*;
        
        pub struct Utc;
        
        impl Utc {
            pub fn now() -> DateTime {
                DateTime
            }
        }
        
        pub struct DateTime;
        
        impl DateTime {
            pub fn to_rfc3339(&self) -> String {
                "2024-01-01T00:00:00Z".to_string() // Deterministic timestamp
            }
        }
    }
}

// Re-export mock modules for use in tests
#[cfg(test)]
use mocks::*;
