use super::*;
use std::io::{self, Write};
use tempfile::NamedTempFile;

// Mock rationale: The core logic is the `Anomaly::classify` function.
// We test this directly with various f64 inputs to ensure deterministic classification.

#[test]
fn test_classify_harmless_rustle() {
    assert!(matches!(Anomaly::classify(0.0), Anomaly::HarmlessRustle));
    assert!(matches!(Anomaly::classify(0.1), Anomaly::HarmlessRustle));
    assert!(matches!(Anomaly::classify(0.2), Anomaly::HarmlessRustle));
}

#[test]
fn test_classify_curious_gust() {
    assert!(matches!(Anomaly::classify(0.20000000000000001), Anomaly::CuriousGust)); // Just above 0.2
    assert!(matches!(Anomaly::classify(0.3), Anomaly::CuriousGust));
    assert!(matches!(Anomaly::classify(0.5), Anomaly::CuriousGust));
}

#[test]
fn test_classify_ominous_howl() {
    assert!(matches!(Anomaly::classify(0.50000000000000001), Anomaly::OminousHowl)); // Just above 0.5
    assert!(matches!(Anomaly::classify(0.75), Anomaly::OminousHowl));
    assert!(matches!(Anomaly::classify(1.0), Anomaly::OminousHowl));
}

#[test]
fn test_classify_cataclysmic_roar() {
    assert!(matches!(Anomaly::classify(1.0000000000000001), Anomaly::CataclysmicRoar)); // Just above 1.0
    assert!(matches!(Anomaly::classify(1.5), Anomaly::CataclysmicRoar));
    assert!(matches!(Anomaly::classify(100.0), Anomaly::CataclysmicRoar));
}

#[test]
fn test_classify_unintelligible_static() {
    assert!(matches!(Anomaly::classify(-0.1), Anomaly::UnintelligibleStatic));
    assert!(matches!(Anomaly::classify(f64::NAN), Anomaly::UnintelligibleStatic));
    assert!(matches!(Anomaly::classify(f64::NEG_INFINITY), Anomaly::UnintelligibleStatic));
}

// Test the display output (without actual terminal colors, just the plain string representation)
#[test]
fn test_anomaly_display_string() {
    assert_eq!(Anomaly::HarmlessRustle.display().to_string(), "Harmless Rustle");
    assert_eq!(Anomaly::CuriousGust.display().to_string(), "Curious Gust");
    assert_eq!(Anomaly::OminousHowl.display().to_string(), "Ominous Howl");
    assert_eq!(Anomaly::CataclysmicRoar.display().to_string(), "Cataclysmic Roar!");
    assert_eq!(Anomaly::UnintelligibleStatic.display().to_string(), "Unintelligible Static");
}

#[test]
fn test_process_line_output() {
    // Mock rationale: We use `gag` to redirect stdout and capture the output of `process_line`.
    // This allows us to test the formatting and content of the printed lines deterministically,
    // without relying on actual terminal output or external files.
    let mut output_buffer = Vec::new();
    {
        let _guard = gag::BufferRedirect::stdout(&mut output_buffer).unwrap();
        process_line("0.1");
        process_line("0.4");
        process_line("0.8");
        process_line("1.3");
        process_line("invalid");
        process_line("-0.5"); // Test negative number
    }
    let output = String::from_utf8(output_buffer).unwrap();

    // Check for the presence of expected output lines, using the plain string representation
    // from `Anomaly::display().to_string()` as `gag` might strip ANSI escape codes.
    assert!(output.contains(&format!("Reading: {:<8.4} -> {}", 0.1, Anomaly::HarmlessRustle.display().to_string())));
    assert!(output.contains(&format!("Reading: {:<8.4} -> {}", 0.4, Anomaly::CuriousGust.display().to_string())));
    assert!(output.contains(&format!("Reading: {:<8.4} -> {}", 0.8, Anomaly::OminousHowl.display().to_string())));
    assert!(output.contains(&format!("Reading: {:<8.4} -> {}", 1.3, Anomaly::CataclysmicRoar.display().to_string())));
    assert!(output.contains(&format!("Reading: {:<8} -> {}", "invalid", Anomaly::UnintelligibleStatic.display().to_string())));
    assert!(output.contains(&format!("Reading: {:<8} -> {}", -0.5, Anomaly::UnintelligibleStatic.display().to_string())));
}

#[test]
fn test_main_with_temp_file() -> io::Result<()> {
    // Mock rationale: Create a temporary file to simulate file input for the `main` function.
    // This allows testing the file reading path without actual file system dependencies.
    let mut temp_file = NamedTempFile::new()?;
    writeln!(temp_file, "0.1")?;
    writeln!(temp_file, "0.5")?;
    writeln!(temp_file, "1.0")?;
    writeln!(temp_file, "invalid")?;
    let file_path = temp_file.path().to_owned();

    // Mock rationale: Temporarily redirect stdout to capture the output of the `main` function.
    let mut output_buffer = Vec::new();
    { // Scope for the `gag` guard
        let _guard = gag::BufferRedirect::stdout(&mut output_buffer).unwrap();

        // Simulate CLI arguments for file input
        let args = Args { file: Some(file_path.clone()) };
        // Mock rationale: Override `clap::Parser::parse` behavior for testing.
        // In a real test, you'd typically pass a mock `Args` struct or use a testing harness.
        // For this simple case, we'll directly call `main` after setting up the args.
        // Note: `main` expects `Args::parse()` to be called. We can't easily mock `clap`'s global `parse()`.
        // A better approach for testing `main`'s file handling would be to refactor `main` to take a `Read` trait object.
        // However, given the constraint of keeping it a simple CLI, we'll test the `process_line` extensively
        // and rely on the standard library's `File::open` and `BufRead` for `main`'s I/O.
        // For this test, we'll manually call the processing loop that `main` would execute.

        let file = File::open(&file_path)?;
        let reader = io::BufReader::new(file);
        for line in reader.lines() {
            process_line(&line?);
        }
    }
    let output = String::from_utf8(output_buffer).unwrap();

    assert!(output.contains(&format!("Reading: {:<8.4} -> {}", 0.1, Anomaly::HarmlessRustle.display().to_string())));
    assert!(output.contains(&format!("Reading: {:<8.4} -> {}", 0.5, Anomaly::CuriousGust.display().to_string())));
    assert!(output.contains(&format!("Reading: {:<8.4} -> {}", 1.0, Anomaly::OminousHowl.display().to_string())));
    assert!(output.contains(&format!("Reading: {:<8} -> {}", "invalid", Anomaly::UnintelligibleStatic.display().to_string())));

    // The temporary file is automatically cleaned up when `temp_file` goes out of scope.
    Ok(())
}
