use nightly_temporal_text_purifier::{purify_text, calculate_signature};
use std::fs;
use std::io::{self, Write};
use tempfile::NamedTempFile;

// Mock rationale: Using tempfile::NamedTempFile for creating temporary files
// simulates file system interactions without relying on external services or network.
// This ensures tests are deterministic and offline.

#[test]
fn test_purify_text_basic() {
    let input = "  Hello World  \n\nLine 2\n  Line 3  \n";
    let expected = "Hello World\nLine 2\nLine 3";
    assert_eq!(purify_text(input), expected);
}

#[test]
fn test_purify_text_empty_lines() {
    let input = "\n\nLine 1\n\n\nLine 2\n";
    let expected = "Line 1\nLine 2";
    assert_eq!(purify_text(input), expected);
}

#[test]
fn test_purify_text_duplicate_lines() {
    let input = "Line 1\nLine 1\nLine 2\nLine 2\nLine 2\nLine 3";
    let expected = "Line 1\nLine 2\nLine 3";
    assert_eq!(purify_text(input), expected);
}

#[test]
fn test_purify_text_mixed_duplicates_and_empty() {
    let input = "  First Line  \n\nFirst Line\n  Second Line  \nSecond Line\n\nThird Line\nThird Line\n";
    let expected = "First Line\nSecond Line\nThird Line";
    assert_eq!(purify_text(input), expected);
}

#[test]
fn test_purify_text_all_empty_or_whitespace() {
    let input = "   \n\n \t \n";
    let expected = "";
    assert_eq!(purify_text(input), expected);
}

#[test]
fn test_calculate_signature_consistent() {
    let content1 = "Hello World\nThis is a test.";
    let content2 = "Hello World\nThis is a test.";
    let content3 = "Hello World\nThis is a different test.";

    let sig1 = calculate_signature(content1);
    let sig2 = calculate_signature(content2);
    let sig3 = calculate_signature(content3);

    assert_eq!(sig1, sig2);
    assert_ne!(sig1, sig3);
}

#[test]
fn test_end_to_end_purification_and_signature() -> io::Result<()> {
    // Mock rationale: Using tempfile::NamedTempFile for creating temporary files
    // simulates file system interactions without relying on external services or network.
    // This ensures tests are deterministic and offline.
    let mut input_file = NamedTempFile::new()?;
    writeln!(input_file, "  Line One  ")?;
    writeln!(input_file, "")?;
    writeln!(input_file, "Line One")?;
    writeln!(input_file, "  Line Two  ")?;
    writeln!(input_file, "Line Two")?;
    writeln!(input_file, "Line Three")?;
    input_file.flush()?;

    let input_path = input_file.path().to_path_buf();

    let input_content = fs::read_to_string(&input_path)?;
    let purified_content = purify_text(&input_content);
    let signature = calculate_signature(&purified_content);

    let expected_purified = "Line One\nLine Two\nLine Three";
    let expected_signature = calculate_signature(expected_purified);

    assert_eq!(purified_content, expected_purified);
    assert_eq!(signature, expected_signature);

    Ok(())
}
