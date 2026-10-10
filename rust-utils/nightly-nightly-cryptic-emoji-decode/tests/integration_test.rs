#[test]
fn test_decode_known() {
    // Run the binary with a known emoji sequence
    let output = std::process::Command::new("cargo")
        .args(&["run", "--quiet", "--", "🚀 🌕"])
        .output()
        .expect("failed to execute cargo run");
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert_eq!(stdout.trim(), "launch moon");
}

#[test]
fn test_decode_unknown() {
    // Run the binary with an emoji that is not in the dictionary
    let output = std::process::Command::new("cargo")
        .args(&["run", "--quiet", "--", "🦄"])
        .output()
        .expect("failed to execute cargo run");
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert_eq!(stdout.trim(), "[unknown]");
}
