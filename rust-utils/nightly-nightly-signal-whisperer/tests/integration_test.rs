use std::process::Command;
use std::io::Write;
use tempfile::NamedTempFile; // For creating temporary files

// Mock rationale: Using tempfile::NamedTempFile to simulate file input and std::process::Command to run the CLI tool
// allows for deterministic, offline testing of the command-line interface without actual file system side effects
// beyond temporary test files, which are cleaned up automatically.

#[test]
fn test_no_input() {
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-signal-whisperer"))
        .output()
        .expect("Failed to execute command");

    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Whisper: No signal detected. The void is silent."));
}

#[test]
fn test_keyword_detection() {
    let mut file = NamedTempFile::new().expect("Failed to create temp file");
    writeln!(file, "This is a test signal. We need shelter. SOS!").expect("Failed to write to temp file");
    let file_path = file.path().to_str().unwrap();

    let output = Command::new(env!("CARGO_BIN_EXE_nightly-signal-whisperer"))
        .arg("-f")
        .arg(file_path)
        .arg("-k")
        .arg("shelter,SOS")
        .output()
        .expect("Failed to execute command");

    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Whisper: A faint echo of a forgotten broadcast detected! Keyword 'shelter' found."));
    assert!(stdout.contains("Whisper: A faint echo of a forgotten broadcast detected! Keyword 'SOS' found."));
}

#[test]
fn test_repeating_sequence_detection_banana() {
    let mut file = NamedTempFile::new().expect("Failed to create temp file");
    writeln!(file, "banana").expect("Failed to write to temp file");
    let file_path = file.path().to_str().unwrap();

    let output = Command::new(env!("CARGO_BIN_EXE_nightly-signal-whisperer"))
        .arg("-f")
        .arg(file_path)
        .arg("-m")
        .arg("2") // min_repeat_len = 2
        .output()
        .expect("Failed to execute command");

    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Whisper: A rhythmic pulse detected! Repeating sequence 'ana' found 2 times."));
    assert!(!stdout.contains("Repeating sequence 'an'")); // Should be filtered out by 'ana'
    assert!(!stdout.contains("Repeating sequence 'na'")); // Should be filtered out by 'ana'
}

#[test]
fn test_character_frequency_analysis() {
    let mut file = NamedTempFile::new().expect("Failed to create temp file");
    writeln!(file, "AAAAABBC").expect("Failed to write to temp file"); // A is 62.5%
    let file_path = file.path().to_str().unwrap();

    let output = Command::new(env!("CARGO_BIN_EXE_nightly-signal-whisperer"))
        .arg("-f")
        .arg(file_path)
        .arg("-t")
        .arg("60.0") // freq_threshold = 60%
        .output()
        .expect("Failed to execute command");

    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Whisper: An unusual resonance! Character 'A' appears with 62.50% frequency."));
    assert!(!stdout.contains("Character 'B'")); // B is 25%
    assert!(!stdout.contains("Character 'C'")); // C is 12.5%
}

#[test]
fn test_all_features_combined() {
    let mut file = NamedTempFile::new().expect("Failed to create temp file");
    writeln!(file, "Hello World! Hello again! SOS SOS SOS! XXXXX").expect("Failed to write to temp file");
    let file_path = file.path().to_str().unwrap();

    let output = Command::new(env!("CARGO_BIN_EXE_nightly-signal-whisperer"))
        .arg("-f")
        .arg(file_path)
        .arg("-k")
        .arg("SOS,World")
        .arg("-m")
        .arg("3")
        .arg("-t")
        .arg("20.0") // X is 5/28 ~ 17.8%, S is 6/28 ~ 21.4%
        .output()
        .expect("Failed to execute command");

    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Keyword 'SOS' found."));
    assert!(stdout.contains("Keyword 'World' found."));
    assert!(stdout.contains("Repeating sequence 'SOS' found 3 times."));
    assert!(stdout.contains("Repeating sequence 'Hello' found 2 times."));
    assert!(stdout.contains("Character 'S' appears with")); // Should be > 20%
    assert!(!stdout.contains("Character 'X'")); // Should be < 20%
}

#[test]
fn test_stdin_input() {
    let input = "This is a test. SOS!";
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-signal-whisperer"))
        .arg("-k")
        .arg("SOS")
        .stdin(input.as_bytes())
        .output()
        .expect("Failed to execute command");

    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Keyword 'SOS' found."));
}
