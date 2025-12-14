use std::process::Command;
use std::fs;
use std::io::Write;
use tempfile::tempdir;

// Mock rationale: We create a temporary directory and populate it with dummy files
// to simulate a real file system for testing. This ensures tests are deterministic,
// isolated, and do not depend on external resources or modify the user's actual files.

#[test]
fn test_relic_sorter_basic_categorization() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    // Create dummy files with minimal content for infer to detect types
    fs::write(path.join("ancient_wisdom.txt"), "This is an old scroll.")?;
    fs::write(path.join("sunset_view.jpg"), [0xFF, 0xD8, 0xFF, 0xE0, 0x00, 0x10, 0x4A, 0x46, 0x49, 0x46, 0x00, 0x01, 0x01, 0x00, 0x00, 0x01, 0x00, 0x01, 0x00, 0x00])?; // Minimal JPEG header
    fs::write(path.join("battle_hymn.mp3"), [0x49, 0x44, 0x33, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])?; // Minimal ID3v2 header for MP3
    fs::write(path.join("secret_plans.zip"), [0x50, 0x4B, 0x03, 0x04, 0x14, 0x00, 0x00, 0x00, 0x08, 0x00])?; // Minimal ZIP header
    fs::write(path.join("launch_script.sh"), "#!/bin/bash\necho 'Hello'")?;
    fs::write(path.join("unknown_blob"), "some random data")?;
    fs::write(path.join("config.json"), "{ \"key\": \"value\" }")?;
    fs::write(path.join("another_text.log"), "A log entry.")?;

    // Run the command
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-relic-sorter"))
        .arg("--path")
        .arg(path)
        .output()?;

    let stdout = String::from_utf8_lossy(&output.stdout);
    let stderr = String::from_utf8_lossy(&output.stderr);

    println!("STDOUT:\n{}", stdout);
    println!("STDERR:\n{}", stderr);

    assert!(output.status.success());
    assert!(stderr.is_empty());

    // Assertions for categories and file counts
    assert!(stdout.contains("Ancient Scrolls (Text): 2 relics found")); // txt, log
    assert!(stdout.contains(format!("  - {}", path.join("ancient_wisdom.txt").display()).as_str()));
    assert!(stdout.contains(format!("  - {}", path.join("another_text.log").display()).as_str()));

    assert!(stdout.contains("Bundled Secrets (Archive): 1 relics found"));
    assert!(stdout.contains(format!("  - {}", path.join("secret_plans.zip").display()).as_str()));

    assert!(stdout.contains("Digital Artifacts (Data/Code): 1 relics found"));
    assert!(stdout.contains(format!("  - {}", path.join("config.json").display()).as_str()));

    assert!(stdout.contains("Forbidden Runes (Executable/Script): 1 relics found"));
    assert!(stdout.contains(format!("  - {}", path.join("launch_script.sh").display()).as_str()));

    assert!(stdout.contains("Sonic Echoes (Audio): 1 relics found"));
    assert!(stdout.contains(format!("  - {}", path.join("battle_hymn.mp3").display()).as_str()));

    assert!(stdout.contains("Unidentified Relic: 1 relics found"));
    assert!(stdout.contains(format!("  - {}", path.join("unknown_blob").display()).as_str()));

    assert!(stdout.contains("Visual Glyphs (Image): 1 relics found"));
    assert!(stdout.contains(format!("  - {}", path.join("sunset_view.jpg").display()).as_str()));

    Ok(())
}

#[test]
fn test_relic_sorter_verbose_output() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    fs::write(path.join("test.txt"), "hello")?;

    let output = Command::new(env!("CARGO_BIN_EXE_nightly-relic-sorter"))
        .arg("--path")
        .arg(path)
        .arg("--verbose")
        .output()?;

    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(output.status.success());
    assert!(stdout.contains(format!("  {} -> Ancient Scrolls (Text)", path.join("test.txt").display()).as_str()));

    Ok(())
}

#[test]
fn test_relic_sorter_non_existent_path() -> Result<(), Box<dyn std::error::Error>> {
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-relic-sorter"))
        .arg("--path")
        .arg("/non/existent/path/to/relics")
        .output()?;

    let stderr = String::from_utf8_lossy(&output.stderr);
    assert!(!output.status.success());
    assert!(stderr.contains("Error: Path '/non/existent/path/to/relics' does not exist."));

    Ok(())
}

#[test]
fn test_relic_sorter_path_is_file() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let file_path = dir.path().join("a_file.txt");
    fs::write(&file_path, "content")?;

    let output = Command::new(env!("CARGO_BIN_EXE_nightly-relic-sorter"))
        .arg("--path")
        .arg(&file_path)
        .output()?;

    let stderr = String::from_utf8_lossy(&output.stderr);
    assert!(!output.status.success());
    assert!(stderr.contains(format!("Error: Path '{}' is not a directory.", file_path.display()).as_str()));

    Ok(())
}
