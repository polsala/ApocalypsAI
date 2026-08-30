use std::process::Command;

#[test]
fn test_to_epoch_zero() {
    let output = Command::new("cargo")
        .args(&["run", "--quiet", "--", "--to-epoch", "1970-01-01T00:00:00Z"])
        .output()
        .expect("failed to execute process");
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert_eq!(stdout.trim(), "0");
}

#[test]
fn test_from_epoch_zero() {
    let output = Command::new("cargo")
        .args(&["run", "--quiet", "--", "--from-epoch", "0"])
        .output()
        .expect("failed to execute process");
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    // chrono formats with +00:00 offset
    assert_eq!(stdout.trim(), "1970-01-01T00:00:00+00:00");
}
