use nightly_quantum_entanglement_checker::*;
use std::fs;
use tempfile::NamedTempFile;

#[test]
fn test_hash_generation_consistency() {
    // Test that the same content always produces the same hash
    let content = b"Consistent test content";
    let hash1 = generate_hash(content);
    let hash2 = generate_hash(content);
    assert_eq!(hash1, hash2, "Same content should produce identical hashes");
}

#[test]
fn test_hash_uniqueness() {
    // Test that different content produces different hashes
    let content1 = b"Content A";
    let content2 = b"Content B";
    let hash1 = generate_hash(content1);
    let hash2 = generate_hash(content2);
    assert_ne!(hash1, hash2, "Different content should produce different hashes");
}

#[test]
fn test_empty_content_hash() {
    // Test hashing empty content
    let empty_content = b"";
    let hash = generate_hash(empty_content);
    assert_eq!(hash.len(), 64, "Empty content should still produce a 64-char hash");
    assert_eq!(hash, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "SHA-256 of empty string should be known value");
}

#[test]
fn test_large_content_hash() {
    // Test hashing large content
    let large_content = vec![b'a'; 1000000]; // 1MB of 'a'
    let hash = generate_hash(&large_content);
    assert_eq!(hash.len(), 64, "Large content should produce a 64-char hash");
}

#[test]
fn test_entanglement_logic_identical_hashes() {
    // Test entanglement detection with identical hashes
    let hash = "a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890";
    assert!(are_entangled(&hash, &hash), "Identical hashes should be entangled");
}

#[test]
fn test_entanglement_logic_different_hashes() {
    // Test entanglement detection with different hashes
    let hash_a = "a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890";
    let hash_b = "f0e1d2c3b4a5968778695a4b3c2d1e0f0e1d2c3b4a5968778695a4b3c2d1e0f0";
    assert!(!are_entangled(&hash_a, &hash_b), "Different hashes should not be entangled");
}

#[test]
fn test_entanglement_report_formatting() {
    // Test that the entanglement report has correct formatting
    let report = generate_entanglement_report("test_a.rs", "test_b.rs", true);
    assert!(report.starts_with("🔬 Quantum Entanglement Analysis Report 🔬"), "Report should start with header");
    assert!(report.contains("File A: test_a.rs"), "Report should contain File A name");
    assert!(report.contains("File B: test_b.rs"), "Report should contain File B name");
    assert!(report.contains("ENTANGLEMENT CONFIRMED"), "Report should contain entanglement status");
}

#[test]
fn test_file_hash_consistency() {
    // Test that the same file always produces the same hash
    let temp_file = NamedTempFile::new().unwrap();
    let content = b"Test file content";
    fs::write(temp_file.path(), content).unwrap();
    
    let hash1 = get_file_hash(temp_file.path()).unwrap();
    let hash2 = get_file_hash(temp_file.path()).unwrap();
    assert_eq!(hash1, hash2, "Same file should produce identical hashes");
}

#[test]
fn test_file_hash_error_handling() {
    // Test error handling for non-existent files
    let result = get_file_hash("/path/that/does/not/exist.txt");
    assert!(result.is_err(), "Should return error for non-existent file");
}

#[test]
fn test_string_hash_vs_file_hash() {
    // Test that string hashing matches file hashing for same content
    let content = "String and file content";
    let string_hash = get_string_hash(content);
    
    let temp_file = NamedTempFile::new().unwrap();
    fs::write(temp_file.path(), content).unwrap();
    let file_hash = get_file_hash(temp_file.path()).unwrap();
    
    assert_eq!(string_hash, file_hash, "String hash should match file hash for same content");
}

#[test]
fn test_temporary_file_lifecycle() {
    // Test that temporary files work correctly in our context
    let temp_file = NamedTempFile::new().unwrap();
    let content = b"Temporary file test";
    fs::write(temp_file.path(), content).unwrap();
    
    // Verify file exists and can be read
    let hash = get_file_hash(temp_file.path()).unwrap();
    assert_eq!(hash.len(), 64);
    
    // File should be automatically cleaned up when temp_file goes out of scope
}

#[test]
fn test_unicode_content_hashing() {
    // Test hashing content with unicode characters
    let unicode_content = "Hello, 世界! 🌍";
    let hash = get_string_hash(unicode_content);
    assert_eq!(hash.len(), 64, "Unicode content should produce a 64-char hash");
}

#[test]
fn test_special_characters_hashing() {
    // Test hashing content with special characters
    let special_content = "Special chars: !@#$%^&*()_+-=[]{}|;':",./<>?";
    let hash = get_string_hash(special_content);
    assert_eq!(hash.len(), 64, "Special characters should produce a 64-char hash");
}

#[test]
fn test_report_contains_all_required_elements() {
    // Test that the report contains all required elements
    let report = generate_entanglement_report("file_a.rs", "file_b.rs", true);
    let required_elements = [
        "🔬 Quantum Entanglement Analysis Report 🔬",
        "==========================================",
        "File A: file_a.rs",
        "File B: file_b.rs",
        "ENTANGLEMENT CONFIRMED",
        "Quantum Coherence Level: MAXIMUM",
        "Spooky Action at Distance: DETECTED",
        "Recommendation:"
    ];
    
    for element in &required_elements {
        assert!(report.contains(element), "Report should contain: {}", element);
    }
}

#[test]
fn test_negative_entanglement_report() {
    // Test that the negative entanglement report contains correct elements
    let report = generate_entanglement_report("file_a.rs", "file_b.rs", false);
    assert!(report.contains("ENTANGLEMENT REJECTED"), "Report should contain rejection message");
    assert!(report.contains("Quantum Coherence Level: NONE"), "Report should indicate no coherence");
    assert!(report.contains("NOT DETECTED"), "Report should indicate no spooky action");
}

#[test]
fn test_hash_collision_resistance() {
    // Test that similar but different content produces different hashes
    let content1 = b"Almost identical content";
    let content2 = b"Almost identical contenx"; // Changed last character
    let hash1 = generate_hash(content1);
    let hash2 = generate_hash(content2);
    assert_ne!(hash1, hash2, "Slightly different content should produce different hashes");
}

#[test]
fn test_deterministic_hashing() {
    // Test that hashing is deterministic across multiple runs
    let content = b"Deterministic test content";
    let expected_hash = generate_hash(content);
    
    // Generate hash multiple times to ensure consistency
    for _ in 0..10 {
        let hash = generate_hash(content);
        assert_eq!(hash, expected_hash, "Hashing should be deterministic");
    }
}
