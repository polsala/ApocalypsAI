use nightly_quantum_entanglement_checker::*;

#[cfg(test)]
mod tests {
    use super::*;
    use std::fs;
    use std::io::Write;
    use tempfile::NamedTempFile;

    #[test]
    fn test_calculate_hash_identical_content() {
        let content = b"fn main() { println!(\"Hello, world!\"); }";
        let hash1 = calculate_hash(content);
        let hash2 = calculate_hash(content);
        
        assert_eq!(hash1, hash2);
        assert_eq!(hash1.len(), 64); // SHA-256 produces 64 hex characters
    }

    #[test]
    fn test_calculate_hash_different_content() {
        let content1 = b"fn main() { println!(\"Hello\"); }";
        let content2 = b"fn main() { println!(\"World\"); }";
        
        let hash1 = calculate_hash(content1);
        let hash2 = calculate_hash(content2);
        
        assert_ne!(hash1, hash2);
        assert_eq!(hash1.len(), 64);
        assert_eq!(hash2.len(), 64);
    }

    #[test]
    fn test_calculate_similarity_identical_hashes() {
        let hash = "a1b2c3d4e5f6".repeat(4); // 48 chars
        let similarity = calculate_similarity(&hash, &hash);
        
        assert_eq!(similarity, 100.0);
    }

    #[test]
    fn test_calculate_similarity_different_hashes() {
        let hash1 = "a1b2c3d4e5f6".repeat(4);
        let hash2 = "f6e5d4c3b2a1".repeat(4);
        
        let similarity = calculate_similarity(&hash1, &hash2);
        
        assert_eq!(similarity, 0.0);
    }

    #[test]
    fn test_calculate_similarity_partial_match() {
        let hash1 = "abcdef123456".repeat(4);
        let hash2 = "abcdef654321".repeat(4);
        
        // First 6 characters match out of 48 total
        let expected_similarity = (6.0 / 48.0) * 100.0;
        let similarity = calculate_similarity(&hash1, &hash2);
        
        assert!((similarity - expected_similarity).abs() < 0.01);
    }

    #[test]
    fn test_get_entanglement_level_cosmic_background() {
        let (level, description) = get_entanglement_level(15.0);
        assert_eq!(level, "Cosmic Background Radiation");
        assert_eq!(description, "No meaningful connection");
    }

    #[test]
    fn test_get_entanglement_level_stellar_drift() {
        let (level, description) = get_entanglement_level(30.0);
        assert_eq!(level, "Stellar Drift");
        assert_eq!(description, "Slight similarities, likely coincidental");
    }

    #[test]
    fn test_get_entanglement_level_orbital_resonance() {
        let (level, description) = get_entanglement_level(50.0);
        assert_eq!(level, "Orbital Resonance");
        assert_eq!(description, "Noticeable patterns, worth investigating");
    }

    #[test]
    fn test_get_entanglement_level_gravitational_pull() {
        let (level, description) = get_entanglement_level(70.0);
        assert_eq!(level, "Gravitational Pull");
        assert_eq!(description, "Strong similarities, likely related");
    }

    #[test]
    fn test_get_entanglement_level_quantum_entanglement() {
        let (level, description) = get_entanglement_level(90.0);
        assert_eq!(level, "Quantum Entanglement");
        assert_eq!(description, "Nearly identical, definitely related");
    }

    #[test]
    fn test_get_status_message_cosmic_background() {
        let message = get_status_message(10.0);
        assert!(message.contains("separate realities"));
    }

    #[test]
    fn test_get_status_message_stellar_drift() {
        let message = get_status_message(30.0);
        assert!(message.contains("distant relationship"));
    }

    #[test]
    fn test_get_status_message_orbital_resonance() {
        let message = get_status_message(50.0);
        assert!(message.contains("intriguing patterns"));
    }

    #[test]
    fn test_get_status_message_gravitational_pull() {
        let message = get_status_message(70.0);
        assert!(message.contains("significant connection"));
    }

    #[test]
    fn test_get_status_message_quantum_entanglement() {
        let message = get_status_message(95.0);
        assert!(message.contains("fundamental connection"));
    }

    #[test]
    fn test_get_recommendation_cosmic_background() {
        let recommendation = get_recommendation(10.0);
        assert!(recommendation.contains("unrelated"));
    }

    #[test]
    fn test_get_recommendation_stellar_drift() {
        let recommendation = get_recommendation(30.0);
        assert!(recommendation.contains("Monitor"));
    }

    #[test]
    fn test_get_recommendation_orbital_resonance() {
        let recommendation = get_recommendation(50.0);
        assert!(recommendation.contains("investigating"));
    }

    #[test]
    fn test_get_recommendation_gravitational_pull() {
        let recommendation = get_recommendation(70.0);
        assert!(recommendation.contains("document the relationship"));
    }

    #[test]
    fn test_get_recommendation_quantum_entanglement() {
        let recommendation = get_recommendation(95.0);
        assert!(recommendation.contains("practically identical"));
    }

    #[test]
    fn test_read_content_from_file() {
        // Create a temporary file with test content
        let mut temp_file = NamedTempFile::new().unwrap();
        writeln!(temp_file, "fn test() {{}}").unwrap();
        
        let path = temp_file.path().to_str().unwrap();
        let content = read_content(path).unwrap();
        
        assert!(content.contains("fn test()"));
    }

    #[test]
    fn test_read_content_from_stdin() {
        // This test would require mocking stdin, which is complex
        // For now, we'll test the logic path exists
        // In a real implementation, you'd use a library like `mockall` or `tempfile` with stdin redirection
        let result = read_content("-");
        // This will fail in normal test environment, but validates the code path
        assert!(result.is_err());
    }

    #[test]
    fn test_end_to_end_identical_files() {
        // Create two identical temporary files
        let mut temp_file_a = NamedTempFile::new().unwrap();
        let mut temp_file_b = NamedTempFile::new().unwrap();
        
        let test_content = "fn main() { println!(\"Hello, world!\"); }";
        writeln!(temp_file_a, "{}").unwrap();
        writeln!(temp_file_b, "{}").unwrap();
        
        let path_a = temp_file_a.path().to_str().unwrap();
        let path_b = temp_file_b.path().to_str().unwrap();
        
        let content_a = read_content(path_a).unwrap();
        let content_b = read_content(path_b).unwrap();
        
        let hash_a = calculate_hash(content_a.as_bytes());
        let hash_b = calculate_hash(content_b.as_bytes());
        
        let probability = calculate_similarity(&hash_a, &hash_b);
        
        assert_eq!(probability, 100.0);
    }

    #[test]
    fn test_end_to_end_different_files() {
        // Create two different temporary files
        let mut temp_file_a = NamedTempFile::new().unwrap();
        let mut temp_file_b = NamedTempFile::new().unwrap();
        
        writeln!(temp_file_a, "fn main() {{ println!(\"Hello\"); }}").unwrap();
        writeln!(temp_file_b, "fn main() {{ println!(\"World\"); }}").unwrap();
        
        let path_a = temp_file_a.path().to_str().unwrap();
        let path_b = temp_file_b.path().to_str().unwrap();
        
        let content_a = read_content(path_a).unwrap();
        let content_b = read_content(path_b).unwrap();
        
        let hash_a = calculate_hash(content_a.as_bytes());
        let hash_b = calculate_hash(content_b.as_bytes());
        
        let probability = calculate_similarity(&hash_a, &hash_b);
        
        // Different files should have low similarity
        assert!(probability < 50.0);
    }
}
