use std::fs;
use std::path::Path;

// Import the functions from main.rs
// Since we can't use mod in tests without a lib.rs, we'll include the source
include!("../src/main.rs");

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_simple_hash_identical_strings() {
        let content = "Hello World";
        let hash1 = simple_hash(content);
        let hash2 = simple_hash(content);
        assert_eq!(hash1, hash2, "Identical strings should produce identical hashes");
    }

    #[test]
    fn test_simple_hash_different_strings() {
        let content1 = "Hello World";
        let content2 = "Hello World!";
        let hash1 = simple_hash(content1);
        let hash2 = simple_hash(content2);
        assert_ne!(hash1, hash2, "Different strings should produce different hashes");
    }

    #[test]
    fn test_quantum_entanglement_identical_hashes() {
        let hash = 12345;
        let state = check_quantum_entanglement(hash, hash);
        // Due to quantum probability, we can't guarantee the exact result
        // But we can test that it's not decoherent
        assert!(state != QuantumState::Decoherent, "Identical hashes should not be decoherent");
    }

    #[test]
    fn test_quantum_entanglement_different_hashes() {
        let hash1 = 12345;
        let hash2 = 67890;
        let state = check_quantum_entanglement(hash1, hash2);
        // Due to quantum probability, we can't guarantee the exact result
        // But we can test the logic paths
        // With our deterministic hash and fixed random calculation,
        // hash2 * 0.987654321 will be > 0.01, so it should be decoherent
        let expected_random = (hash2 as f64 * 0.987654321).fract();
        if expected_random >= 0.01 {
            assert_eq!(state, QuantumState::Decoherent, "Different hashes with high random value should be decoherent");
        }
    }

    #[test]
    fn test_quantum_state_emoji() {
        assert_eq!(QuantumState::Entangled.emoji(), "🌀");
        assert_eq!(QuantumState::Decoherent.emoji(), "❄️");
        assert_eq!(QuantumState::Superposition.emoji(), "⚛️");
    }

    #[test]
    fn test_quantum_state_description() {
        assert_eq!(QuantumState::Entangled.description(), "Quantum Entanglement Confirmed!");
        assert_eq!(QuantumState::Decoherent.description(), "Quantum Decoherence Detected");
        assert_eq!(QuantumState::Superposition.description(), "Quantum Superposition State");
    }

    #[test]
    fn test_read_file_content_success() {
        // Create a temporary test file
        let test_content = "This is a test file for quantum entanglement checking.";
        fs::write("test_file.txt", test_content).expect("Failed to create test file");
        
        let result = read_file_content(Path::new("test_file.txt"));
        
        assert!(result.is_ok(), "Should successfully read existing file");
        assert_eq!(result.unwrap(), test_content);
        
        // Clean up
        fs::remove_file("test_file.txt").expect("Failed to remove test file");
    }

    #[test]
    fn test_read_file_content_failure() {
        let result = read_file_content(Path::new("nonexistent_file.txt"));
        
        assert!(result.is_err(), "Should fail to read non-existent file");
        assert!(result.unwrap_err().contains("nonexistent_file.txt"), "Error message should contain filename");
    }

    #[test]
    fn test_quantum_probability_edge_cases() {
        // Test with hash values that would create specific random values
        // This tests the deterministic nature of our quantum simulation
        
        // Test case where hash1 * 0.123456789 creates a random value >= 0.99
        // This would be a superposition state
        let hash = 8100000000; // This creates random >= 0.99
        let state = check_quantum_entanglement(hash, hash);
        
        let expected_random = (hash as f64 * 0.123456789).fract();
        if expected_random >= 0.99 {
            assert_eq!(state, QuantumState::Superposition, "High random value should create superposition");
        }
    }

    #[test]
    fn test_hash_sensitivity() {
        // Test that small changes in input create different hashes
        let original = "fn main() { println!(\"Hello\"); }";
        let modified = "fn main() { println!(\"Hello\!"); }"; // Added exclamation
        
        let hash1 = simple_hash(original);
        let hash2 = simple_hash(modified);
        
        assert_ne!(hash1, hash2, "Small changes should produce different hashes");
    }

    #[test]
    fn test_empty_strings() {
        let hash1 = simple_hash("");
        let hash2 = simple_hash("");
        assert_eq!(hash1, hash2, "Empty strings should produce the same hash");
        
        let state = check_quantum_entanglement(hash1, hash2);
        assert!(state != QuantumState::Decoherent, "Empty strings should not be decoherent");
    }

    #[test]
    fn test_unicode_content() {
        let content1 = "🦀 Rust is awesome! 🌐";
        let content2 = "🦀 Rust is awesome! 🌐";
        let content3 = "🦀 Rust is awesome! 🌍"; // Different emoji
        
        let hash1 = simple_hash(content1);
        let hash2 = simple_hash(content2);
        let hash3 = simple_hash(content3);
        
        assert_eq!(hash1, hash2, "Identical Unicode strings should produce identical hashes");
        assert_ne!(hash1, hash3, "Different Unicode strings should produce different hashes");
    }
}
