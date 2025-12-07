use std::fs;
use std::io::Write;
use tempfile::NamedTempFile;
use sha2::{Sha256, Digest};

// Import the main module
use crate::*;

#[test]
fn test_calculate_coherence_identical_hashes() {
    let hash = "a1b2c3d4e5f67890123456789012345678901234567890123456789012345678";
    let coherence = calculate_coherence(hash, hash);
    assert_eq!(coherence, 10.0);
}

#[test]
fn test_calculate_coherence_different_hashes() {
    let hash1 = "a1b2c3d4e5f67890123456789012345678901234567890123456789012345678";
    let hash2 = "f8e7d6c5b4a39281091827364554637281920394857684736273849506172839";
    let coherence = calculate_coherence(hash1, hash2);
    assert!(coherence >= 0.0 && coherence <= 10.0);
}

#[test]
fn test_calculate_coherence_partial_match() {
    let hash1 = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
    let hash2 = "aaaabbaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
    let coherence = calculate_coherence(hash1, hash2);
    assert!(coherence > 0.0 && coherence < 10.0);
}

#[test]
fn test_calculate_file_hash_identical_files() {
    let mut temp_file1 = NamedTempFile::new().unwrap();
    let mut temp_file2 = NamedTempFile::new().unwrap();
    
    let test_content = b"Hello, quantum world! This is a test file for hash calculation.";
    
    temp_file1.write_all(test_content).unwrap();
    temp_file2.write_all(test_content).unwrap();
    
    let hash1 = calculate_file_hash(temp_file1.path()).unwrap();
    let hash2 = calculate_file_hash(temp_file2.path()).unwrap();
    
    assert_eq!(hash1, hash2);
}

#[test]
fn test_calculate_file_hash_different_files() {
    let mut temp_file1 = NamedTempFile::new().unwrap();
    let mut temp_file2 = NamedTempFile::new().unwrap();
    
    temp_file1.write_all(b"File content A").unwrap();
    temp_file2.write_all(b"File content B").unwrap();
    
    let hash1 = calculate_file_hash(temp_file1.path()).unwrap();
    let hash2 = calculate_file_hash(temp_file2.path()).unwrap();
    
    assert_ne!(hash1, hash2);
}

#[test]
fn test_calculate_file_hash_empty_files() {
    let mut temp_file1 = NamedTempFile::new().unwrap();
    let mut temp_file2 = NamedTempFile::new().unwrap();
    
    // Write empty content
    temp_file1.write_all(b"").unwrap();
    temp_file2.write_all(b"").unwrap();
    
    let hash1 = calculate_file_hash(temp_file1.path()).unwrap();
    let hash2 = calculate_file_hash(temp_file2.path()).unwrap();
    
    // Empty files should have the same hash
    assert_eq!(hash1, hash2);
}

#[test]
fn test_calculate_file_hash_large_files() {
    let mut temp_file1 = NamedTempFile::new().unwrap();
    let mut temp_file2 = NamedTempFile::new().unwrap();
    
    // Create large content (1MB)
    let large_content = vec![b'a'; 1024 * 1024];
    
    temp_file1.write_all(&large_content).unwrap();
    temp_file2.write_all(&large_content).unwrap();
    
    let hash1 = calculate_file_hash(temp_file1.path()).unwrap();
    let hash2 = calculate_file_hash(temp_file2.path()).unwrap();
    
    assert_eq!(hash1, hash2);
}

#[test]
fn test_quantum_result_creation_match() {
    let hash = "a1b2c3d4e5f67890123456789012345678901234567890123456789012345678";
    let result = QuantumResult::new(
        "file1.txt".to_string(),
        "file2.txt".to_string(),
        hash.to_string(),
        hash.to_string(),
    );
    
    assert!(result.quantum_match);
    assert_eq!(result.entanglement_probability, 1.0);
    assert_eq!(result.coherence_score, 10.0);
}

#[test]
fn test_quantum_result_creation_no_match() {
    let hash1 = "a1b2c3d4e5f67890123456789012345678901234567890123456789012345678";
    let hash2 = "f8e7d6c5b4a39281091827364554637281920394857684736273849506172839";
    let result = QuantumResult::new(
        "file1.txt".to_string(),
        "file2.txt".to_string(),
        hash1.to_string(),
        hash2.to_string(),
    );
    
    assert!(!result.quantum_match);
    assert_eq!(result.entanglement_probability, 0.0);
    assert!(result.coherence_score >= 0.0 && result.coherence_score <= 10.0);
}

#[test]
fn test_quantum_uncertainty_factor() {
    // Test that quantum uncertainty affects the result
    let hash1 = "a1b2c3d4e5f67890123456789012345678901234567890123456789012345678";
    let hash2 = "a1b2c3d4e5f67890123456789012345678901234567890123456789012345678";
    
    let result1 = QuantumResult::new(
        "file1.txt".to_string(),
        "file2.txt".to_string(),
        hash1.to_string(),
        hash2.to_string(),
    );
    
    let result2 = QuantumResult::new(
        "file1.txt".to_string(),
        "file2.txt".to_string(),
        hash1.to_string(),
        hash2.to_string(),
    );
    
    // With quantum uncertainty, results might vary slightly
    // This test mainly ensures the code runs without panicking
    assert!(result1.entanglement_probability >= 0.0 && result1.entanglement_probability <= 1.0);
    assert!(result2.entanglement_probability >= 0.0 && result2.entanglement_probability <= 1.0);
}

#[test]
fn test_batch_file_processing() {
    let mut batch_file = NamedTempFile::new().unwrap();
    
    // Create test files
    let mut temp_file1 = NamedTempFile::new().unwrap();
    let mut temp_file2 = NamedTempFile::new().unwrap();
    let mut temp_file3 = NamedTempFile::new().unwrap();
    let mut temp_file4 = NamedTempFile::new().unwrap();
    
    temp_file1.write_all(b"test content 1").unwrap();
    temp_file2.write_all(b"test content 1").unwrap(); // Same content
    temp_file3.write_all(b"test content 2").unwrap(); // Different content
    temp_file4.write_all(b"test content 3").unwrap(); // Different content
    
    // Write batch file
    let batch_content = format!(
        "{} {}
{} {}
# This is a comment
# Another comment
{} {}
",
        temp_file1.path().to_str().unwrap(),
        temp_file2.path().to_str().unwrap(),
        temp_file1.path().to_str().unwrap(),
        temp_file3.path().to_str().unwrap(),
        temp_file3.path().to_str().unwrap(),
        temp_file4.path().to_str().unwrap(),
    );
    
    batch_file.write_all(batch_content.as_bytes()).unwrap();
    
    let results = process_batch_file(batch_file.path()).unwrap();
    
    assert_eq!(results.len(), 3);
    
    // First pair should match (same content)
    assert!(results[0].quantum_match);
    
    // Second pair should not match (different content)
    assert!(!results[1].quantum_match);
    
    // Third pair should not match (different content)
    assert!(!results[2].quantum_match);
}

#[test]
fn test_batch_file_with_invalid_lines() {
    let mut batch_file = NamedTempFile::new().unwrap();
    
    // Write batch file with invalid lines
    let batch_content = "
invalid_line
file1.txt file2.txt file3.txt
file1.txt file2.txt
# comment line
";
    
    batch_file.write_all(batch_content.as_bytes()).unwrap();
    
    let results = process_batch_file(batch_file.path()).unwrap();
    
    // Should only process the valid line
    assert_eq!(results.len(), 1);
}

#[test]
fn test_file_not_found_error() {
    let result = calculate_file_hash("nonexistent_file.txt");
    assert!(result.is_err());
}

#[test]
fn test_hash_consistency() {
    // Test that the same file always produces the same hash
    let mut temp_file = NamedTempFile::new().unwrap();
    temp_file.write_all(b"consistent test content").unwrap();
    
    let hash1 = calculate_file_hash(temp_file.path()).unwrap();
    let hash2 = calculate_file_hash(temp_file.path()).unwrap();
    
    assert_eq!(hash1, hash2);
}

#[test]
fn test_sha256_hash_format() {
    // Test that our hash function produces valid SHA-256 format
    let mut temp_file = NamedTempFile::new().unwrap();
    temp_file.write_all(b"test").unwrap();
    
    let hash = calculate_file_hash(temp_file.path()).unwrap();
    
    // SHA-256 hash should be 64 hex characters
    assert_eq!(hash.len(), 64);
    assert!(hash.chars().all(|c| c.is_ascii_hexdigit()));
}

// Mock rationale: These tests verify the core functionality of the quantum entanglement checker
// without requiring external dependencies or network access. They test hash calculation,
// coherence scoring, quantum result creation, and batch file processing with various edge cases.
