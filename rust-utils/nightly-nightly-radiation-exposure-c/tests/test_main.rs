use std::process::Command;

#[test]
fn test_cli_output() {
    // Mock rationale: compile the CLI tool locally for a deterministic test
    let compile = Command::new("rustc")
        .args(&["src/main.rs", "-o", "radcalc"])
        .output()
        .expect("Failed to compile the utility");
    assert!(compile.status.success(), "Compilation failed: {}", String::from_utf8_lossy(&compile.stderr));

    // Run the compiled binary with known inputs
    let run = Command::new("./radcalc")
        .args(&["250", "0.5"])
        .output()
        .expect("Failed to execute the utility");
    assert!(run.status.success(), "Execution failed: {}", String::from_utf8_lossy(&run.stderr));
    let stdout = String::from_utf8_lossy(&run.stdout);
    assert_eq!(stdout.trim(), "2.00");
}
