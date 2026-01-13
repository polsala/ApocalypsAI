use std::fs::File;
use std::io::Write;
use std::path::PathBuf;
use nightly_uptime_emoji::{read_uptime, format_uptime};

#[test]
fn test_format_uptime() {
    let seconds = 123456.78;
    let formatted = format_uptime(seconds);
    assert_eq!(formatted, "ð 1 days, 10 hours, 17 minutes");
}

#[test]
fn test_read_uptime_file() {
    let dir = std::env::temp_dir();
    let file_path = dir.join("uptime_test.txt");
    let mut file = File::create(&file_path).unwrap();
    writeln!(file, "123456.78 0.00").unwrap();
    let seconds = read_uptime(&file_path).unwrap();
    assert!((seconds - 123456.78).abs() < 0.01);
    std::fs::remove_file(&file_path).unwrap();
}

#[test]
fn test_main_output() {
    let dir = std::env::temp_dir();
    let file_path = dir.join("uptime_test.txt");
    let mut file = File::create(&file_path).unwrap();
    writeln!(file, "123456.78 0.00").unwrap();
    let output = std::process::Command::new("cargo")
        .args(&["run", "--quiet", "--", "--uptime-file", file_path.to_str().unwrap()])
        .output()
        .expect("failed to run");
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("ð 1 days, 10 hours, 17 minutes"));
    std::fs::remove_file(&file_path).unwrap();
}
