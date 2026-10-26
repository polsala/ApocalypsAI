use std::io::{self, Cursor, Write};
use std::process::{Command, Stdio};
use std::fs;

// Helper function to run the main binary with given arguments and input
fn run_de_noiser(args: &[&str], input: &str) -> String {
    let mut cmd = Command::new(env!("CARGO_BIN_EXE_nightly-echo-de-noiser"))
        .args(args)
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .spawn()
        .expect("Failed to spawn de-noiser process");

    let stdin = cmd.stdin.as_mut().expect("Failed to open stdin");
    stdin.write_all(input.as_bytes()).expect("Failed to write to stdin");
    drop(stdin); // Close stdin to signal EOF

    let output = cmd.wait_with_output().expect("Failed to wait for de-noiser process");

    assert!(output.status.success(), "De-noiser process failed: {:?}", output);
    String::from_utf8(output.stdout).expect("Output not valid UTF-8")
}

#[test]
fn test_no_filtering() {
    // Mock rationale: Testing the CLI behavior by piping input and capturing output.
    // This simulates real-world usage without needing complex file mocks.
    let input = "Line 1\nLine 2\nLine 3\n";
    let output = run_de_noiser(&[], input);
    assert_eq!(output, input);
}

#[test]
fn test_filter_single_pattern() {
    // Mock rationale: Testing the CLI behavior by piping input and capturing output.
    let input = "Important message\nNoise line here\nAnother important message\n";
    let output = run_de_noiser(&["-p", "Noise line"], input);
    assert_eq!(output, "Important message\nAnother important message\n");
}

#[test]
fn test_filter_multiple_patterns() {
    // Mock rationale: Testing the CLI behavior by piping input and capturing output.
    let input = "Msg 1\nNoise A\nMsg 2\nNoise B\nMsg 3\n";
    let output = run_de_noiser(&["-p", "Noise A", "-p", "Noise B"], input);
    assert_eq!(output, "Msg 1\nMsg 2\nMsg 3\n");
}

#[test]
fn test_deduplicate_consecutive_lines() {
    // Mock rationale: Testing the CLI behavior by piping input and capturing output.
    let input = "A\nA\nB\nC\nC\nC\nD\n";
    let output = run_de_noiser(&["-d"], input);
    assert_eq!(output, "A\nB\nC\nD\n");
}

#[test]
fn test_deduplicate_non_consecutive_lines() {
    // Mock rationale: Testing the CLI behavior by piping input and capturing output.
    let input = "A\nB\nA\nC\n";
    let output = run_de_noiser(&["-d"], input);
    assert_eq!(output, "A\nB\nA\nC\n"); // 'A' appears twice as they are not consecutive
}

#[test]
fn test_combine_pattern_and_deduplicate() {
    // Mock rationale: Testing the CLI behavior by piping input and capturing output.
    let input = "Important\nNoise\nImportant\nImportant\nAnother Noise\nFinal Message\n";
    let output = run_de_noiser(&["-p", "Noise", "-d"], input);
    // Expected output: 'Noise' is filtered. The first 'Important' is printed. The second 'Important' is a consecutive duplicate of the first *printed* line, so it's filtered. 'Another Noise' is not filtered by the 'Noise' pattern and is not a duplicate of the last printed line. 'Final Message' is not filtered.
    assert_eq!(output, "Important\nAnother Noise\nFinal Message\n");
}

#[test]
fn test_filter_empty_lines() {
    // Mock rationale: Testing the CLI behavior by piping input and capturing output.
    let input = "Line 1\n\nLine 2\n\n\nLine 3\n";
    let output = run_de_noiser(&["-p", "^$"], input);
    assert_eq!(output, "Line 1\nLine 2\nLine 3\n");
}

#[test]
fn test_read_from_file() {
    // Mock rationale: Creating a temporary file to simulate file input.
    let temp_dir = tempfile::tempdir().expect("Failed to create temp dir");
    let file_path = temp_dir.path().join("test_input.log");
    fs::write(&file_path, "Line 1\nNoise\nLine 2\n").expect("Failed to write temp file");

    let output = Command::new(env!("CARGO_BIN_EXE_nightly-echo-de-noiser"))
        .args(&[file_path.to_str().unwrap(), "-p", "Noise"])
        .stdout(Stdio::piped())
        .output()
        .expect("Failed to execute de-noiser");

    assert!(output.status.success());
    assert_eq!(String::from_utf8(output.stdout).unwrap(), "Line 1\nLine 2\n");

    temp_dir.close().expect("Failed to clean up temp dir");
}
