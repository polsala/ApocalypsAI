use std::fs;
use std::path::Path;
use nightly_quantum_entanglement_checker::*;

#[test]
fn test_get_file_hash() {
    // Create temporary test files
    fs::write("test_file1.txt", "Hello World").unwrap();
    fs::write("test_file2.txt", "Hello World").unwrap();
    fs::write("test_file3.txt", "Different Content").unwrap();
    
    let checker = QuantumEntanglementChecker::new().unwrap();
    
    // Test that identical files have the same hash
    let hash1 = checker.get_file_hash("test_file1.txt").unwrap();
    let hash2 = checker.get_file_hash("test_file2.txt").unwrap();
    assert_eq!(hash1, hash2, "Identical files should have the same hash");
    
    // Test that different files have different hashes
    let hash3 = checker.get_file_hash("test_file3.txt").unwrap();
    assert_ne!(hash1, hash3, "Different files should have different hashes");
    
    // Test file not found error
    let result = checker.get_file_hash("nonexistent.txt");
    assert!(result.is_err(), "Should return error for nonexistent file");
    
    // Cleanup
    fs::remove_file("test_file1.txt").unwrap();
    fs::remove_file("test_file2.txt").unwrap();
    fs::remove_file("test_file3.txt").unwrap();
}

#[test]
fn test_calculate_correlation() {
    // Create test files
    fs::write("test_file1.txt", "Hello World").unwrap();
    fs::write("test_file2.txt", "Hello World").unwrap();
    fs::write("test_file3.txt", "Different Content").unwrap();
    
    let checker = QuantumEntanglementChecker::new().unwrap();
    
    // Test correlation between identical files
    let correlation1 = checker.calculate_correlation("test_file1.txt", "test_file2.txt").unwrap();
    assert!(correlation1 > 0.9, "Identical files should have high correlation");
    
    // Test correlation between different files
    let correlation2 = checker.calculate_correlation("test_file1.txt", "test_file3.txt").unwrap();
    assert!(correlation2 < correlation1, "Different files should have lower correlation");
    
    // Cleanup
    fs::remove_file("test_file1.txt").unwrap();
    fs::remove_file("test_file2.txt").unwrap();
    fs::remove_file("test_file3.txt").unwrap();
}

#[test]
fn test_entangle_files() {
    let mut checker = QuantumEntanglementChecker::new().unwrap();
    
    // Create test files
    fs::write("test_file1.txt", "Hello World").unwrap();
    fs::write("test_file2.txt", "Hello World").unwrap();
    
    // Test successful entanglement
    let result = checker.entangle_files("test_file1.txt", "test_file2.txt", None);
    assert!(result.is_ok(), "Should successfully entangle files");
    
    // Test entanglement with custom strength
    let result = checker.entangle_files("test_file1.txt", "test_file3.txt", Some(0.95));
    assert!(result.is_ok(), "Should successfully entangle files with custom strength");
    
    // Test entanglement with same file
    let result = checker.entangle_files("test_file1.txt", "test_file1.txt", None);
    assert!(result.is_err(), "Should not allow entangling a file with itself");
    
    // Check that records were saved
    assert_eq!(checker.records.len(), 2, "Should have 2 entanglement records");
    
    // Cleanup
    fs::remove_file("test_file1.txt").unwrap();
    fs::remove_file("test_file2.txt").unwrap();
    fs::remove_file("test_file3.txt").unwrap();
}

#[test]
fn test_check_entanglement() {
    let mut checker = QuantumEntanglementChecker::new().unwrap();
    
    // Create test files
    fs::write("test_file1.txt", "Hello World").unwrap();
    fs::write("test_file2.txt", "Hello World").unwrap();
    fs::write("test_file3.txt", "Different Content").unwrap();
    
    // Entangle files first
    checker.entangle_files("test_file1.txt", "test_file2.txt", None).unwrap();
    
    // Test checking entanglement between identical files
    let status = checker.check_entanglement("test_file1.txt", "test_file2.txt").unwrap();
    assert!(status.entangled, "Identical files should be entangled");
    assert!(status.correlation > 0.9, "Should have high correlation");
    
    // Test checking entanglement between different files
    let status = checker.check_entanglement("test_file1.txt", "test_file3.txt").unwrap();
    assert!(!status.entangled, "Different files should not be entangled");
    assert!(status.correlation < 0.5, "Should have low correlation");
    
    // Test checking non-existent file
    let result = checker.check_entanglement("test_file1.txt", "nonexistent.txt");
    assert!(result.is_err(), "Should return error for non-existent file");
    
    // Cleanup
    fs::remove_file("test_file1.txt").unwrap();
    fs::remove_file("test_file2.txt").unwrap();
    fs::remove_file("test_file3.txt").unwrap();
}

#[test]
fn test_list_entangled_pairs() {
    let mut checker = QuantumEntanglementChecker::new().unwrap();
    
    // Create test files
    fs::write("test_file1.txt", "Hello World").unwrap();
    fs::write("test_file2.txt", "Hello World").unwrap();
    fs::write("test_file3.txt", "Hello World").unwrap();
    fs::write("test_file4.txt", "Hello World").unwrap();
    
    // Entangle multiple file pairs
    checker.entangle_files("test_file1.txt", "test_file2.txt", None).unwrap();
    checker.entangle_files("test_file3.txt", "test_file4.txt", None).unwrap();
    
    let pairs = checker.list_entangled_pairs();
    assert_eq!(pairs.len(), 2, "Should have 2 entangled pairs");
    assert!(pairs.contains(&("test_file1.txt".to_string(), "test_file2.txt".to_string())));
    assert!(pairs.contains(&("test_file3.txt".to_string(), "test_file4.txt".to_string())));
    
    // Cleanup
    fs::remove_file("test_file1.txt").unwrap();
    fs::remove_file("test_file2.txt").unwrap();
    fs::remove_file("test_file3.txt").unwrap();
    fs::remove_file("test_file4.txt").unwrap();
}

#[test]
fn test_clean_records() {
    let mut checker = QuantumEntanglementChecker::new().unwrap();
    
    // Create test files and entangle them
    fs::write("test_file1.txt", "Hello World").unwrap();
    fs::write("test_file2.txt", "Hello World").unwrap();
    checker.entangle_files("test_file1.txt", "test_file2.txt", None).unwrap();
    
    assert_eq!(checker.records.len(), 1, "Should have 1 entanglement record");
    
    // Clean records
    checker.clean_records().unwrap();
    assert_eq!(checker.records.len(), 0, "Should have 0 entanglement records after cleaning");
    
    // Cleanup
    fs::remove_file("test_file1.txt").unwrap();
    fs::remove_file("test_file2.txt").unwrap();
}

#[test]
fn test_config_loading() {
    // Test default config
    let config = QuantumConfig::default();
    assert_eq!(config.threshold, 0.7);
    assert_eq!(config.strength, 0.9);
    assert_eq!(config.output.format, "console");
    assert_eq!(config.output.verbose, false);
    
    // Test TOML config file
    let toml_content = r#"
[entanglement]
threshold = 0.8
strength = 0.95

[output]
format = "json"
verbose = true
"#;
    
    fs::write(".test-quantum-entanglement.toml", toml_content).unwrap();
    
    let config: QuantumConfig = toml::from_str(toml_content).unwrap();
    assert_eq!(config.threshold, 0.8);
    assert_eq!(config.strength, 0.95);
    assert_eq!(config.output.format, "json");
    assert_eq!(config.output.verbose, true);
    
    // Cleanup
    fs::remove_file(".test-quantum-entanglement.toml").unwrap();
}

#[test]
fn test_quantum_concepts() {
    // Test correlation calculation edge cases
    let mut checker = QuantumEntanglementChecker::new().unwrap();
    
    // Create empty files
    fs::write("empty1.txt", "").unwrap();
    fs::write("empty2.txt", "").unwrap();
    
    let correlation = checker.calculate_correlation("empty1.txt", "empty2.txt").unwrap();
    assert!(correlation > 0.9, "Empty files should have high correlation");
    
    // Create very large identical files
    let large_content = "x".repeat(10000);
    fs::write("large1.txt", &large_content).unwrap();
    fs::write("large2.txt", &large_content).unwrap();
    
    let correlation = checker.calculate_correlation("large1.txt", "large2.txt").unwrap();
    assert!(correlation > 0.9, "Large identical files should have high correlation");
    
    // Cleanup
    fs::remove_file("empty1.txt").unwrap();
    fs::remove_file("empty2.txt").unwrap();
    fs::remove_file("large1.txt").unwrap();
    fs::remove_file("large2.txt").unwrap();
}

#[test]
fn test_error_handling() {
    let mut checker = QuantumEntanglementChecker::new().unwrap();
    
    // Test file not found
    let result = checker.get_file_hash("nonexistent.txt");
    assert!(result.is_err());
    
    // Test entanglement with non-existent files
    let result = checker.entangle_files("nonexistent1.txt", "nonexistent2.txt", None);
    assert!(result.is_err());
    
    // Test checking entanglement with non-existent files
    let result = checker.check_entanglement("nonexistent1.txt", "nonexistent2.txt");
    assert!(result.is_err());
}

#[test]
fn test_record_persistence() {
    // Clean up any existing records
    if Path::new(".quantum-entanglement-records.toml").exists() {
        fs::remove_file(".quantum-entanglement-records.toml").unwrap();
    }
    
    let mut checker = QuantumEntanglementChecker::new().unwrap();
    
    // Create test files and entangle them
    fs::write("test_file1.txt", "Hello World").unwrap();
    fs::write("test_file2.txt", "Hello World").unwrap();
    checker.entangle_files("test_file1.txt", "test_file2.txt", None).unwrap();
    
    // Verify record was saved to file
    assert!(Path::new(".quantum-entanglement-records.toml").exists());
    
    // Create new checker instance (simulating restart)
    let checker2 = QuantumEntanglementChecker::new().unwrap();
    assert_eq!(checker2.records.len(), 1, "Records should persist across restarts");
    
    // Cleanup
    fs::remove_file("test_file1.txt").unwrap();
    fs::remove_file("test_file2.txt").unwrap();
    fs::remove_file(".quantum-entanglement-records.toml").unwrap();
}
