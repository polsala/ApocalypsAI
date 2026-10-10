use std::process::Command;
use std::fs;
use std::io;
use std::path::Path;
use std::env;

// Mock rationale: We create temporary files and directories for testing file I/O operations.
// This is deterministic and offline, as it doesn't rely on external services or pre-existing
// files, and cleans up after itself. We also run the compiled binary as a subprocess,
// which is a standard and self-contained way to test CLI tools.

// Get the path to the compiled binary
fn get_binary_path() -> PathBuf {
    let bin_name = env!("CARGO_PKG_NAME");
    // Assuming tests are run from the project root, or `cargo test` handles path correctly.
    // For `cargo test`, the binary is usually in `target/debug/` or `target/release/`.
    // We'll use `target/debug` for tests.
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("target")
        .join("debug")
        .join(bin_name)
}

#[test]
fn test_weave_multiple_files_to_output() -> io::Result<()> {
    let test_dir = Path::new("target/test_output/test_weave_multiple_files_to_output");
    fs::create_dir_all(test_dir)?;

    let file1_path = test_dir.join("fragment1.txt");
    let file2_path = test_dir.join("fragment2.txt");
    let output_path = test_dir.join("woven_lore.txt");

    fs::write(&file1_path, "This is the first fragment.")?;
    fs::write(&file2_path, "And this is the second part.")?;

    let output = Command::new(get_binary_path())
        .arg("-i")
        .arg(&file1_path)
        .arg("-i")
        .arg(&file2_path)
        .arg("-o")
        .arg(&output_path)
        .output()?;

    assert!(output.status.success(), "Command failed with stderr: {}", String::from_utf8_lossy(&output.stderr));
    assert!(output.stderr.is_empty(), "Unexpected stderr: {}", String::from_utf8_lossy(&output.stderr));

    let expected_content = format!(
        "\n--- LORE FRAGMENT FROM: fragment1.txt ---\n\nThis is the first fragment.\n\n--- END FRAGMENT ---\n\n--- LORE FRAGMENT FROM: fragment2.txt ---\n\nAnd this is the second part.\n\n--- END FRAGMENT ---\n"
    );

    let actual_content = fs::read_to_string(&output_path)?;
    assert_eq!(actual_content, expected_content);

    fs::remove_dir_all(test_dir)?;
    Ok(())
}

#[test]
fn test_weave_single_file_to_stdout() -> io::Result<()> {
    let test_dir = Path::new("target/test_output/test_weave_single_file_to_stdout");
    fs::create_dir_all(test_dir)?;

    let file_path = test_dir.join("single_fragment.txt");
    fs::write(&file_path, "Only one story here.")?;

    let output = Command::new(get_binary_path())
        .arg("-i")
        .arg(&file_path)
        .output()?;

    assert!(output.status.success(), "Command failed with stderr: {}", String::from_utf8_lossy(&output.stderr));
    assert!(output.stderr.is_empty(), "Unexpected stderr: {}", String::from_utf8_lossy(&output.stderr));

    let expected_content = format!(
        "\n--- LORE FRAGMENT FROM: single_fragment.txt ---\n\nOnly one story here.\n\n--- END FRAGMENT ---\n"
    );

    let actual_stdout = String::from_utf8(output.stdout).unwrap();
    assert_eq!(actual_stdout, expected_content);

    fs::remove_dir_all(test_dir)?;
    Ok(())
}

#[test]
fn test_non_existent_input_file() -> io::Result<()> {
    let test_dir = Path::new("target/test_output/test_non_existent_input_file");
    fs::create_dir_all(test_dir)?;

    let non_existent_path = test_dir.join("missing.txt");
    let output_path = test_dir.join("output.txt");

    let output = Command::new(get_binary_path())
        .arg("-i")
        .arg(&non_existent_path)
        .arg("-o")
        .arg(&output_path)
        .output()?;

    assert!(!output.status.success(), "Command unexpectedly succeeded");
    let stderr = String::from_utf8(output.stderr).unwrap();
    assert!(stderr.contains("Error reading file") && (stderr.contains("No such file or directory") || stderr.contains("os error 2")), "Unexpected stderr: {}", stderr);

    assert!(!output_path.exists(), "Output file was created despite input error");

    fs::remove_dir_all(test_dir)?;
    Ok(())
}

#[test]
fn test_empty_input_file() -> io::Result<()> {
    let test_dir = Path::new("target/test_output/test_empty_input_file");
    fs::create_dir_all(test_dir)?;

    let empty_file_path = test_dir.join("empty.txt");
    let output_path = test_dir.join("output.txt");
    fs::write(&empty_file_path, "")?; // Create an empty file

    let output = Command::new(get_binary_path())
        .arg("-i")
        .arg(&empty_file_path)
        .arg("-o")
        .arg(&output_path)
        .output()?;

    assert!(output.status.success(), "Command failed with stderr: {}", String::from_utf8_lossy(&output.stderr));
    assert!(output.stderr.is_empty(), "Unexpected stderr: {}", String::from_utf8_lossy(&output.stderr));

    let expected_content = format!(
        "\n--- LORE FRAGMENT FROM: empty.txt ---\n\n\n\n--- END FRAGMENT ---\n"
    );
    let actual_content = fs::read_to_string(&output_path)?;
    assert_eq!(actual_content, expected_content);

    fs::remove_dir_all(test_dir)?;
    Ok(())
}

#[test]
fn test_no_input_files() -> io::Result<()> {
    let output = Command::new(get_binary_path())
        .output()?;

    assert!(!output.status.success(), "Command unexpectedly succeeded without input files");
    let stderr = String::from_utf8(output.stderr).unwrap();
    assert!(stderr.contains("The following required arguments were not provided:"));
    assert!(stderr.contains("--input <INPUT>"));

    Ok(())
}
