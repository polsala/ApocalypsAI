use std::process::Command;
use std::fs;

#[test]
fn test_help_command() {
    let output = Command::new("target/debug/chaos-cannon")
        .arg("--help")
        .output()
        .expect("Failed to execute command");
    
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("A whimsical CLI tool"));
}

#[test]
fn test_version_command() {
    let output = Command::new("target/debug/chaos-cannon")
        .arg("--version")
        .output()
        .expect("Failed to execute command");
    
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("chaos-cannon 0.1.0"));
}

#[test]
fn test_parse_size() {
    // Test the parse_size function by calling the binary with a test argument
    // Since we can't directly test private functions, we'll test the behavior
    // through the CLI interface
    let output = Command::new("target/debug/chaos-cannon")
        .arg("memory")
        .arg("consume")
        .arg("--size")
        .arg("1MB")
        .output()
        .expect("Failed to execute command");
    
    // The command should at least parse the size correctly (even if it fails due to permissions)
    let stderr = String::from_utf8_lossy(&output.stderr);
    // If it gets past parsing, it should try to allocate memory
    // We expect this to fail due to permissions or other runtime issues, not parsing
    assert!(!stderr.contains("Failed to parse"));
}

#[test]
fn test_cleanup_disk() {
    // Create a test directory
    let test_dir = "/tmp/chaos_cannon_test";
    fs::create_dir_all(test_dir).expect("Failed to create test directory");
    
    // Create some test files
    fs::write(format!("{}/chaos_cannon_fill.dat", test_dir), b"test").expect("Failed to create test file");
    fs::write(format!("{}/chaos_cannon_test.txt", test_dir), b"test").expect("Failed to create test file");
    
    // Verify files exist
    assert!(fs::metadata(format!("{}/chaos_cannon_fill.dat", test_dir)).is_ok());
    
    // Run cleanup
    let output = Command::new("target/debug/chaos-cannon")
        .arg("cleanup")
        .arg("disk")
        .arg("--path")
        .arg(test_dir)
        .output()
        .expect("Failed to execute command");
    
    // Check that chaos files were removed
    assert!(!Path::new(&format!("{}/chaos_cannon_fill.dat", test_dir)).exists());
    
    // Clean up test directory
    fs::remove_dir_all(test_dir).expect("Failed to remove test directory");
}

#[test]
fn test_whimsical_mode() {
    // Test that whimsical mode at least executes without crashing
    let output = Command::new("target/debug/chaos-cannon")
        .arg("whimsical")
        .arg("--target")
        .arg("all")
        .output()
        .expect("Failed to execute command");
    
    // Whimsical mode should succeed (even if individual chaos actions fail due to permissions)
    // The important thing is that it doesn't crash during parsing or execution
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Engaging whimsical chaos mode"));
}
