use nightly_quantum_entanglement_checker::*;
use std::fs;
use std::path::Path;

#[test]
fn test_hash_content() {
    let checker = QuantumChecker::new();
    
    let content = "fn main() { println!(\"Hello, world!\"); }";
    let hash = checker.hash_content(content);
    
    // SHA-256 should produce a 64-character hex string
    assert_eq!(hash.len(), 64);
    assert!(hash.chars().all(|c| c.is_ascii_hexdigit()));
}

#[test]
fn test_hash_uniqueness() {
    let checker = QuantumChecker::new();
    
    let content1 = "fn main() { println!(\"Hello!\"); }";
    let content2 = "fn main() { println!(\"World!\"); }";
    
    let hash1 = checker.hash_content(content1);
    let hash2 = checker.hash_content(content2);
    
    // Different content should produce different hashes
    assert_ne!(hash1, hash2);
}

#[test]
fn test_identical_content_similarity() {
    let checker = QuantumChecker::new();
    
    let content = "fn test() { let x = 5; }";
    let hash1 = checker.hash_content(content);
    let hash2 = checker.hash_content(content);
    
    let similarity = checker.calculate_similarity(&hash1, &hash2);
    
    // Identical content should have 100% similarity
    assert_eq!(similarity, 1.0);
}

#[test]
fn test_different_content_similarity() {
    let checker = QuantumChecker::new();
    
    let content1 = "fn main() { println!(\"Hello\"); }";
    let content2 = "fn test() { assert_eq!(1, 1); }";
    
    let hash1 = checker.hash_content(content1);
    let hash2 = checker.hash_content(content2);
    
    let similarity = checker.calculate_similarity(&hash1, &hash2);
    
    // Different content should have lower similarity
    assert!(similarity < 1.0);
    assert!(similarity >= 0.0);
}

#[test]
fn test_entanglement_detection() {
    let checker = QuantumChecker::new();
    
    // Test with identical content
    let content = "fn calculate() -> i32 { 42 }";
    let result = checker.check_entanglement(content, content);
    
    assert!(result.is_entangled);
    assert_eq!(result.similarity_percentage, 100.0);
    assert!(!result.quantum_message.is_empty());
}

#[test]
fn test_no_entanglement() {
    let checker = QuantumChecker::new();
    
    // Test with completely different content
    let content1 = "fn main() { println!(\"Rust\"); }";
    let content2 = "def python_function(): return 'Python'";
    
    let result = checker.check_entanglement(content1, content2);
    
    // Should not be entangled due to very different content
    assert!(!result.is_entangled);
    assert!(result.similarity_percentage < 50.0);
}

#[test]
fn test_entanglement_level_classification() {
    let checker = QuantumChecker::new();
    
    // Test high entanglement
    let content = "fn test() { let x = 5; let y = 10; }";
    let result = checker.check_entanglement(content, content);
    let level = checker.determine_entanglement_level(1.0);
    
    assert_eq!(level, "High Entanglement");
    
    // Test medium entanglement
    let level = checker.determine_entanglement_level(0.6);
    assert_eq!(level, "Medium Entanglement");
    
    // Test low entanglement
    let level = checker.determine_entanglement_level(0.3);
    assert_eq!(level, "Low Entanglement");
    
    // Test no entanglement
    let level = checker.determine_entanglement_level(0.1);
    assert_eq!(level, "No Entanglement");
}

#[test]
fn test_quantum_signature_generation() {
    let checker = QuantumChecker::new();
    
    let hash1 = "a1b2c3d4e5f67890123456789012345678901234567890123456789012345678";
    let hash2 = "f6e5d4c3b2a10987654321098765432109876543210987654321098765432109";
    
    let signature = checker.generate_quantum_signature(hash1, hash2);
    
    assert!(signature.starts_with("Q:"));
    assert!(signature.ends_with(":"));
    assert!(signature.len() > 10);
}

#[test]
fn test_report_generation() {
    let checker = QuantumChecker::new();
    
    let content1 = "fn add(a: i32, b: i32) -> i32 { a + b }";
    let content2 = "fn subtract(a: i32, b: i32) -> i32 { a - b }";
    
    let report = checker.generate_report(content1, content2);
    
    assert!(!report.result.hash1.is_empty());
    assert!(!report.result.hash2.is_empty());
    assert!(report.result.similarity_percentage >= 0.0);
    assert!(report.result.similarity_percentage <= 100.0);
    assert!(!report.result.quantum_message.is_empty());
    assert!(!report.entanglement_level.is_empty());
    assert!(!report.quantum_signature.is_empty());
}

#[test]
fn test_file_reading() {
    // Create a temporary test file
    let test_content = "fn test_file() { println!(\"test\"); }";
    let test_file = "test_temp.rs";
    
    fs::write(test_file, test_content).expect("Failed to create test file");
    
    // Test reading the file
    let result = utils::read_file(test_file);
    assert!(result.is_ok());
    assert_eq!(result.unwrap(), test_content);
    
    // Clean up
    fs::remove_file(test_file).expect("Failed to remove test file");
}

#[test]
fn test_empty_content() {
    let checker = QuantumChecker::new();
    
    let result = checker.check_entanglement("", "");
    
    assert!(result.is_entangled);
    assert_eq!(result.similarity_percentage, 100.0);
}

#[test]
fn test_similar_but_different_content() {
    let checker = QuantumChecker::new();
    
    let content1 = "fn calculate(x: i32) -> i32 { x * 2 }";
    let content2 = "fn compute(y: i32) -> i32 { y * 2 }";
    
    let result = checker.check_entanglement(content1, content2);
    
    // Should have some similarity but not be identical
    assert!(result.similarity_percentage > 0.0);
    assert!(result.similarity_percentage < 100.0);
}

#[test]
fn test_quantum_message_generation() {
    let checker = QuantumChecker::new();
    
    // Test entangled message
    let message = checker.generate_quantum_message(0.9, true);
    assert!(message.contains("quantum"));
    assert!(message.contains("entanglement"));
    
    // Test non-entangled message
    let message = checker.generate_quantum_message(0.1, false);
    assert!(message.contains("quantum"));
    assert!(message.contains("separate"));
}
