use nightly_rust_resource_tracker::resource_tracker::{ResourceTracker, Resource};
use std::fs;
use std::process::Command;

#[test]
fn test_cli_add_and_list() {
    // Cleanup any existing file
    let _ = fs::remove_file("resources.json");
    
    // Add a resource via CLI
    let output = Command::new(env!("CARGO"))
        .args(&[
            "run",
            "--bin",
            "nightly-rust-resource-tracker",
            "--",
            "add",
            "--name",
            "Water",
            "--quantity",
            "100",
            "--category",
            "Essentials",
        ])
        .output()
        .expect("Failed to execute command");
    
    assert!(output.status.success());
    
    // Verify the file was created
    assert!(fs::metadata("resources.json").is_ok());
    
    // List resources via CLI
    let output = Command::new(env!("CARGO"))
        .args(&[
            "run",
            "--bin",
            "nightly-rust-resource-tracker",
            "--",
            "list",
        ])
        .output()
        .expect("Failed to execute command");
    
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Water"));
    assert!(stdout.contains("100"));
    
    // Cleanup
    let _ = fs::remove_file("resources.json");
}

#[test]
fn test_cli_update_quantity() {
    // Cleanup any existing file
    let _ = fs::remove_file("resources.json");
    
    // Add a resource
    let output = Command::new(env!("CARGO"))
        .args(&[
            "run",
            "--bin",
            "nightly-rust-resource-tracker",
            "--",
            "add",
            "--name",
            "Food",
            "--quantity",
            "50",
            "--category",
            "Essentials",
        ])
        .output()
        .expect("Failed to execute command");
    
    assert!(output.status.success());
    
    // Update quantity
    let output = Command::new(env!("CARGO"))
        .args(&[
            "run",
            "--bin",
            "nightly-rust-resource-tracker",
            "--",
            "update",
            "--name",
            "Food",
            "--quantity",
            "75",
        ])
        .output()
        .expect("Failed to execute command");
    
    assert!(output.status.success());
    
    // Verify the update
    let tracker = ResourceTracker::load().unwrap();
    assert_eq!(tracker.get_resource("Food").unwrap().quantity, 75);
    
    // Cleanup
    let _ = fs::remove_file("resources.json");
}

#[test]
fn test_cli_remove_resource() {
    // Cleanup any existing file
    let _ = fs::remove_file("resources.json");
    
    // Add a resource
    let output = Command::new(env!("CARGO"))
        .args(&[
            "run",
            "--bin",
            "nightly-rust-resource-tracker",
            "--",
            "add",
            "--name",
            "Weapons",
            "--quantity",
            "10",
            "--category",
            "Defense",
        ])
        .output()
        .expect("Failed to execute command");
    
    assert!(output.status.success());
    
    // Remove resource
    let output = Command::new(env!("CARGO"))
        .args(&[
            "run",
            "--bin",
            "nightly-rust-resource-tracker",
            "--",
            "remove",
            "--name",
            "Weapons",
        ])
        .output()
        .expect("Failed to execute command");
    
    assert!(output.status.success());
    
    // Verify the removal
    let tracker = ResourceTracker::load().unwrap();
    assert!(tracker.get_resource("Weapons").is_none());
    
    // Cleanup
    let _ = fs::remove_file("resources.json");
}

#[test]
fn test_cli_export_json() {
    // Cleanup any existing files
    let _ = fs::remove_file("resources.json");
    let _ = fs::remove_file("export.json");
    
    // Add a resource
    let output = Command::new(env!("CARGO"))
        .args(&[
            "run",
            "--bin",
            "nightly-rust-resource-tracker",
            "--",
            "add",
            "--name",
            "Medicine",
            "--quantity",
            "25",
            "--category",
            "Medical",
        ])
        .output()
        .expect("Failed to execute command");
    
    assert!(output.status.success());
    
    // Export to JSON
    let output = Command::new(env!("CARGO"))
        .args(&[
            "run",
            "--bin",
            "nightly-rust-resource-tracker",
            "--",
            "export",
            "--format",
            "json",
            "--output",
            "export.json",
        ])
        .output()
        .expect("Failed to execute command");
    
    assert!(output.status.success());
    
    // Verify the export file exists and contains data
    assert!(fs::metadata("export.json").is_ok());
    let content = fs::read_to_string("export.json").unwrap();
    assert!(content.contains("Medicine"));
    assert!(content.contains("25"));
    
    // Cleanup
    let _ = fs::remove_file("resources.json");
    let _ = fs::remove_file("export.json");
}

#[test]
fn test_cli_export_csv() {
    // Cleanup any existing files
    let _ = fs::remove_file("resources.json");
    let _ = fs::remove_file("export.csv");
    
    // Add a resource
    let output = Command::new(env!("CARGO"))
        .args(&[
            "run",
            "--bin",
            "nightly-rust-resource-tracker",
            "--",
            "add",
            "--name",
            "Tools",
            "--quantity",
            "15",
            "--category",
            "Equipment",
        ])
        .output()
        .expect("Failed to execute command");
    
    assert!(output.status.success());
    
    // Export to CSV
    let output = Command::new(env!("CARGO"))
        .args(&[
            "run",
            "--bin",
            "nightly-rust-resource-tracker",
            "--",
            "export",
            "--format",
            "csv",
            "--output",
            "export.csv",
        ])
        .output()
        .expect("Failed to execute command");
    
    assert!(output.status.success());
    
    // Verify the export file exists and contains data
    assert!(fs::metadata("export.csv").is_ok());
    let content = fs::read_to_string("export.csv").unwrap();
    assert!(content.contains("Tools"));
    assert!(content.contains("15"));
    
    // Cleanup
    let _ = fs::remove_file("resources.json");
    let _ = fs::remove_file("export.csv");
}

#[test]
fn test_interactive_mode() {
    // Cleanup any existing file
    let _ = fs::remove_file("resources.json");
    
    // Test that interactive mode starts without crashing
    let output = Command::new(env!("CARGO"))
        .args(&[
            "run",
            "--bin",
            "nightly-rust-resource-tracker",
            "--",
            "interactive",
        ])
        .output()
        .expect("Failed to execute command");
    
    // Interactive mode should start successfully (even if we can't fully test it here)
    assert!(output.status.success() || output.status.code() == Some(0));
    
    // Cleanup
    let _ = fs::remove_file("resources.json");
}
