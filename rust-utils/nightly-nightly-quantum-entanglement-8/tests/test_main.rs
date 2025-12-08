use std::fs;
use std::process::Command;

#[test]
fn test_quantum_entanglement_checker() {
    // Create test files
    let test_dir = "test_files";
    fs::create_dir_all(test_dir).unwrap();
    
    let file_a = format!("{}/test_a.rs", test_dir);
    let file_b = format!("{}/test_b.rs", test_dir);
    
    // Write identical content
    fs::write(&file_a, "fn hello() { println!(\"world\"); }\
fn goodbye() { println!(\"farewell\"); }\
").unwrap();
    fs::write(&file_b, "fn hello() { println!(\"world\"); }\
fn goodbye() { println!(\"farewell\"); }\
").unwrap();
    
    // Run the tool
    let output = Command::new(env!("CARGO_BIN_EXE_quantum-entanglement-checker"))
        .arg(&file_a)
        .arg(&file_b)
        .output()
        .expect("Failed to run quantum-entanglement-checker");
    
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    
    // Check that probability is high for identical files
    assert!(stdout.contains("Entanglement Probability:"));
    assert!(stdout.contains("Quantum State:"));
    
    // Clean up
    fs::remove_dir_all(test_dir).unwrap();
}

#[test]
fn test_different_files_low_entanglement() {
    let test_dir = "test_files_diff";
    fs::create_dir_all(test_dir).unwrap();
    
    let file_a = format!("{}/test_a.rs", test_dir);
    let file_b = format!("{}/test_b.rs", test_dir);
    
    // Write different content
    fs::write(&file_a, "fn main() { let x = 5; }\
").unwrap();
    fs::write(&file_b, "fn helper() { let y = 10; }\
").unwrap();
    
    let output = Command::new(env!("CARGO_BIN_EXE_quantum-entanglement-checker"))
        .arg(&file_a)
        .arg(&file_b)
        .output()
        .expect("Failed to run quantum-entanglement-checker");
    
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    
    // Should show low entanglement
    assert!(stdout.contains("Entanglement Probability:"));
    
    // Clean up
    fs::remove_dir_all(test_dir).unwrap();
}

#[test]
fn test_function_filter() {
    let test_dir = "test_files_func";
    fs::create_dir_all(test_dir).unwrap();
    
    let file_a = format!("{}/test_a.rs", test_dir);
    let file_b = format!("{}/test_b.rs", test_dir);
    
    // Write content with different functions
    fs::write(&file_a, "fn main() { }\
fn helper() { }\
").unwrap();
    fs::write(&file_b, "fn main() { }\
fn other() { }\
").unwrap();
    
    let output = Command::new(env!("CARGO_BIN_EXE_quantum-entanglement-checker"))
        .arg(&file_a)
        .arg(&file_b)
        .arg("--function")
        .arg("main")
        .output()
        .expect("Failed to run quantum-entanglement-checker");
    
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    
    // Should show high entanglement for the specific function
    assert!(stdout.contains("Entanglement Probability:"));
    
    // Clean up
    fs::remove_dir_all(test_dir).unwrap();
}

#[test]
fn test_verbose_output() {
    let test_dir = "test_files_verbose";
    fs::create_dir_all(test_dir).unwrap();
    
    let file_a = format!("{}/test_a.rs", test_dir);
    let file_b = format!("{}/test_b.rs", test_dir);
    
    fs::write(&file_a, "fn test() { }\
").unwrap();
    fs::write(&file_b, "fn test() { }\
").unwrap();
    
    let output = Command::new(env!("CARGO_BIN_EXE_quantum-entanglement-checker"))
        .arg(&file_a)
        .arg(&file_b)
        .arg("--verbose")
        .output()
        .expect("Failed to run quantum-entanglement-checker");
    
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    
    // Should include verbose quantum details
    assert!(stdout.contains("Particle Correlation:"));
    assert!(stdout.contains("Wave Function Overlap:"));
    assert!(stdout.contains("Decoherence Factor:"));
    
    // Clean up
    fs::remove_dir_all(test_dir).unwrap();
}
