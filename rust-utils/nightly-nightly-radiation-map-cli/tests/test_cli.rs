use std::process::Command;
use std::fs::write;
use std::env::temp_dir;

#[test]
fn cli_outputs_colored_table() {
    let csv_path = temp_dir().join("cli_test.csv");
    let _ = write(&csv_path, "Safe,0.3\nDanger,6.5\n");
    // The binary name is inferred by Cargo during integration tests
    let output = Command::new(env!("CARGO_BIN_EXE_radiomap"))
        .arg(csv_path.to_str().unwrap())
        .output()
        .expect("failed to execute radiomap binary");
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Safe"));
    assert!(stdout.contains("Danger"));
    // Verify ANSI color codes are present
    assert!(stdout.contains("\x1b[32m"));
    assert!(stdout.contains("\x1b[31m"));
}
