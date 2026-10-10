use super::*;
use std::fs::{self, File};
use std::io::Write;
use tempfile::tempdir;
use chrono::{Utc, Duration};

// Mock rationale: We create temporary files and directories to simulate a file system
// without relying on actual user files or external resources. This ensures tests are
// deterministic and isolated. We also control file modification times for decay status testing.

#[test]
fn test_calculate_sha256() -> io::Result<()> {
    let dir = tempdir()?;
    let file_path = dir.path().join("test_file.txt");
    fs::write(&file_path, "hello world")?;
    let expected_checksum = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e7304336293879ecb";
    assert_eq!(calculate_sha256(&file_path)?, expected_checksum);
    Ok(())
}

#[test]
fn test_decay_status_from_timestamp() {
    let now = Utc::now();

    // Pristine: less than 1 year old
    let pristine_time = now - Duration::days(100);
    assert_eq!(DecayStatus::from_timestamp(pristine_time), DecayStatus::Pristine);

    // Weathered: 1 to 5 years old
    let weathered_time = now - Duration::days(365 * 2); // 2 years old
    assert_eq!(DecayStatus::from_timestamp(weathered_time), DecayStatus::Weathered);

    // Decaying: 5 to 10 years old
    let decaying_time = now - Duration::days(365 * 7); // 7 years old
    assert_eq!(DecayStatus::from_timestamp(decaying_time), DecayStatus::Decaying);

    // Dust: more than 10 years old
    let dust_time = now - Duration::days(365 * 12); // 12 years old
    assert_eq!(DecayStatus::from_timestamp(dust_time), DecayStatus::Dust);
}

#[test]
fn test_generate_relic_registry() -> io::Result<()> {
    let dir = tempdir()?;
    let input_dir = dir.path().join("relics");
    fs::create_dir(&input_dir)?;

    // Create a pristine file (less than 1 year old)
    let pristine_file_path = input_dir.join("pristine.txt");
    fs::write(&pristine_file_path, "fresh data")?;
    // Set modification time to recent (within 1 year)
    let now = Utc::now();
    let one_month_ago = now - Duration::days(30);
    filetime::set_file_mtime(&pristine_file_path, filetime::FileTime::from_system_time(one_month_ago.into()))?;

    // Create a weathered file (2 years old)
    let weathered_file_path = input_dir.join("old_log.txt");
    fs::write(&weathered_file_path, "old log entries")?;
    let two_years_ago = now - Duration::days(365 * 2);
    filetime::set_file_mtime(&weathered_file_path, filetime::FileTime::from_system_time(two_years_ago.into()))?;

    // Create a decaying file (7 years old)
    let decaying_file_path = input_dir.join("ancient_config.cfg");
    fs::write(&decaying_file_path, "config v1")?;
    let seven_years_ago = now - Duration::days(365 * 7);
    filetime::set_file_mtime(&decaying_file_path, filetime::FileTime::from_system_time(seven_years_ago.into()))?;

    // Create a dust file (12 years old)
    let dust_file_path = input_dir.join("forgotten_memo.doc");
    fs::write(&dust_file_path, "top secret memo")?;
    let twelve_years_ago = now - Duration::days(365 * 12);
    filetime::set_file_mtime(&dust_file_path, filetime::FileTime::from_system_time(twelve_years_ago.into()))?;

    // Create a subdirectory with another file
    let sub_dir = input_dir.join("sub_dir");
    fs::create_dir(&sub_dir)?;
    let sub_file_path = sub_dir.join("nested.txt");
    fs::write(&sub_file_path, "nested data")?;
    filetime::set_file_mtime(&sub_file_path, filetime::FileTime::from_system_time(one_month_ago.into()))?; // Pristine

    let registry = generate_relic_registry(&input_dir)?;

    assert_eq!(registry.len(), 5); // 4 files in root, 1 in sub_dir

    // Check specific entries
    let pristine_entry = registry.iter().find(|e| e.filename == "pristine.txt").unwrap();
    assert_eq!(pristine_entry.decay_status, DecayStatus::Pristine);
    assert_eq!(pristine_entry.checksum_sha256, calculate_sha256(&pristine_file_path)?);

    let weathered_entry = registry.iter().find(|e| e.filename == "old_log.txt").unwrap();
    assert_eq!(weathered_entry.decay_status, DecayStatus::Weathered);

    let decaying_entry = registry.iter().find(|e| e.filename == "ancient_config.cfg").unwrap();
    assert_eq!(decaying_entry.decay_status, DecayStatus::Decaying);

    let dust_entry = registry.iter().find(|e| e.filename == "forgotten_memo.doc").unwrap();
    assert_eq!(dust_entry.decay_status, DecayStatus::Dust);

    let nested_entry = registry.iter().find(|e| e.filename == "nested.txt").unwrap();
    assert_eq!(nested_entry.decay_status, DecayStatus::Pristine);
    assert!(nested_entry.path.to_string_lossy().contains("sub_dir"));

    Ok(())
}

#[test]
fn test_main_cli_output() -> io::Result<()> {
    let dir = tempdir()?;
    let input_dir = dir.path().join("test_input");
    fs::create_dir(&input_dir)?;
    fs::write(input_dir.join("file1.txt"), "content1")?;
    fs::write(input_dir.join("file2.txt"), "content2")?;

    let output_file = dir.path().join("test_registry.json");

    // Temporarily set command line arguments
    let args = vec![
        "nightly-relic-registry-cli".to_string(),
        "--input-dir".to_string(),
        input_dir.to_string_lossy().to_string(),
        "--output-file".to_string(),
        output_file.to_string_lossy().to_string(),
    ];
    // Mock rationale: We capture stdout/stderr to verify the CLI output without
    // actually printing to the console during tests. This makes the test deterministic.
    let original_args = std::env::args().collect::<Vec<String>>();
    std::env::set_var("RUST_BACKTRACE", "0"); // Suppress backtrace for cleaner test output
    std::env::set_args(args);

    let result = std::panic::catch_unwind(|| {
        main()
    });

    // Restore original arguments
    std::env::set_args(original_args);

    assert!(result.is_ok(), "main function panicked: {:?}", result.err());
    assert!(result.unwrap().is_ok(), "main function returned an error");

    assert!(output_file.exists());
    let content = fs::read_to_string(&output_file)?;
    let registry: Vec<RelicEntry> = serde_json::from_str(&content)?;

    assert_eq!(registry.len(), 2);
    assert!(content.contains("file1.txt"));
    assert!(content.contains("file2.txt"));
    assert!(content.contains("Pristine")); // Default decay status for newly created files

    Ok(())
}

#[test]
fn test_main_cli_invalid_input_dir() -> io::Result<()> {
    let dir = tempdir()?;
    let non_existent_dir = dir.path().join("non_existent");
    let output_file = dir.path().join("test_registry.json");

    let args = vec![
        "nightly-relic-registry-cli".to_string(),
        "--input-dir".to_string(),
        non_existent_dir.to_string_lossy().to_string(),
        "--output-file".to_string(),
        output_file.to_string_lossy().to_string(),
    ];
    let original_args = std::env::args().collect::<Vec<String>>();
    std::env::set_args(args);

    // Mock rationale: We expect the program to exit with an error code,
    // so we catch the panic that `std::process::exit` causes in tests.
    let result = std::panic::catch_unwind(|| {
        main().unwrap(); // main() returns Result, unwrap() will panic on Err
    });

    std::env::set_args(original_args);

    assert!(result.is_err()); // Expect a panic due to exit(1)
    Ok(())
}
