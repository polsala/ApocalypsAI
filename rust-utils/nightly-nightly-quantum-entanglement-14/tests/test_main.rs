use std::fs;
use std::path::Path;
use tempfile::NamedTempFile;

// Mock rationale: We use temporary files to create deterministic test cases
// without relying on external files or network resources

#[test]
fn test_identical_files_are_entangled() {
    let temp1 = NamedTempFile::new().unwrap();
    let temp2 = NamedTempFile::new().unwrap();
    
    let content = "fn main() { println!(\"Hello, world!\"); }";
    fs::write(temp1.path(), content).unwrap();
    fs::write(temp2.path(), content).unwrap();
    
    let checker = quantum_engine::QuantumEntanglementChecker::new();
    let report = checker.check_entanglement(
        temp1.path().to_str().unwrap(),
        temp2.path().to_str().unwrap(),
        0.0,
    ).unwrap();
    
    assert!(report.is_entangled, "Identical files should be entangled");
    assert!(report.entanglement_level > 0.8, "Entanglement level should be high for identical files");
    assert_eq!(report.coherence_state, "Highly Coherent");
}

#[test]
fn test_completely_different_files_are_not_entangled() {
    let temp1 = NamedTempFile::new().unwrap();
    let temp2 = NamedTempFile::new().unwrap();
    
    let content1 = "fn main() { println!(\"Hello, world!\"); }";
    let content2 = "class Program { static void Main() { Console.WriteLine(\"Hello\"); } }";
    
    fs::write(temp1.path(), content1).unwrap();
    fs::write(temp2.path(), content2).unwrap();
    
    let checker = quantum_engine::QuantumEntanglementChecker::new();
    let report = checker.check_entanglement(
        temp1.path().to_str().unwrap(),
        temp2.path().to_str().unwrap(),
        0.0,
    ).unwrap();
    
    assert!(!report.is_entangled, "Completely different files should not be entangled");
    assert!(report.entanglement_level < 0.4, "Entanglement level should be low for different files");
    assert_eq!(report.coherence_state, "Decohered");
}

#[test]
fn test_similar_files_are_partially_entangled() {
    let temp1 = NamedTempFile::new().unwrap();
    let temp2 = NamedTempFile::new().unwrap();
    
    let content1 = "fn calculate(x: i32) -> i32 { x * 2 }";
    let content2 = "fn calculate(y: i32) -> i32 { y * 2 }";
    
    fs::write(temp1.path(), content1).unwrap();
    fs::write(temp2.path(), content2).unwrap();
    
    let checker = quantum_engine::QuantumEntanglementChecker::new();
    let report = checker.check_entanglement(
        temp1.path().to_str().unwrap(),
        temp2.path().to_str().unwrap(),
        0.0,
    ).unwrap();
    
    assert!(report.is_entangled, "Similar files should be entangled");
    assert!(report.entanglement_level > 0.4 && report.entanglement_level < 0.8, 
           "Entanglement level should be moderate for similar files");
    assert_eq!(report.coherence_state, "Partially Coherent");
}

#[test]
fn test_decoherence_reduces_entanglement() {
    let temp1 = NamedTempFile::new().unwrap();
    let temp2 = NamedTempFile::new().unwrap();
    
    let content1 = "fn test() { let x = 42; }";
    let content2 = "fn test() { let x = 42; }";
    
    fs::write(temp1.path(), content1).unwrap();
    fs::write(temp2.path(), content2).unwrap();
    
    let checker = quantum_engine::QuantumEntanglementChecker::new();
    
    let report_without_decoherence = checker.check_entanglement(
        temp1.path().to_str().unwrap(),
        temp2.path().to_str().unwrap(),
        0.0,
    ).unwrap();
    
    let report_with_decoherence = checker.check_entanglement(
        temp1.path().to_str().unwrap(),
        temp2.path().to_str().unwrap(),
        0.3,
    ).unwrap();
    
    assert!(report_with_decoherence.entanglement_level < report_without_decoherence.entanglement_level,
           "Decoherence should reduce entanglement level");
    assert_eq!(report_with_decoherence.decoherence_factor, 0.3);
}

#[test]
fn test_decoherence_cannot_be_negative_or_greater_than_one() {
    let temp1 = NamedTempFile::new().unwrap();
    let temp2 = NamedTempFile::new().unwrap();
    
    let content = "fn main() {}";
    fs::write(temp1.path(), content).unwrap();
    fs::write(temp2.path(), content).unwrap();
    
    let checker = quantum_engine::QuantumEntanglementChecker::new();
    
    // Test that decoherence is clamped to 0.0-1.0 range
    let report = checker.check_entanglement(
        temp1.path().to_str().unwrap(),
        temp2.path().to_str().unwrap(),
        1.5, // This should be clamped to 1.0
    ).unwrap();
    
    // With maximum decoherence, files should not be entangled
    assert!(!report.is_entangled, "Maximum decoherence should prevent entanglement");
    assert_eq!(report.decoherence_factor, 1.0);
}

#[test]
fn test_quantum_signatures_are_deterministic() {
    let temp1 = NamedTempFile::new().unwrap();
    let temp2 = NamedTempFile::new().unwrap();
    
    let content = "fn test() {}";
    fs::write(temp1.path(), content).unwrap();
    fs::write(temp2.path(), content).unwrap();
    
    let checker = quantum_engine::QuantumEntanglementChecker::new();
    
    let report1 = checker.check_entanglement(
        temp1.path().to_str().unwrap(),
        temp2.path().to_str().unwrap(),
        0.0,
    ).unwrap();
    
    let report2 = checker.check_entanglement(
        temp1.path().to_str().unwrap(),
        temp2.path().to_str().unwrap(),
        0.0,
    ).unwrap();
    
    // Quantum signatures should be deterministic (same content = same signature)
    assert_eq!(report1.quantum_signature_1, report2.quantum_signature_1);
    assert_eq!(report1.quantum_signature_2, report2.quantum_signature_2);
}

#[test]
fn test_missing_file_returns_error() {
    let checker = quantum_engine::QuantumEntanglementChecker::new();
    
    let result = checker.check_entanglement(
        "nonexistent1.rs",
        "nonexistent2.rs",
        0.0,
    );
    
    assert!(result.is_err(), "Should return error for missing files");
}

#[test]
fn test_report_generation() {
    let temp1 = NamedTempFile::new().unwrap();
    let temp2 = NamedTempFile::new().unwrap();
    let temp_output = NamedTempFile::new().unwrap();
    
    let content = "fn main() { println!(\"test\"); }";
    fs::write(temp1.path(), content).unwrap();
    fs::write(temp2.path(), content).unwrap();
    
    let checker = quantum_engine::QuantumEntanglementChecker::new();
    let report = checker.check_entanglement(
        temp1.path().to_str().unwrap(),
        temp2.path().to_str().unwrap(),
        0.0,
    ).unwrap();
    
    let json = serde_json::to_string_pretty(&report).unwrap();
    fs::write(temp_output.path(), json).unwrap();
    
    let loaded_json = fs::read_to_string(temp_output.path()).unwrap();
    let loaded_report: quantum_engine::EntanglementReport = 
        serde_json::from_str(&loaded_json).unwrap();
    
    assert_eq!(report.file1_name, loaded_report.file1_name);
    assert_eq!(report.file2_name, loaded_report.file2_name);
    assert_eq!(report.is_entangled, loaded_report.is_entangled);
}
