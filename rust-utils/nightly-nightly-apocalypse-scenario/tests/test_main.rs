use std::process::Command;
use std::str;

#[test]
fn test_deterministic_output() {
    let output = Command::new("cargo")
        .args(&["run", "--quiet", "--", "--seed", "42"])
        .output()
        .expect("Failed to execute command");
    assert!(output.status.success());
    let stdout = str::from_utf8(&output.stdout).unwrap();
    let expected = "Title: The Rise of the Machines
Cause: AI takeover
Tip: Find a sturdy shelter and stock up on water.
";
    assert_eq!(stdout, expected);
}
