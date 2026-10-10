use assert_cmd::Command;
use predicates::prelude::*;
use std::fs;
use std::time::{Duration, SystemTime};
use tempfile::tempdir;

// Mock rationale: The `tempfile` crate is used to create isolated, temporary file system environments for tests.
// This ensures tests are deterministic and do not interfere with the actual file system or other tests.
// File modification times are explicitly set for test files to simulate various drift scenarios,
// making the tests independent of the system's current time for the *creation* of the drift.
// The drift threshold is chosen to be large enough to account for minor execution time variations
// while still being able to detect the deliberately introduced drifts.

// Helper function from main.rs, re-exported for tests
#[path = "../src/main.rs"]
mod main_app;

fn set_mtime_for_test(path: &std::path::Path, duration_from_now: Duration, is_future: bool) -> Result<(), Box<dyn std::error::Error>> {
    main_app::set_mtime(path, duration_from_now, is_future)
}

#[test]
fn test_no_drift_detected() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let file_path = dir.path().join("aligned.txt");
    fs::write(&file_path, "content")?;

    // Set mtime to be very close to now (within default 60s threshold)
    set_mtime_for_test(&file_path, Duration::from_secs(10), false)?;

    Command::cargo_bin("tdc")?
        .arg(dir.path())
        .assert()
        .success()
        .stdout(predicate::str::contains("No significant temporal drift detected"));

    Ok(())
}

#[test]
fn test_drift_detected_past() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let file_path = dir.path().join("past_drift.txt");
    fs::write(&file_path, "content")?;

    // Set mtime 100 seconds in the past, exceeding default 60s threshold
    set_mtime_for_test(&file_path, Duration::from_secs(100), false)?;

    Command::cargo_bin("tdc")?
        .arg(dir.path())
        .assert()
        .success()
        .stdout(predicate::str::contains("DRIFT DETECTED").and(predicate::str::contains("(past)")));

    Ok(())
}

#[test]
fn test_drift_detected_future() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let file_path = dir.path().join("future_drift.txt");
    fs::write(&file_path, "content")?;

    // Set mtime 100 seconds in the future, exceeding default 60s threshold
    set_mtime_for_test(&file_path, Duration::from_secs(100), true)?;

    Command::cargo_bin("tdc")?
        .arg(dir.path())
        .assert()
        .success()
        .stdout(predicate::str::contains("DRIFT DETECTED").and(predicate::str::contains("(future)")));

    Ok(())
}

#[test]
fn test_drift_with_custom_threshold() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let file_path = dir.path().join("custom_threshold_drift.txt");
    fs::write(&file_path, "content")?;

    // Set mtime 40 seconds in the past
    set_mtime_for_test(&file_path, Duration::from_secs(40), false)?;

    // Should not detect drift with default 60s threshold
    Command::cargo_bin("tdc")?
        .arg(dir.path())
        .assert()
        .success()
        .stdout(predicate::str::contains("No significant temporal drift detected"));

    // Should detect drift with 30s threshold
    Command::cargo_bin("tdc")?
        .arg(dir.path())
        .arg("--threshold")
        .arg("30")
        .assert()
        .success()
        .stdout(predicate::str::contains("DRIFT DETECTED"));

    Ok(())
}

#[test]
fn test_fix_drift() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let file_path = dir.path().join("fix_me.txt");
    fs::write(&file_path, "content")?;

    // Set mtime 100 seconds in the past
    set_mtime_for_test(&file_path, Duration::from_secs(100), false)?;

    let initial_mtime = fs::metadata(&file_path)?.modified()?;

    Command::cargo_bin("tdc")?
        .arg(dir.path())
        .arg("--fix")
        .assert()
        .success()
        .stdout(predicate::str::contains("Recalibrated"));

    let fixed_mtime = fs::metadata(&file_path)?.modified()?;

    // The fixed mtime should be different from the initial mtime
    assert_ne!(initial_mtime, fixed_mtime);

    // The fixed mtime should be very close to SystemTime::now() (within a small margin)
    let now = SystemTime::now();
    let diff = if fixed_mtime > now {
        fixed_mtime.duration_since(now)?
    } else {
        now.duration_since(fixed_mtime)?
    };
    assert!(diff < Duration::from_secs(5), "Fixed mtime is not close enough to now: {:?}", diff);

    Ok(())
}

#[test]
fn test_fix_drift_multiple_files() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let file1_path = dir.path().join("file1.txt");
    let file2_path = dir.path().join("file2.txt");
    let file3_path = dir.path().join("file3.txt");

    fs::write(&file1_path, "content1")?;
    fs::write(&file2_path, "content2")?;
    fs::write(&file3_path, "content3")?;

    // File 1: Drifted past
    set_mtime_for_test(&file1_path, Duration::from_secs(150), false)?;
    // File 2: Drifted future
    set_mtime_for_test(&file2_path, Duration::from_secs(150), true)?;
    // File 3: Aligned (within threshold)
    set_mtime_for_test(&file3_path, Duration::from_secs(10), false)?;

    let initial_mtime1 = fs::metadata(&file1_path)?.modified()?;
    let initial_mtime2 = fs::metadata(&file2_path)?.modified()?;
    let initial_mtime3 = fs::metadata(&file3_path)?.modified()?;

    Command::cargo_bin("tdc")?
        .arg(dir.path())
        .arg("--fix")
        .arg("--threshold")
        .arg("60")
        .assert()
        .success()
        .stdout(predicate::str::contains("Recalibrated '" + &file1_path.file_name().unwrap().to_string_lossy() + "'"))
        .stdout(predicate::str::contains("Recalibrated '" + &file2_path.file_name().unwrap().to_string_lossy() + "'"))
        .stdout(predicate::str::contains("Successfully recalibrated 2 drifted files."));

    let fixed_mtime1 = fs::metadata(&file1_path)?.modified()?;
    let fixed_mtime2 = fs::metadata(&file2_path)?.modified()?;
    let fixed_mtime3 = fs::metadata(&file3_path)?.modified()?;

    assert_ne!(initial_mtime1, fixed_mtime1);
    assert_ne!(initial_mtime2, fixed_mtime2);
    assert_eq!(initial_mtime3, fixed_mtime3); // This one should not have been fixed

    let now = SystemTime::now();
    let diff1 = if fixed_mtime1 > now { fixed_mtime1.duration_since(now)? } else { now.duration_since(fixed_mtime1)? };
    let diff2 = if fixed_mtime2 > now { fixed_mtime2.duration_since(now)? } else { now.duration_since(fixed_mtime2)? };

    assert!(diff1 < Duration::from_secs(5));
    assert!(diff2 < Duration::from_secs(5));

    Ok(())
}
