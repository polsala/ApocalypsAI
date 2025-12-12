use std::process::Command;

#[test]
fn test_echo_hello() {
    let output = Command::new("cargo")
        .args(&["run", "--quiet", "--", "hello"])
        .output()
        .expect("failed to execute process");
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Original: hello"));
    assert!(stdout.contains("Reversed: olleh"));
    assert!(stdout.contains("Whimsy: Your future is bright!"));
}

#[test]
fn test_echo_space() {
    let output = Command::new("cargo")
        .args(&["run", "--quiet", "--", " "])
        .output()
        .expect("failed to execute process");
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Original:  "));
    assert!(stdout.contains("Reversed:  "));
    assert!(stdout.contains("Whimsy: Your future is bright!"));
}

#[test]
fn test_echo_abc() {
    let output = Command::new("cargo")
        .args(&["run", "--quiet", "--", "abc"])
        .output()
        .expect("failed to execute process");
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Original: abc"));
    assert!(stdout.contains("Reversed: cba"));
    assert!(stdout.contains("Whimsy: The sky is green."));
}
