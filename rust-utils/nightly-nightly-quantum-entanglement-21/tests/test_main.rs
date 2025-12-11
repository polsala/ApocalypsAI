use std::fs;
use std::path::Path;

// Mock rationale: We create temporary test files to verify entanglement detection
// without relying on external files, ensuring deterministic offline tests

#[test]
fn test_identical_files_entangled() {
    // Create two identical test files
    let temp_dir = std::env::temp_dir();
    let file1_path = temp_dir.join("test_file1.txt");
    let file2_path = temp_dir.join("test_file2.txt");
    
    let test_content = "This is identical content for testing quantum entanglement!";
    
    fs::write(&file1_path, test_content).expect("Failed to write test file 1");
    fs::write(&file2_path, test_content).expect("Failed to write test file 2");
    
    // Test entanglement check
    let result = super::check_entanglement(
        file1_path.to_str().unwrap(),
        file2_path.to_str().unwrap()
    ).expect("Entanglement check failed");
    
    assert!(result.entangled, "Identical files should be quantumly entangled");
    assert!(result.confidence > 0.9, "Confidence should be very high for identical files");
    assert!(result.quantum_randomness > 0.0, "Quantum randomness should be applied");
    
    // Clean up
    fs::remove_file(&file1_path).ok();
    fs::remove_file(&file2_path).ok();
}

#[test]
fn test_different_files_not_entangled() {
    // Create two different test files
    let temp_dir = std::env::temp_dir();
    let file1_path = temp_dir.join("test_file3.txt");
    let file2_path = temp_dir.join("test_file4.txt");
    
    let content1 = "First file content";
    let content2 = "Second different content";
    
    fs::write(&file1_path, content1).expect("Failed to write test file 1");
    fs::write(&file2_path, content2).expect("Failed to write test file 2");
    
    // Test entanglement check
    let result = super::check_entanglement(
        file1_path.to_str().unwrap(),
        file2_path.to_str().unwrap()
    ).expect("Entanglement check failed");
    
    assert!(!result.entangled, "Different files should not be entangled");
    assert!(result.confidence < 0.5, "Confidence should be low for different files");
    
    // Clean up
    fs::remove_file(&file1_path).ok();
    fs::remove_file(&file2_path).ok();
}

#[test]
fn test_nonexistent_file_error() {
    let temp_dir = std::env::temp_dir();
    let existing_file = temp_dir.join("existing_test.txt");
    let nonexistent_file = temp_dir.join("nonexistent.txt");
    
    fs::write(&existing_file, "test content").expect("Failed to write test file");
    
    // Test with nonexistent file
    let result = super::check_entanglement(
        existing_file.to_str().unwrap(),
        nonexistent_file.to_str().unwrap()
    );
    
    assert!(result.is_err(), "Should return error for nonexistent file");
    assert!(result.unwrap_err().contains("File not found"), "Error should mention missing file");
    
    // Clean up
    fs::remove_file(&existing_file).ok();
}

#[test]
fn test_empty_files_entangled() {
    // Test with two empty files
    let temp_dir = std::env::temp_dir();
    let file1_path = temp_dir.join("empty1.txt");
    let file2_path = temp_dir.join("empty2.txt");
    
    fs::write(&file1_path, "").expect("Failed to write empty file 1");
    fs::write(&file2_path, "").expect("Failed to write empty file 2");
    
    let result = super::check_entanglement(
        file1_path.to_str().unwrap(),
        file2_path.to_str().unwrap()
    ).expect("Entanglement check failed");
    
    assert!(result.entangled, "Empty files should be entangled (same hash)");
    assert!(result.confidence > 0.9, "Confidence should be high for empty files");
    
    // Clean up
    fs::remove_file(&file1_path).ok();
    fs::remove_file(&file2_path).ok();
}

#[test]
fn test_large_files_entangled() {
    // Test with larger files to ensure performance
    let temp_dir = std::env::temp_dir();
    let file1_path = temp_dir.join("large1.txt");
    let file2_path = temp_dir.join("large2.txt");
    
    // Create a large string content (1MB)
    let large_content = "A".repeat(1024 * 1024);
    
    fs::write(&file1_path, &large_content).expect("Failed to write large file 1");
    fs::write(&file2_path, &large_content).expect("Failed to write large file 2");
    
    let result = super::check_entanglement(
        file1_path.to_str().unwrap(),
        file2_path.to_str().unwrap()
    ).expect("Entanglement check failed");
    
    assert!(result.entangled, "Large identical files should be entangled");
    assert!(result.confidence > 0.9, "Confidence should be high for large identical files");
    
    // Clean up
    fs::remove_file(&file1_path).ok();
    fs::remove_file(&file2_path).ok();
}
