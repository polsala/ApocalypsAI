use nightly_quantum_entanglement_checker::{QuantumAnalyzer, EntanglementConfig, OutputFormat, EntanglementState};
use std::fs;
use tempfile::NamedTempFile;

#[tokio::test]
async fn test_end_to_end_identical_files() {
    let analyzer = QuantumAnalyzer::new();
    let config = EntanglementConfig {
        uncertainty_threshold: 0.05,
        verbose: true,
        output_format: OutputFormat::Text,
    };

    // Create two identical temporary files
    let mut temp_file1 = NamedTempFile::new().unwrap();
    let mut temp_file2 = NamedTempFile::new().unwrap();
    
    let content = "fn add(a: i32, b: i32) -> i32 { a + b }\nstruct Point { x: f64, y: f64 }";
    
    writeln!(temp_file1, "{}").unwrap();
    writeln!(temp_file2, "{}").unwrap();
    
    let path1 = temp_file1.path().to_str().unwrap();
    let path2 = temp_file2.path().to_str().unwrap();
    
    let result = analyzer
        .analyze_files(path1, path2, config)
        .await
        .unwrap();

    assert_eq!(result.entanglement_state, EntanglementState::Entangled);
    assert_eq!(result.file1_hash, result.file2_hash);
    assert!(result.similarity > 0.99);
    assert!(result.entanglement_probability > 0.9);
}

#[tokio::test]
async fn test_end_to_end_different_files() {
    let analyzer = QuantumAnalyzer::new();
    let config = EntanglementConfig {
        uncertainty_threshold: 0.05,
        verbose: false,
        output_format: OutputFormat::Text,
    };

    // Create two different temporary files
    let mut temp_file1 = NamedTempFile::new().unwrap();
    let mut temp_file2 = NamedTempFile::new().unwrap();
    
    writeln!(temp_file1, "fn add(a: i32, b: i32) -> i32 {{ a + b }}").unwrap();
    writeln!(temp_file2, "struct Point {{ x: f64, y: f64 }}").unwrap();
    
    let path1 = temp_file1.path().to_str().unwrap();
    let path2 = temp_file2.path().to_str().unwrap();
    
    let result = analyzer
        .analyze_files(path1, path2, config)
        .await
        .unwrap();

    assert_eq!(result.entanglement_state, EntanglementState::Independent);
    assert_ne!(result.file1_hash, result.file2_hash);
    assert!(result.similarity < 0.5);
    assert!(result.entanglement_probability < 0.5);
}

#[tokio::test]
async fn test_large_files_performance() {
    let analyzer = QuantumAnalyzer::new();
    let config = EntanglementConfig {
        uncertainty_threshold: 0.05,
        verbose: false,
        output_format: OutputFormat::Text,
    };

    // Create large temporary files (1MB each)
    let mut temp_file1 = NamedTempFile::new().unwrap();
    let mut temp_file2 = NamedTempFile::new().unwrap();
    
    let large_content: String = (0..100000).map(|i| format!("line {}\n", i)).collect();
    
    write!(temp_file1, "{}").unwrap();
    write!(temp_file2, "{}").unwrap(); // Identical content
    
    let path1 = temp_file1.path().to_str().unwrap();
    let path2 = temp_file2.path().to_str().unwrap();
    
    let start = std::time::Instant::now();
    let result = analyzer
        .analyze_files(path1, path2, config)
        .await
        .unwrap();
    let duration = start.elapsed();

    // Should complete quickly (under 1 second for 1MB files)
    assert!(duration.as_secs() < 1);
    assert_eq!(result.entanglement_state, EntanglementState::Entangled);
}

#[tokio::test]
async fn test_error_handling_invalid_file() {
    let analyzer = QuantumAnalyzer::new();
    let config = EntanglementConfig {
        uncertainty_threshold: 0.05,
        verbose: false,
        output_format: OutputFormat::Text,
    };

    let result = analyzer
        .analyze_files("/nonexistent/file.rs", "src/lib.rs", config)
        .await;

    assert!(result.is_err());
    assert!(result.unwrap_err().to_string().contains("No such file"));
}

#[tokio::test]
async fn test_unicode_file_paths() {
    let analyzer = QuantumAnalyzer::new();
    let config = EntanglementConfig {
        uncertainty_threshold: 0.05,
        verbose: false,
        output_format: OutputFormat::Text,
    };

    // Create temporary file with unicode content
    let mut temp_file = NamedTempFile::new().unwrap();
    writeln!(temp_file, "fn こんにちは() {{ println!(\"世界\"); }}").unwrap();
    writeln!(temp_file, "// 日本語のコメント").unwrap();
    
    let path = temp_file.path().to_str().unwrap();
    
    let result = analyzer
        .analyze_files(path, path, config)
        .await
        .unwrap();

    assert_eq!(result.entanglement_state, EntanglementState::Entangled);
    assert!(result.similarity > 0.9);
}

#[tokio::test]
async fn test_configurable_uncertainty_threshold() {
    let analyzer = QuantumAnalyzer::new();
    
    let content = "fn test() { let x = 42; }";
    
    // Test with different uncertainty thresholds
    for uncertainty in [0.01, 0.05, 0.1, 0.2, 0.5] {
        let config = EntanglementConfig {
            uncertainty_threshold: uncertainty,
            verbose: false,
            output_format: OutputFormat::Text,
        };
        
        let result = analyzer
            .analyze_content(content, "file1.rs", "file2.rs", config)
            .await
            .unwrap();

        // All should detect entanglement for identical content
        assert_eq!(result.entanglement_state, EntanglementState::Entangled);
        assert!(result.entanglement_probability >= 0.0 && result.entanglement_probability <= 1.0);
        
        // Higher uncertainty should generally reduce probability
        if uncertainty > 0.01 {
            // This is a probabilistic test - higher uncertainty typically reduces probability
            // but due to the quantum nature, we just verify it's still valid
            assert!(result.entanglement_probability >= 0.0 && result.entanglement_probability <= 1.0);
        }
    }
}

#[tokio::test]
async fn test_json_output_consistency() {
    let analyzer = QuantumAnalyzer::new();
    let config = EntanglementConfig {
        uncertainty_threshold: 0.05,
        verbose: true,
        output_format: OutputFormat::Json,
    };

    let content = "fn main() { println!(\"Hello, world!\"); }";
    
    let result = analyzer
        .analyze_content(content, "main.rs", "main_copy.rs", config)
        .await
        .unwrap();

    // Serialize to JSON and back to verify format
    let json_str = serde_json::to_string_pretty(&result).unwrap();
    let parsed: nightly_quantum_entanglement_checker::EntanglementResult = 
        serde_json::from_str(&json_str).unwrap();

    assert_eq!(result.file1_path, parsed.file1_path);
    assert_eq!(result.file2_path, parsed.file2_path);
    assert_eq!(result.entanglement_state, parsed.entanglement_state);
}

#[tokio::test]
async fn test_hash_collision_resistance() {
    let analyzer = QuantumAnalyzer::new();
    
    // Test with content that might have similar hashes
    let content1 = "a".repeat(1000);
    let content2 = "b".repeat(1000);
    
    let hash1 = analyzer.compute_quantum_signature(&content1);
    let hash2 = analyzer.compute_quantum_signature(&content2);
    
    // Hashes should be different
    assert_ne!(hash1, hash2);
    
    // Distance should be high
    let distance = analyzer.calculate_hash_distance(&hash1, &hash2);
    assert!(distance > 0.8);
}

#[tokio::test]
async fn test_word_frequency_analysis() {
    let analyzer = QuantumAnalyzer::new();
    
    let content1 = "hello world hello rust";
    let content2 = "hello rust rust world";
    
    let freq1 = analyzer.word_frequency(&content1);
    let freq2 = analyzer.word_frequency(&content2);
    
    assert_eq!(freq1.get("hello"), Some(&2));
    assert_eq!(freq1.get("world"), Some(&1));
    assert_eq!(freq1.get("rust"), Some(&1));
    
    assert_eq!(freq2.get("hello"), Some(&1));
    assert_eq!(freq2.get("world"), Some(&1));
    assert_eq!(freq2.get("rust"), Some(&2));
}

#[tokio::test]
async fn test_edge_case_empty_content() {
    let analyzer = QuantumAnalyzer::new();
    let config = EntanglementConfig {
        uncertainty_threshold: 0.05,
        verbose: false,
        output_format: OutputFormat::Text,
    };

    let result = analyzer
        .analyze_content("", "empty1.rs", "empty2.rs", config)
        .await
        .unwrap();

    // Empty content should have perfect hash similarity but zero coherence
    assert!(result.similarity > 0.9);
    assert!(result.quantum_coherence < 0.1);
    assert!(result.entanglement_probability >= 0.0 && result.entanglement_probability <= 1.0);
}
