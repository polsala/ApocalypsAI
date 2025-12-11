use assert_cmd::Command;
use predicates::prelude::*;
use std::env;
use std::fs;
use std::path::PathBuf;
use tempfile::tempdir; // For creating temporary directories

// Mock rationale:
// - Environment variables: The PATH environment variable is system-dependent and can change.
//   Tests will mock it by setting a specific PATH value for the test execution context.
// - Filesystem existence: Checking if paths exist involves interacting with the actual filesystem,
//   which is non-deterministic and can have side effects. Tests will use temporary directories
//   and files to simulate existent and non-existent paths in a controlled, isolated environment.

#[test]
fn test_dry_run_no_changes() {
    let dir = tempdir().unwrap();
    let path1 = dir.path().join("bin1");
    let path2 = dir.path().join("bin2");
    fs::create_dir(&path1).unwrap();
    fs::create_dir(&path2).unwrap();

    let original_path = env::join_paths(&[path1.clone(), path2.clone()]).unwrap();

    let mut cmd = Command::cargo_bin("path-purifier").unwrap();
    cmd.env("PATH", original_path.to_string_lossy().to_string())
        .arg("--dry-run")
        .assert()
        .success()
        .stdout(predicates::str::contains(format!("--- Original PATH ---\n{}", original_path.to_string_lossy())))
        .stdout(predicates::str::contains(format!("--- Proposed Clean PATH ---\n{}", original_path.to_string_lossy())))
        .stdout(predicates::str::contains("No entries removed."));
}

#[test]
fn test_dry_run_with_duplicates() {
    let dir = tempdir().unwrap();
    let path1 = dir.path().join("bin1");
    let path2 = dir.path().join("bin2");
    fs::create_dir(&path1).unwrap();
    fs::create_dir(&path2).unwrap();

    let path_delimiter = if cfg!(windows) { ";" } else { ":" };
    let original_path_str = format!(
        "{0}{1}{2}{1}{0}",
        path1.to_string_lossy(),
        path_delimiter,
        path2.to_string_lossy()
    );
    let expected_clean_path_str = format!(
        "{0}{1}{2}",
        path1.to_string_lossy(),
        path_delimiter,
        path2.to_string_lossy()
    );

    let mut cmd = Command::cargo_bin("path-purifier").unwrap();
    cmd.env("PATH", original_path_str.clone())
        .arg("--dry-run")
        .assert()
        .success()
        .stdout(predicates::str::contains(format!("--- Original PATH ---\n{}", original_path_str)))
        .stdout(predicates::str::contains(format!("--- Proposed Clean PATH ---\n{}", expected_clean_path_str)))
        .stdout(predicates::str::contains(format!("--- Removed Entries ---\n- {}", path1.to_string_lossy())));
}

#[test]
fn test_dry_run_with_non_existent_paths() {
    let dir = tempdir().unwrap();
    let existent_path = dir.path().join("existent_bin");
    let non_existent_path = dir.path().join("non_existent_bin"); // This path will not be created
    fs::create_dir(&existent_path).unwrap();

    let path_delimiter = if cfg!(windows) { ";" } else { ":" };
    let original_path_str = format!(
        "{0}{1}{2}",
        existent_path.to_string_lossy(),
        path_delimiter,
        non_existent_path.to_string_lossy()
    );
    let expected_clean_path_str = format!("{}", existent_path.to_string_lossy());

    let mut cmd = Command::cargo_bin("path-purifier").unwrap();
    cmd.env("PATH", original_path_str.clone())
        .arg("--dry-run")
        .assert()
        .success()
        .stdout(predicates::str::contains(format!("--- Original PATH ---\n{}", original_path_str)))
        .stdout(predicates::str::contains(format!("--- Proposed Clean PATH ---\n{}", expected_clean_path_str)))
        .stdout(predicates::str::contains(format!("--- Removed Entries ---\n- {}", non_existent_path.to_string_lossy())));
}

#[test]
fn test_apply_mode() {
    let dir = tempdir().unwrap();
    let path1 = dir.path().join("bin1");
    let path2 = dir.path().join("bin2");
    fs::create_dir(&path1).unwrap();
    fs::create_dir(&path2).unwrap();

    let path_delimiter = if cfg!(windows) { ";" } else { ":" };
    let original_path_str = format!(
        "{0}{1}{2}{1}{0}",
        path1.to_string_lossy(),
        path_delimiter,
        path2.to_string_lossy()
    );
    let expected_clean_path_str = format!(
        "{0}{1}{2}",
        path1.to_string_lossy(),
        path_delimiter,
        path2.to_string_lossy()
    );

    let mut cmd = Command::cargo_bin("path-purifier").unwrap();
    cmd.env("PATH", original_path_str.clone())
        .arg("--apply")
        .assert()
        .success()
        .stdout(format!("{}\n", expected_clean_path_str)); // Ensure it prints exactly the new path followed by a newline
}

#[test]
fn test_interactive_mode_keep_all() {
    let dir = tempdir().unwrap();
    let path1 = dir.path().join("bin1");
    let path2 = dir.path().join("bin2");
    let non_existent_path = dir.path().join("non_existent_bin");
    fs::create_dir(&path1).unwrap();
    fs::create_dir(&path2).unwrap();

    let path_delimiter = if cfg!(windows) { ";" } else { ":" };
    let original_path_str = format!(
        "{0}{1}{2}{1}{0}{1}{3}",
        path1.to_string_lossy(),
        path_delimiter,
        path2.to_string_lossy(),
        non_existent_path.to_string_lossy()
    );
    let expected_clean_path_str = format!(
        "{0}{1}{2}",
        path1.to_string_lossy(),
        path_delimiter,
        path2.to_string_lossy()
    ); // If user keeps duplicate, it's still only added once. Non-existent is kept.

    let mut cmd = Command::cargo_bin("path-purifier").unwrap();
    cmd.env("PATH", original_path_str.clone())
        .arg("--interactive")
        .write_stdin("y\ny\n") // Respond 'y' to both prompts (duplicate, non-existent)
        .assert()
        .success()
        .stdout(predicates::str::contains(format!("--- Original PATH ---\n{}", original_path_str)))
        .stdout(predicates::str::contains(format!("--- Proposed Clean PATH ---\n{}", expected_clean_path_str)))
        .stdout(predicates::str::contains("No entries removed."));
}

#[test]
fn test_interactive_mode_remove_all() {
    let dir = tempdir().unwrap();
    let path1 = dir.path().join("bin1");
    let path2 = dir.path().join("bin2");
    let non_existent_path = dir.path().join("non_existent_bin");
    fs::create_dir(&path1).unwrap();
    fs::create_dir(&path2).unwrap();

    let path_delimiter = if cfg!(windows) { ";" } else { ":" };
    let original_path_str = format!(
        "{0}{1}{2}{1}{0}{1}{3}",
        path1.to_string_lossy(),
        path_delimiter,
        path2.to_string_lossy(),
        non_existent_path.to_string_lossy()
    );
    let expected_clean_path_str = format!(
        "{0}{1}{2}",
        path1.to_string_lossy(),
        path_delimiter,
        path2.to_string_lossy()
    );

    let mut cmd = Command::cargo_bin("path-purifier").unwrap();
    cmd.env("PATH", original_path_str.clone())
        .arg("--interactive")
        .write_stdin("n\nn\n") // Respond 'n' to both prompts (duplicate, non-existent)
        .assert()
        .success()
        .stdout(predicates::str::contains(format!("--- Original PATH ---\n{}", original_path_str)))
        .stdout(predicates::str::contains(format!("--- Proposed Clean PATH ---\n{}", expected_clean_path_str)))
        .stdout(predicates::str::contains(format!("--- Removed Entries ---\n- {}", path1.to_string_lossy())))
        .stdout(predicates::str::contains(format!("- {}", non_existent_path.to_string_lossy())));
}

#[test]
fn test_empty_path() {
    let mut cmd = Command::cargo_bin("path-purifier").unwrap();
    cmd.env("PATH", "")
        .arg("--dry-run")
        .assert()
        .success()
        .stdout(predicates::str::contains("--- Original PATH ---\n"))
        .stdout(predicates::str::contains("--- Proposed Clean PATH ---\n"))
        .stdout(predicates::str::contains("No entries removed."));
}

#[test]
fn test_path_with_only_non_existent() {
    let dir = tempdir().unwrap();
    let non_existent_path1 = dir.path().join("non_existent_bin1");
    let non_existent_path2 = dir.path().join("non_existent_bin2");

    let path_delimiter = if cfg!(windows) { ";" } else { ":" };
    let original_path_str = format!(
        "{0}{1}{2}",
        non_existent_path1.to_string_lossy(),
        path_delimiter,
        non_existent_path2.to_string_lossy()
    );
    let expected_clean_path_str = ""; // Empty path

    let mut cmd = Command::cargo_bin("path-purifier").unwrap();
    cmd.env("PATH", original_path_str.clone())
        .arg("--dry-run")
        .assert()
        .success()
        .stdout(predicates::str::contains(format!("--- Original PATH ---\n{}", original_path_str)))
        .stdout(predicates::str::contains("--- Proposed Clean PATH ---\n")) // Empty line
        .stdout(predicates::str::contains(format!("--- Removed Entries ---\n- {}", non_existent_path1.to_string_lossy())))
        .stdout(predicates::str::contains(format!("- {}", non_existent_path2.to_string_lossy())));
}
