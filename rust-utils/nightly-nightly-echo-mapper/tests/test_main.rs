use std::process::Command;
use std::fs::{self, File};
use std::io::Write;
use std::path::Path;
use tempfile::tempdir;
use filetime::{set_file_mtime, FileTime};
use std::time::{SystemTime, Duration};

// Mock rationale: We need to create files with specific modification times
// to test the filtering logic deterministically. `tempdir` provides an isolated
// environment, and `filetime` allows precise control over timestamps,
// which are external system properties. Running the compiled binary ensures
// the full CLI logic is tested, not just internal functions.

#[test]
fn test_fresh_files() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    // File modified 30 minutes ago (fresh)
    let fresh_file = path.join("fresh_file.txt");
    File::create(&fresh_file)?.write_all(b"content")?;
    let thirty_mins_ago = SystemTime::now() - Duration::from_secs(30 * 60);
    set_file_mtime(&fresh_file, FileTime::from_system_time(thirty_mins_ago))?;

    // File modified 2 hours ago (stale for 1h, fresh for 3h)
    let slightly_stale_file = path.join("slightly_stale_file.txt");
    File::create(&slightly_stale_file)?.write_all(b"content")?;
    let two_hours_ago = SystemTime::now() - Duration::from_secs(2 * 60 * 60);
    set_file_mtime(&slightly_stale_file, FileTime::from_system_time(two_hours_ago))?;

    // File modified 2 days ago (very stale)
    let stale_file = path.join("stale_file.txt");
    File::create(&stale_file)?.write_all(b"content")?;
    let two_days_ago = SystemTime::now() - Duration::from_secs(2 * 24 * 60 * 60);
    set_file_mtime(&stale_file, FileTime::from_system_time(two_days_ago))?;

    // Test --fresh 1h
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-echo-mapper"))
        .arg("--path")
        .arg(path)
        .arg("--fresh")
        .arg("1h")
        .output()?;

    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    println!("Fresh 1h output:\n{}", stdout);
    assert!(stdout.contains(&fresh_file.display().to_string()));
    assert!(!stdout.contains(&slightly_stale_file.display().to_string()));
    assert!(!stdout.contains(&stale_file.display().to_string()));

    // Test --fresh 3h
    let output_3h = Command::new(env!("CARGO_BIN_EXE_nightly-echo-mapper"))
        .arg("--path")
        .arg(path)
        .arg("--fresh")
        .arg("3h")
        .output()?;

    assert!(output_3h.status.success());
    let stdout_3h = String::from_utf8_lossy(&output_3h.stdout);
    println!("Fresh 3h output:\n{}", stdout_3h);
    assert!(stdout_3h.contains(&fresh_file.display().to_string()));
    assert!(stdout_3h.contains(&slightly_stale_file.display().to_string()));
    assert!(!stdout_3h.contains(&stale_file.display().to_string()));


    dir.close()?;
    Ok(())
}

#[test]
fn test_stale_files() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    // File modified 3 hours ago (stale for 1h, not stale for 1d)
    let slightly_stale_file = path.join("slightly_stale_file.txt");
    File::create(&slightly_stale_file)?.write_all(b"content")?;
    let three_hours_ago = SystemTime::now() - Duration::from_secs(3 * 60 * 60);
    set_file_mtime(&slightly_stale_file, FileTime::from_system_time(three_hours_ago))?;

    // File modified 2 days ago (stale for 1d)
    let very_stale_file = path.join("very_stale_file.txt");
    File::create(&very_stale_file)?.write_all(b"content")?;
    let two_days_ago = SystemTime::now() - Duration::from_secs(2 * 24 * 60 * 60);
    set_file_mtime(&very_stale_file, FileTime::from_system_time(two_days_ago))?;

    // File modified 30 minutes ago (not stale)
    let fresh_file = path.join("fresh_file.txt");
    File::create(&fresh_file)?.write_all(b"content")?;
    let thirty_mins_ago = SystemTime::now() - Duration::from_secs(30 * 60);
    set_file_mtime(&fresh_file, FileTime::from_system_time(thirty_mins_ago))?;

    // Test --stale 1h
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-echo-mapper"))
        .arg("--path")
        .arg(path)
        .arg("--stale")
        .arg("1h")
        .output()?;

    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    println!("Stale 1h output:\n{}", stdout);
    assert!(stdout.contains(&slightly_stale_file.display().to_string()));
    assert!(stdout.contains(&very_stale_file.display().to_string()));
    assert!(!stdout.contains(&fresh_file.display().to_string()));

    // Test --stale 1d
    let output_1d = Command::new(env!("CARGO_BIN_EXE_nightly-echo-mapper"))
        .arg("--path")
        .arg(path)
        .arg("--stale")
        .arg("1d")
        .output()?;

    assert!(output_1d.status.success());
    let stdout_1d = String::from_utf8_lossy(&output_1d.stdout);
    println!("Stale 1d output:\n{}", stdout_1d);
    assert!(!stdout_1d.contains(&slightly_stale_file.display().to_string()));
    assert!(stdout_1d.contains(&very_stale_file.display().to_string()));
    assert!(!stdout_1d.contains(&fresh_file.display().to_string()));

    dir.close()?;
    Ok(())
}

#[test]
fn test_max_depth() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    // Create files at different depths
    let file_depth_0 = path.join("file0.txt");
    File::create(&file_depth_0)?.write_all(b"content")?;
    set_file_mtime(&file_depth_0, FileTime::from_system_time(SystemTime::now() - Duration::from_secs(10)))?;

    let sub_dir = path.join("sub");
    fs::create_dir(&sub_dir)?;
    let file_depth_1 = sub_dir.join("file1.txt");
    File::create(&file_depth_1)?.write_all(b"content")?;
    set_file_mtime(&file_depth_1, FileTime::from_system_time(SystemTime::now() - Duration::from_secs(10)))?;

    let sub_sub_dir = sub_dir.join("sub_sub");
    fs::create_dir(&sub_sub_dir)?;
    let file_depth_2 = sub_sub_dir.join("file2.txt");
    File::create(&file_depth_2)?.write_all(b"content")?;
    set_file_mtime(&file_depth_2, FileTime::from_system_time(SystemTime::now() - Duration::from_secs(10)))?;

    // Test max-depth 0
    let output_d0 = Command::new(env!("CARGO_BIN_EXE_nightly-echo-mapper"))
        .arg("--path")
        .arg(path)
        .arg("--fresh")
        .arg("1h")
        .arg("--max-depth")
        .arg("0")
        .output()?;

    assert!(output_d0.status.success());
    let stdout_d0 = String::from_utf8_lossy(&output_d0.stdout);
    println!("Max depth 0 output:\n{}", stdout_d0);
    assert!(stdout_d0.contains(&file_depth_0.display().to_string()));
    assert!(!stdout_d0.contains(&file_depth_1.display().to_string()));
    assert!(!stdout_d0.contains(&file_depth_2.display().to_string()));

    // Test max-depth 1
    let output_d1 = Command::new(env!("CARGO_BIN_EXE_nightly-echo-mapper"))
        .arg("--path")
        .arg(path)
        .arg("--fresh")
        .arg("1h")
        .arg("--max-depth")
        .arg("1")
        .output()?;

    assert!(output_d1.status.success());
    let stdout_d1 = String::from_utf8_lossy(&output_d1.stdout);
    println!("Max depth 1 output:\n{}", stdout_d1);
    assert!(stdout_d1.contains(&file_depth_0.display().to_string()));
    assert!(stdout_d1.contains(&file_depth_1.display().to_string()));
    assert!(!stdout_d1.contains(&file_depth_2.display().to_string()));

    dir.close()?;
    Ok(())
}

#[test]
fn test_error_handling() -> Result<(), Box<dyn std::error::Error>> {
    let output_no_args = Command::new(env!("CARGO_BIN_EXE_nightly-echo-mapper"))
        .output()?;
    assert!(!output_no_args.status.success());
    let stderr_no_args = String::from_utf8_lossy(&output_no_args.stderr);
    assert!(stderr_no_args.contains("Error: Either --fresh or --stale duration must be specified."));

    let output_both_args = Command::new(env!("CARGO_BIN_EXE_nightly-echo-mapper"))
        .arg("--fresh").arg("1h")
        .arg("--stale").arg("1d")
        .output()?;
    assert!(!output_both_args.status.success());
    let stderr_both_args = String::from_utf8_lossy(&output_both_args.stderr);
    assert!(stderr_both_args.contains("Error: Cannot specify both --fresh and --stale."));

    Ok(())
}
