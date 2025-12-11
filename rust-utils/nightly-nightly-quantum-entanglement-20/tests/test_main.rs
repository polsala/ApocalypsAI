use quantum_entanglement_checker::*;
use std::fs;
use tempfile::TempDir;

#[test]
fn test_full_entanglement_workflow() {
    // Create a temporary directory for testing
    let temp_dir = TempDir::new().unwrap();
    let dir_path = temp_dir.path();
    
    // Create test files
    let file1_path = dir_path.join("test1.txt");
    let file2_path = dir_path.join("test2.txt");
    let file3_path = dir_path.join("test3.txt");
    
    fs::write(&file1_path, "hello world content for testing").unwrap();
    fs::write(&file2_path, "hello rust content for testing").unwrap();
    fs::write(&file3_path, "completely different content here").unwrap();
    
    let checker = QuantumEntanglementChecker::new(0.1);
    
    // Test individual entanglement check
    let result = checker.check_entanglement(
        file1_path.to_str().unwrap(),
        file2_path.to_str().unwrap()
    );
    
    assert!(result.is_some());
    let result = result.unwrap();
    assert!(result.entanglement_score > 0.0);
    assert!(result.entanglement_score <= 1.0);
    
    // Test network generation
    let network_results = checker.find_entangled_files(dir_path.to_str().unwrap(), Some(0.1));
    
    assert!(network_results.len() >= 1);
    
    // Verify that file1 and file2 have higher entanglement than file3
    let file1_file2_result = network_results.iter().find(|r| {
        (r.file1 == file1_path.to_str().unwrap() && r.file2 == file2_path.to_str().unwrap()) ||
        (r.file1 == file2_path.to_str().unwrap() && r.file2 == file1_path.to_str().unwrap())
    });
    
    assert!(file1_file2_result.is_some());
    let file1_file2_score = file1_file2_result.unwrap().entanglement_score;
    
    // File3 should have lower entanglement with both file1 and file2
    let file1_file3_result = network_results.iter().find(|r| {
        (r.file1 == file1_path.to_str().unwrap() && r.file2 == file3_path.to_str().unwrap()) ||
        (r.file1 == file3_path.to_str().unwrap() && r.file2 == file1_path.to_str().unwrap())
    });
    
    if let Some(file1_file3) = file1_file3_result {
        assert!(file1_file3.entanglement_score < file1_file2_score);
    }
}

#[test]
fn test_entanglement_score_calculation() {
    let checker = QuantumEntanglementChecker::new(0.5);
    
    // Test with perfect correlation
    let score = checker.calculate_entanglement_score(1.0, 1.0, 1.0, 1.0);
    assert!(score >= 1.0 && score <= 1.1);
    
    // Test with no correlation
    let score = checker.calculate_entanglement_score(0.0, 0.0, 0.0, 0.0);
    assert_eq!(score, 0.0);
    
    // Test with mixed correlation
    let score = checker.calculate_entanglement_score(0.8, 0.6, 0.4, 0.2);
    assert!(score > 0.0 && score < 1.0);
}

#[test]
fn test_quantum_state_generation() {
    let checker = QuantumEntanglementChecker::new(0.5);
    
    // Test with score 0.25
    let state = checker.generate_quantum_state(0.25);
    assert!((state.amplitude - 0.5).abs() < 0.001);
    assert!(state.probability >= 0.0 && state.probability <= 1.0);
    
    // Test with score 1.0
    let state = checker.generate_quantum_state(1.0);
    assert!((state.amplitude - 1.0).abs() < 0.001);
    assert!((state.probability - 1.0).abs() < 0.001);
    
    // Test with score 0.0
    let state = checker.generate_quantum_state(0.0);
    assert_eq!(state.amplitude, 0.0);
    assert_eq!(state.probability, 0.0);
}

#[test]
fn test_metadata_correlation_calculation() {
    let checker = QuantumEntanglementChecker::new(0.5);
    
    // Create temporary files of different sizes
    let temp_file1 = tempfile::NamedTempFile::new().unwrap();
    let temp_file2 = tempfile::NamedTempFile::new().unwrap();
    
    fs::write(temp_file1.path(), "small").unwrap();
    fs::write(temp_file2.path(), "much larger content for testing").unwrap();
    
    let correlation = checker.calculate_metadata_correlation(
        temp_file1.path().to_str().unwrap(),
        temp_file2.path().to_str().unwrap()
    );
    
    assert!(correlation >= 0.0 && correlation <= 1.0);
}

#[test]
fn test_pattern_matching_calculation() {
    let checker = QuantumEntanglementChecker::new(0.5);
    
    // Test with identical content
    let pattern_score = checker.calculate_pattern_matching("hello world", "hello world");
    assert_eq!(pattern_score, 1.0);
    
    // Test with completely different content
    let pattern_score = checker.calculate_pattern_matching("hello", "world");
    assert_eq!(pattern_score, 0.0);
    
    // Test with partial overlap
    let pattern_score = checker.calculate_pattern_matching("hello world", "hello rust");
    assert!(pattern_score > 0.0 && pattern_score < 1.0);
}

#[test]
fn test_quantum_interference_calculation() {
    let checker = QuantumEntanglementChecker::new(0.5);
    
    // Test with identical lengths
    let interference = checker.calculate_quantum_interference("hello", "world");
    assert_eq!(interference, 1.0);
    
    // Test with different lengths
    let interference = checker.calculate_quantum_interference("hello", "hello world");
    assert!(interference >= 0.0 && interference < 1.0);
    
    // Test with empty strings
    let interference = checker.calculate_quantum_interference("", "");
    assert_eq!(interference, 1.0);
}

#[test]
fn test_entanglement_threshold_filtering() {
    let temp_dir = TempDir::new().unwrap();
    let dir_path = temp_dir.path();
    
    // Create test files
    let file1_path = dir_path.join("similar1.txt");
    let file2_path = dir_path.join("similar2.txt");
    let file3_path = dir_path.join("different.txt");
    
    fs::write(&file1_path, "very similar content for testing").unwrap();
    fs::write(&file2_path, "very similar content for testing").unwrap();
    fs::write(&file3_path, "completely different unrelated content").unwrap();
    
    let checker = QuantumEntanglementChecker::new(0.5);
    
    // Test with high threshold - should only find very similar files
    let high_threshold_results = checker.find_entangled_files(
        dir_path.to_str().unwrap(), 
        Some(0.8)
    );
    
    // Test with low threshold - should find more entanglements
    let low_threshold_results = checker.find_entangled_files(
        dir_path.to_str().unwrap(), 
        Some(0.1)
    );
    
    // Low threshold should find at least as many as high threshold
    assert!(low_threshold_results.len() >= high_threshold_results.len());
}

#[test]
fn test_entanglement_result_serialization() {
    let result = EntanglementResult {
        file1: "test1.txt".to_string(),
        file2: "test2.txt".to_string(),
        entanglement_score: 0.75,
        quantum_state: QuantumState {
            amplitude: 0.866,
            phase: 1.571,
            probability: 0.75,
        },
        correlation_details: CorrelationDetails {
            content_similarity: 0.8,
            metadata_correlation: 0.6,
            pattern_matching: 0.4,
            quantum_interference: 0.2,
        },
    };
    
    // Test serialization
    let json = serde_json::to_string(&result).unwrap();
    assert!(json.contains("test1.txt"));
    assert!(json.contains("0.75"));
    
    // Test deserialization
    let deserialized: EntanglementResult = serde_json::from_str(&json).unwrap();
    assert_eq!(deserialized.file1, "test1.txt");
    assert_eq!(deserialized.entanglement_score, 0.75);
}
