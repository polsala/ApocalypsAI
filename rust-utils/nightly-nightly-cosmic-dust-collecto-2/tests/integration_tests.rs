use super::Args;
use clap::Parser;
use std::fs;
use std::io::Write;
use std::path::PathBuf;
use tempfile::tempdir;
use chrono::{Utc, Duration};

// Mock rationale: File system operations are inherently external. Using `tempfile` to create
// and manage temporary directories and files allows for deterministic, isolated, and offline
// testing of file system interactions without affecting the real system. This is a standard
// and robust approach for testing CLI tools that interact with the file system.

fn create_test_file(dir: &PathBuf, name: &str, content: &str, age_days: i64) -> PathBuf {
    let file_path = dir.join(name);
    let mut file = fs::File::create(&file_path).unwrap();
    file.write_all(content.as_bytes()).unwrap();

    // Set modification time to simulate age
    let now = Utc::now();
    let past_time = now - Duration::days(age_days);
    filetime::set_file_mtime(&file_path, filetime::FileTime::from_system_time(past_time.into())).unwrap();

    file_path
}

#[test]
fn test_dry_run_identifies_dust() {
    let temp_dir = tempdir().unwrap();
    let temp_path = temp_dir.path().to_path_buf();

    // Create files:
    // 1. Small, old file (should be dust)
    create_test_file(&temp_path, "dusty_log.txt", "small old content", 60);
    // 2. Large, old file (not dust by size)
    create_test_file(&temp_path, "large_old.bin", &"a".repeat(200 * 1024), 60);
    // 3. Small, new file (not dust by age)
    create_test_file(&temp_path, "new_report.txt", "fresh content", 1);
    // 4. Small, old file in a subdirectory (should be dust)
    let sub_dir = temp_path.join("sub");
    fs::create_dir(&sub_dir).unwrap();
    create_test_file(&sub_dir, "sub_dust.tmp", "sub old content", 60);

    let args = Args::parse_from(&[
        "nightly-cosmic-dust-collector",
        "--path",
        temp_path.to_str().unwrap(),
        "--max-size",
        "100", // 100 KB
        "--min-age",
        "30", // 30 days
        "--dry-run",
    ]);

    // Capture stdout to check output
    let mut buffer = Vec::new();
    let stdout = std::io::stdout();
    let _guard = gag::BufferRedirect::stdout(&mut buffer).unwrap();

    // Call the main logic (simulated)
    let result = super::main_logic(args);
    assert!(result.is_ok());

    let output = String::from_utf8(buffer).unwrap();
    // Check that dusty_log.txt and sub_dust.tmp are identified
    assert!(output.contains("dusty_log.txt"));
    assert!(output.contains("sub_dust.tmp"));
    // Check that large_old.bin and new_report.txt are NOT identified
    assert!(!output.contains("large_old.bin"));
    assert!(!output.contains("new_report.txt"));
    // Ensure no archiving message in dry run
    assert!(!output.contains("Archiving cosmic dust..."));

    // Verify files still exist (dry run)
    assert!(temp_path.join("dusty_log.txt").exists());
    assert!(temp_path.join("large_old.bin").exists());
    assert!(temp_path.join("new_report.txt").exists());
    assert!(sub_dir.join("sub_dust.tmp").exists());
}

#[test]
fn test_archive_moves_dust() {
    let temp_dir = tempdir().unwrap();
    let temp_path = temp_dir.path().to_path_buf();
    let archive_dir = temp_path.join("void_archive");

    // Create files
    let dusty_file = create_test_file(&temp_path, "dusty_to_move.txt", "old content", 60);
    let new_file = create_test_file(&temp_path, "new_file.txt", "new content", 1);

    let args = Args::parse_from(&[
        "nightly-cosmic-dust-collector",
        "--path",
        temp_path.to_str().unwrap(),
        "--max-size",
        "100",
        "--min-age",
        "30",
        "--archive-to",
        archive_dir.to_str().unwrap(),
    ]);

    // Capture stdout
    let mut buffer = Vec::new();
    let stdout = std::io::stdout();
    let _guard = gag::BufferRedirect::stdout(&mut buffer).unwrap();

    // Call the main logic
    let result = super::main_logic(args);
    assert!(result.is_ok());

    let output = String::from_utf8(buffer).unwrap();
    assert!(output.contains("Archiving cosmic dust..."));
    assert!(output.contains("Moved '" ) && output.contains("dusty_to_move.txt"));

    // Verify dusty_file is moved and no longer in original location
    assert!(!dusty_file.exists());
    assert!(archive_dir.join("dusty_to_move.txt").exists());

    // Verify new_file is untouched
    assert!(new_file.exists());
    assert!(!archive_dir.join("new_file.txt").exists());
}

#[test]
fn test_no_dust_found() {
    let temp_dir = tempdir().unwrap();
    let temp_path = temp_dir.path().to_path_buf();

    // Create only new files
    create_test_file(&temp_path, "only_new.txt", "very fresh", 1);
    create_test_file(&temp_path, "another_new.log", "just created", 5);

    let args = Args::parse_from(&[
        "nightly-cosmic-dust-collector",
        "--path",
        temp_path.to_str().unwrap(),
        "--max-size",
        "100",
        "--min-age",
        "30",
        "--dry-run",
    ]);

    let mut buffer = Vec::new();
    let stdout = std::io::stdout();
    let _guard = gag::BufferRedirect::stdout(&mut buffer).unwrap();

    let result = super::main_logic(args);
    assert!(result.is_ok());

    let output = String::from_utf8(buffer).unwrap();
    assert!(output.contains("No cosmic dust found. Your digital cosmos is pristine!"));
    assert!(!output.contains("Found "));
}

// Helper function to call the main logic, used by tests
// This is a common pattern to make `main` testable without actually exiting the process.
fn main_logic(args: Args) -> Result<(), Box<dyn std::error::Error>> {
    let now = Utc::now();
    let min_age_duration = Duration::days(args.min_age);
    let max_size_bytes = args.max_size * 1024; // Convert KB to bytes

    let mut dust_files = Vec::new();

    for entry in walkdir::WalkDir::new(&args.path).into_iter().filter_map(|e| e.ok()) {
        if entry.file_type().is_file() {
            let metadata = entry.metadata()?;
            let file_size = metadata.len();

            if file_size > max_size_bytes {
                continue;
            }

            let modified_time: DateTime<Utc> = metadata.modified()?.into();
            if now.signed_duration_since(modified_time) < min_age_duration {
                continue;
            }

            dust_files.push(entry.path().to_path_buf());
        }
    }

    if !dust_files.is_empty() && !args.dry_run {
        if let Some(archive_dir) = &args.archive_to {
            fs::create_dir_all(archive_dir)?;
            for file_path in dust_files {
                let file_name = file_path.file_name().ok_or("Could not get file name")?;
                let dest_path = archive_dir.join(file_name);
                // In tests, we don't print, just perform the action
                let _ = fs::rename(&file_path, &dest_path);
            }
        }
    }
    Ok(())
}
