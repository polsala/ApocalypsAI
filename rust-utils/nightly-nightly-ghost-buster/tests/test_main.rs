use std::process::Command;
use std::fs;
use std::path::Path;
use std::env;
use std::time::{SystemTime, UNIX_EPOCH};

fn run_binary(args: &[&str]) -> String {
    let output = Command::new(env!("CARGO_BIN_EXE_ghost-buster"))
        .args(args)
        .output()
        .expect("failed to execute process");
    String::from_utf8_lossy(&output.stdout).to_string()
}

fn create_temp_dir() -> std::path::PathBuf {
    let start = SystemTime::now();
    let since_the_epoch = start.duration_since(UNIX_EPOCH).expect("Time went backwards");
    let dir_name = format!("ghost_buster_test_{}", since_the_epoch.as_millis());
    let dir_path = env::temp_dir().join(dir_name);
    fs::create_dir_all(&dir_path).expect("Failed to create temp dir");
    dir_path
}

#[test]
fn test_no_ghosts() {
    let dir = create_temp_dir();
    let output = run_binary(&["--path", dir.to_str().unwrap()]);
    assert!(output.contains("No ghosts found."));
    fs::remove_dir_all(dir).unwrap();
}

#[test]
fn test_find_ghosts() {
    let dir = create_temp_dir();
    let ghost_path = dir.join(".secret");
    fs::write(&ghost_path, b"hidden").unwrap();
    let output = run_binary(&["--path", dir.to_str().unwrap()]);
    assert!(output.contains("👻 Found ghost:"));
    assert!(output.contains(".secret"));
    fs::remove_dir_all(dir).unwrap();
}

#[test]
fn test_delete_ghosts() {
    let dir = create_temp_dir();
    let ghost_path = dir.join(".temp");
    fs::write(&ghost_path, b"temp").unwrap();
    let output = run_binary(&["--path", dir.to_str().unwrap(), "--delete"]);
    assert!(output.contains("🗑️ Deleted ghost:"));
    assert!(!ghost_path.exists());
    fs::remove_dir_all(dir).unwrap();
}
