use std::fs;
use std::path::Path;
use tempfile::TempDir;

// Import functions from main module
use crate::*;

#[test]
fn test_normalize_text() {
    // Mock rationale: Test text normalization for consistent comparison
    assert_eq!(normalize_text("Hello World!"), "hello world");
    assert_eq!(normalize_text("Test123"), "test123");
    assert_eq!(normalize_text(""), "");
    assert_eq!(normalize_text("UPPERCASE"), "uppercase");
    assert_eq!(normalize_text("special@#$%chars"), "specialchars");
}

#[test]
fn test_jaccard_similarity_identical() {
    // Mock rationale: Test Jaccard similarity for identical strings
    let result = calculate_jaccard_similarity("hello", "hello");
    assert_eq!(result, 1.0);
}

#[test]
fn test_jaccard_similarity_no_overlap() {
    // Mock rationale: Test Jaccard similarity for completely different strings
    let result = calculate_jaccard_similarity("abc", "xyz");
    assert_eq!(result, 0.0);
}

#[test]
fn test_jaccard_similarity_partial_overlap() {
    // Mock rationale: Test Jaccard similarity for partially overlapping strings
    let result = calculate_jaccard_similarity("abc", "bcd");
    // Intersection: b,c (2 chars), Union: a,b,c,d (4 chars) = 2/4 = 0.5
    assert_eq!(result, 0.5);
}

#[test]
fn test_frequency_similarity_identical() {
    // Mock rationale: Test frequency similarity for identical strings
    let result = calculate_frequency_similarity("hello", "hello");
    assert_eq!(result, 1.0);
}

#[test]
fn test_frequency_similarity_different() {
    // Mock rationale: Test frequency similarity for different strings
    let result = calculate_frequency_similarity("abc", "xyz");
    assert_eq!(result, 0.0);
}

#[test]
fn test_entanglement_coefficient_identical() {
    // Mock rationale: Test entanglement coefficient for identical content
    let result = calculate_entanglement_coefficient("test content", "test content");
    assert_eq!(result, 1.0);
}

#[test]
fn test_entanglement_coefficient_empty() {
    // Mock rationale: Test entanglement coefficient for empty strings
    assert_eq!(calculate_entanglement_coefficient("", ""), 1.0);
    assert_eq!(calculate_entanglement_coefficient("test", ""), 0.0);
    assert_eq!(calculate_entanglement_coefficient("", "test"), 0.0);
}

#[test]
fn test_entanglement_coefficient_similar() {
    // Mock rationale: Test entanglement coefficient for similar content
    let result1 = calculate_entanglement_coefficient("hello world", "hello earth");
    let result2 = calculate_entanglement_coefficient("abc", "xyz");
    
    assert!(result1 > result2, "Similar content should have higher coefficient");
    assert!(result1 > 0.0, "Similar content should have positive coefficient");
}

#[test]
fn test_matches_pattern_wildcard() {
    // Mock rationale: Test pattern matching with wildcards
    assert!(matches_pattern(Path::new("test.rs"), "*.rs"));
    assert!(matches_pattern(Path::new("test.py"), "*.py"));
    assert!(matches_pattern(Path::new("main.rs"), "*main*"));
    assert!(matches_pattern(Path::new("test.rs"), "test.*"));
    assert!(matches_pattern(Path::new("anyfile"), "*"));
    
    assert!(!matches_pattern(Path::new("test.rs"), "*.py"));
    assert!(!matches_pattern(Path::new("main.rs"), "test.*"));
}

#[test]
fn test_find_files_empty_directory() {
    // Mock rationale: Test file finding in empty directory
    let temp_dir = TempDir::new().unwrap();
    let files = find_files(temp_dir.path(), "*", 10).unwrap();
    assert_eq!(files.len(), 0);
}

#[test]
fn test_find_files_with_pattern() {
    // Mock rationale: Test file finding with specific pattern
    let temp_dir = TempDir::new().unwrap();
    
    // Create test files
    fs::write(temp_dir.path().join("test.rs"), "fn main() {}").unwrap();
    fs::write(temp_dir.path().join("test.py"), "def main(): pass").unwrap();
    fs::write(temp_dir.path().join("main.rs"), "fn main() {}").unwrap();
    
    let rust_files = find_files(temp_dir.path(), "*.rs", 10).unwrap();
    let py_files = find_files(temp_dir.path(), "*.py", 10).unwrap();
    
    assert_eq!(rust_files.len(), 2);
    assert_eq!(py_files.len(), 1);
}

#[test]
fn test_calculate_char_frequency() {
    // Mock rationale: Test character frequency calculation
    let freq = calculate_char_frequency("aabbcc");
    
    assert_eq!(freq.get(&'a'), Some(&0.3333333333333333));
    assert_eq!(freq.get(&'b'), Some(&0.3333333333333333));
    assert_eq!(freq.get(&'c'), Some(&0.3333333333333333));
    assert_eq!(freq.get(&'d'), None);
}

#[test]
fn test_format_quantum_level() {
    // Mock rationale: Test quantum level formatting
    assert_eq!(format_quantum_level(0.95), "0.95 (ULTRA-STRONG) ⚛️");
    assert_eq!(format_quantum_level(0.75), "0.75 (STRONG) 🚀");
    assert_eq!(format_quantum_level(0.55), "0.55 (MODERATE) 🌀");
    assert_eq!(format_quantum_level(0.35), "0.35 (WEAK) 💫");
    assert_eq!(format_quantum_level(0.15), "0.15 (TRACE) ✨");
}

#[test]
fn test_entanglement_coefficient_real_code() {
    // Mock rationale: Test with real code snippets
    let code1 = r#"
fn main() {
    println!("Hello, world!");
}
"#;
    
    let code2 = r#"
fn main() {
    println!("Hello, universe!");
}
"#;
    
    let code3 = r#"
def main():
    print("Hello, world!")
"#;
    
    let coeff1 = calculate_entanglement_coefficient(code1, code2);
    let coeff2 = calculate_entanglement_coefficient(code1, code3);
    
    // Similar Rust code should have higher coefficient than different languages
    assert!(coeff1 > coeff2);
    assert!(coeff1 > 0.3); // Should detect some similarity
}

#[test]
fn test_entanglement_coefficient_duplicate_code() {
    // Mock rationale: Test with duplicate code detection
    let original = r#"
struct User {
    name: String,
    age: u32,
}

impl User {
    fn new(name: String, age: u32) -> Self {
        Self { name, age }
    }
}
"#;
    
    let duplicate = r#"
struct Person {
    name: String,
    age: u32,
}

impl Person {
    fn new(name: String, age: u32) -> Self {
        Self { name, age }
    }
}
"#;
    
    let different = r#"
fn calculate_sum(a: i32, b: i32) -> i32 {
    a + b
}
"#;
    
    let coeff1 = calculate_entanglement_coefficient(original, duplicate);
    let coeff2 = calculate_entanglement_coefficient(original, different);
    
    // Similar structure should have higher coefficient
    assert!(coeff1 > coeff2);
    assert!(coeff1 > 0.4); // Should detect structural similarity
}

#[test]
fn test_threshold_filtering() {
    // Mock rationale: Test that threshold filtering works correctly
    let temp_dir = TempDir::new().unwrap();
    
    // Create test files with varying similarity
    fs::write(temp_dir.path().join("similar1.rs"), "fn test() { let x = 1; }",).unwrap();
    fs::write(temp_dir.path().join("similar2.rs"), "fn test() { let x = 2; }",).unwrap();
    fs::write(temp_dir.path().join("different.rs"), "fn main() { println!(\"hello\"); }",).unwrap();
    
    let temp_dir2 = TempDir::new().unwrap();
    fs::write(temp_dir2.path().join("similar3.rs"), "fn test() { let x = 3; }",).unwrap();
    fs::write(temp_dir2.path().join("unrelated.rs"), "struct Config;",).unwrap();
    
    // Test with high threshold - should find fewer matches
    let results_high_threshold = analyze_entanglement(
        temp_dir.path(),
        temp_dir2.path(),
        "*.rs",
        0.8,
        10,
        false,
    ).unwrap();
    
    // Test with low threshold - should find more matches
    let results_low_threshold = analyze_entanglement(
        temp_dir.path(),
        temp_dir2.path(),
        "*.rs",
        0.3,
        10,
        false,
    ).unwrap();
    
    // Low threshold should find at least as many matches as high threshold
    assert!(results_low_threshold.len() >= results_high_threshold.len());
}

#[test]
fn test_empty_directories() {
    // Mock rationale: Test behavior with empty directories
    let temp_dir1 = TempDir::new().unwrap();
    let temp_dir2 = TempDir::new().unwrap();
    
    let results = analyze_entanglement(
        temp_dir1.path(),
        temp_dir2.path(),
        "*",
        0.5,
        10,
        false,
    ).unwrap();
    
    assert_eq!(results.len(), 0);
}

#[test]
fn test_single_file_comparison() {
    // Mock rationale: Test comparison of single files
    let temp_dir = TempDir::new().unwrap();
    let file_path = temp_dir.path().join("test.rs");
    fs::write(&file_path, "fn main() {}",).unwrap();
    
    let temp_dir2 = TempDir::new().unwrap();
    let file_path2 = temp_dir2.path().join("test.rs");
    fs::write(&file_path2, "fn main() {}",).unwrap();
    
    let results = analyze_entanglement(
        temp_dir.path(),
        temp_dir2.path(),
        "*.rs",
        0.5,
        10,
        false,
    ).unwrap();
    
    assert_eq!(results.len(), 1);
    assert_eq!(results[0].coefficient, 1.0);
}

#[test]
fn test_max_depth_limitation() {
    // Mock rationale: Test that max_depth parameter limits directory traversal
    let temp_dir = TempDir::new().unwrap();
    
    // Create nested directory structure
    let deep_dir = temp_dir.path().join("level1").join("level2").join("level3");
    fs::create_dir_all(&deep_dir).unwrap();
    
    fs::write(temp_dir.path().join("root.rs"), "root file",).unwrap();
    fs::write(deep_dir.join("deep.rs"), "deep file",).unwrap();
    
    // Test with max_depth = 1 (should only find root.rs)
    let files = find_files(temp_dir.path(), "*.rs", 1).unwrap();
    assert_eq!(files.len(), 1);
    assert!(files[0].file_name().unwrap() == "root.rs");
    
    // Test with max_depth = 3 (should find both files)
    let files = find_files(temp_dir.path(), "*.rs", 3).unwrap();
    assert_eq!(files.len(), 2);
}

#[test]
fn test_error_handling_invalid_directory() {
    // Mock rationale: Test error handling for invalid directories
    let result = find_files(Path::new("/nonexistent/path"), "*", 10);
    assert!(result.is_err());
}

#[test]
fn test_unicode_support() {
    // Mock rationale: Test handling of Unicode characters
    let text1 = "Hello 世界 🌍";
    let text2 = "Hello 世界 🌎";
    
    let coeff = calculate_entanglement_coefficient(text1, text2);
    assert!(coeff > 0.5); // Should detect similarity despite Unicode
    assert!(coeff < 1.0); // But not identical due to different emoji
}

#[test]
fn test_large_file_handling() {
    // Mock rationale: Test handling of larger text content
    let large_text1 = "a".repeat(10000) + "unique_marker_1" + &"b".repeat(10000);
    let large_text2 = "a".repeat(10000) + "unique_marker_2" + &"b".repeat(10000);
    
    let coeff = calculate_entanglement_coefficient(&large_text1, &large_text2);
    assert!(coeff > 0.8); // Should detect high similarity
}

#[test]
fn test_case_insensitive_comparison() {
    // Mock rationale: Test that comparison is case-insensitive
    let text1 = "Hello World";
    let text2 = "HELLO WORLD";
    let text3 = "hello world";
    
    let coeff1 = calculate_entanglement_coefficient(text1, text2);
    let coeff2 = calculate_entanglement_coefficient(text1, text3);
    
    // Should be very similar (if not identical) due to normalization
    assert!((coeff1 - coeff2).abs() < 0.1);
}

#[test]
fn test_special_characters_handling() {
    // Mock rationale: Test handling of special characters and symbols
    let code1 = r#"
fn test() {
    let result = a + b * c;
    if result > 100 {
        println!("Large result: {}", result);
    }
}
"#;
    
    let code2 = r#"
fn calculate() {
    let output = x + y * z;
    if output > 100 {
        println!("Large output: {}", output);
    }
}
"#;
    
    let coeff = calculate_entanglement_coefficient(code1, code2);
    assert!(coeff > 0.4); // Should detect structural similarity
}

#[test]
fn test_performance_consistency() {
    // Mock rationale: Test that results are consistent across multiple runs
    let temp_dir = TempDir::new().unwrap();
    let temp_dir2 = TempDir::new().unwrap();
    
    fs::write(temp_dir.path().join("test1.rs"), "fn test() { let x = 1; }",).unwrap();
    fs::write(temp_dir2.path().join("test2.rs"), "fn test() { let x = 2; }",).unwrap();
    
    let result1 = analyze_entanglement(
        temp_dir.path(),
        temp_dir2.path(),
        "*.rs",
        0.3,
        10,
        false,
    ).unwrap();
    
    let result2 = analyze_entanglement(
        temp_dir.path(),
        temp_dir2.path(),
        "*.rs",
        0.3,
        10,
        false,
    ).unwrap();
    
    // Should get same number of results
    assert_eq!(result1.len(), result2.len());
    
    // Should get same coefficients (within floating point precision)
    for (r1, r2) in result1.iter().zip(result2.iter()) {
        assert!((r1.coefficient - r2.coefficient).abs() < 0.001);
    }
}

#[test]
fn test_format_quantum_level_edge_cases() {
    // Mock rationale: Test edge cases for quantum level formatting
    assert_eq!(format_quantum_level(1.0), "1.00 (ULTRA-STRONG) ⚛️");
    assert_eq!(format_quantum_level(0.0), "0.00 (TRACE) ✨");
    assert_eq!(format_quantum_level(0.7), "0.70 (STRONG) 🚀");
    assert_eq!(format_quantum_level(0.5), "0.50 (MODERATE) 🌀");
    assert_eq!(format_quantum_level(0.3), "0.30 (WEAK) 💫");
}

#[test]
fn test_read_file_content() {
    // Mock rationale: Test file reading functionality
    let temp_dir = TempDir::new().unwrap();
    let file_path = temp_dir.path().join("test.txt");
    fs::write(&file_path, "test content",).unwrap();
    
    let content = read_file_content(&file_path).unwrap();
    assert_eq!(content, "test content");
}

#[test]
fn test_read_file_content_nonexistent() {
    // Mock rationale: Test error handling for nonexistent files
    let result = read_file_content(Path::new("/nonexistent/file.txt"));
    assert!(result.is_err());
}

#[test]
fn test_parallel_processing() {
    // Mock rationale: Test that parallel processing produces same results as sequential
    // This is implicitly tested by the consistency test above
    // The parallel implementation should be deterministic
    let temp_dir = TempDir::new().unwrap();
    let temp_dir2 = TempDir::new().unwrap();
    
    // Create multiple files to ensure parallel processing is used
    for i in 0..10 {
        fs::write(
            temp_dir.path().join(format!("test{}.rs", i)),
            format!("fn test{}() {{ let x = {}; }}", i, i),
        ).unwrap();
        fs::write(
            temp_dir2.path().join(format!("test{}.rs", i)),
            format!("fn test{}() {{ let x = {}; }}", i, i + 1),
        ).unwrap();
    }
    
    let results = analyze_entanglement(
        temp_dir.path(),
        temp_dir2.path(),
        "*.rs",
        0.0,
        10,
        false,
    ).unwrap();
    
    // Should find 10 matches (each file compared with each file)
    assert_eq!(results.len(), 10);
    
    // All coefficients should be reasonable (not NaN or negative)
    for result in &results {
        assert!(result.coefficient >= 0.0 && result.coefficient <= 1.0);
        assert!(!result.coefficient.is_nan());
    }
}
