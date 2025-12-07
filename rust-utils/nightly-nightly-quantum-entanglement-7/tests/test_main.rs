use nightly_quantum_entanglement_checker::compare_files;
use std::fs;
use std::io::Write;
use tempfile::NamedTempFile;

#[test]
fn test_identical_files() {
    let mut file1 = NamedTempFile::new().unwrap();
    let mut file2 = NamedTempFile::new().unwrap();
    
    let test_content = "fn main() {
    println!(\"Hello, world!\");
}"
    .to_string();
    
    writeln!(file1, "{}").unwrap();
    writeln!(file2, "{}").unwrap();
    
    let result = compare_files(
        file1.path().to_str().unwrap(),
        file2.path().to_str().unwrap()
    ).unwrap();
    
    assert!(result, "Identical files should be quantum-entangled");
}

#[test]
fn test_different_files() {
    let mut file1 = NamedTempFile::new().unwrap();
    let mut file2 = NamedTempFile::new().unwrap();
    
    writeln!(file1, "fn main() {{
    println!(\"Hello, world!\");
}}").unwrap();
    writeln!(file2, "fn main() {{
    println!(\"Goodbye, world!\");
}}").unwrap();
    
    let result = compare_files(
        file1.path().to_str().unwrap(),
        file2.path().to_str().unwrap()
    ).unwrap();
    
    assert!(!result, "Different files should not be quantum-entangled");
}

#[test]
fn test_empty_files() {
    let mut file1 = NamedTempFile::new().unwrap();
    let mut file2 = NamedTempFile::new().unwrap();
    
    // Write nothing to both files
    
    let result = compare_files(
        file1.path().to_str().unwrap(),
        file2.path().to_str().unwrap()
    ).unwrap();
    
    assert!(result, "Empty files should be quantum-entangled");
}
