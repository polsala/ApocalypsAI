use std::process::Command;
use std::fs::{self, File};
use std::io::Write;

#[test]
fn cli_returns_optimal_selection() {
    // Mock input JSON (offline, deterministic)
    let input_json = r#"{
        "capacity": 8,
        "items": [
            {"name": "radio", "weight": 3, "value": 6},
            {"name": "map", "weight": 2, "value": 4},
            {"name": "knife", "weight": 1, "value": 2},
            {"name": "tent", "weight": 5, "value": 7}
        ]
    }"#;
    // Write to a temporary file
    let tmp_dir = tempfile::tempdir().expect("tempdir failed");
    let input_path = tmp_dir.path().join("input.json");
    let mut file = File::create(&input_path).expect("create file");
    file.write_all(input_json.as_bytes()).expect("write");

    // Execute the compiled binary (assumes cargo build has been run)
    let output = Command::new("./target/debug/scavenger_knapsack")
        .arg(&input_path)
        .output()
        .expect("failed to execute binary");
    assert!(output.status.success(), "binary exited with error");
    let stdout = String::from_utf8_lossy(&output.stdout);
    // Expected optimal set: radio + knife (weight 4, value 8) or map + tent (weight 7, value 11) – the latter is better.
    let expected = "[\"map\",\"tent\"]"; // order follows DP reconstruction (map then tent)
    assert_eq!(stdout.trim(), expected);
    // Clean up
    drop(tmp_dir);
}
