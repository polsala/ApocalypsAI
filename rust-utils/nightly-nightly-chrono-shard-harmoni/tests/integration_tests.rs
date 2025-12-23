use assert_cmd::Command;
use predicates::prelude::*;
use std::fs;
use std::io::Write;

// Helper to create a temporary file with content
fn create_temp_file(name: &str, content: &str) -> std::path::PathBuf {
    let path = std::env::temp_dir().join(name);
    let mut file = fs::File::create(&path).unwrap();
    file.write_all(content.as_bytes()).unwrap();
    path
}

#[test]
fn test_no_anomalies() {
    // Mock rationale: Using temporary files to simulate file input without actual file system dependencies
    // or network calls. This ensures deterministic and offline testing.
    let content = "\
2023-01-01T10:00:00Z Event A\n
2023-01-01T10:00:10Z Event B\n
2023-01-01T10:00:20Z Event C\n
";
    let file = create_temp_file("test_no_anomalies.log", content);

    Command::cargo_bin("chrono-shard-harmonizer")
        .unwrap()
        .arg(file.to_str().unwrap())
        .assert()
        .success()
        .stdout(predicate::str::contains("Input lines processed: 3"))
        .stdout(predicate::str::contains("Valid data shards found: 3"))
        .stdout(predicate::str::contains("Original order: Perfectly aligned."))
        .stdout(predicate::str::contains("Echoes of Time: None detected."))
        .stdout(predicate::str::contains("Temporal Rifts: None detected."));

    fs::remove_file(file).unwrap();
}

#[test]
fn test_temporal_rift() {
    // Mock rationale: Using temporary files to simulate file input.
    let content = "\
2023-01-01T10:00:00Z Event A\n
2023-01-01T10:00:10Z Event B\n
2023-01-01T10:01:00Z Event C\n
2023-01-01T10:02:00Z Event D\n
"; // Gap between B and C is 50s. Gap between C and D is 60s. Default threshold is 60s.
    let file = create_temp_file("test_temporal_rift.log", content);

    Command::cargo_bin("chrono-shard-harmonizer")
        .unwrap()
        .arg(file.to_str().unwrap())
        .arg("-t")
        .arg("50") // Set threshold to 50s
        .assert()
        .success()
        .stdout(predicate::str::contains("Input lines processed: 4"))
        .stdout(predicate::str::contains("Valid data shards found: 4"))
        .stdout(predicate::str::contains("Original order: Perfectly aligned."))
        .stdout(predicate::str::contains("Echoes of Time: None detected."))
        .stdout(predicate::str::contains("Temporal Rifts (Gaps > 50s): 2"))
        .stdout(predicate::str::contains("Rift detected between 2023-01-01T10:00:10Z and 2023-01-01T10:01:00Z (Duration: 50s)"))
        .stdout(predicate::str::contains("Rift detected between 2023-01-01T10:01:00Z and 2023-01-01T10:02:00Z (Duration: 60s)"));

    fs::remove_file(file).unwrap();
}

#[test]
fn test_echoes_of_time() {
    // Mock rationale: Using temporary files to simulate file input.
    let content = "\
2023-01-01T10:00:00Z Event A\n
2023-01-01T10:00:10Z Event B\n
2023-01-01T10:00:10Z Event C (duplicate)\n
2023-01-01T10:00:20Z Event D\n
";
    let file = create_temp_file("test_echoes_of_time.log", content);

    Command::cargo_bin("chrono-shard-harmonizer")
        .unwrap()
        .arg(file.to_str().unwrap())
        .assert()
        .success()
        .stdout(predicate::str::contains("Input lines processed: 4"))
        .stdout(predicate::str::contains("Valid data shards found: 4"))
        .stdout(predicate::str::contains("Original order: Perfectly aligned."))
        .stdout(predicate::str::contains("Echoes of Time (Duplicate Timestamps): 1"))
        .stdout(predicate::str::contains("2023-01-01T10:00:10Z (2 occurrences)"))
        .stdout(predicate::str::contains("Temporal Rifts: None detected."));

    fs::remove_file(file).unwrap();
}

#[test]
fn test_out_of_order() {
    // Mock rationale: Using temporary files to simulate file input.
    let content = "\
2023-01-01T10:00:10Z Event B\n
2023-01-01T10:00:00Z Event A (out of order)\n
2023-01-01T10:00:20Z Event C\n
";
    let file = create_temp_file("test_out_of_order.log", content);

    Command::cargo_bin("chrono-shard-harmonizer")
        .unwrap()
        .arg(file.to_str().unwrap())
        .assert()
        .success()
        .stdout(predicate::str::contains("Input lines processed: 3"))
        .stdout(predicate::str::contains("Valid data shards found: 3"))
        .stdout(predicate::str::contains("Original order: Chronological Drift Detected (1 out-of-order instances)"))
        .stdout(predicate::str::contains("Echoes of Time: None detected."))
        .stdout(predicate::str::contains("Temporal Rifts: None detected."));

    fs::remove_file(file).unwrap();
}

#[test]
fn test_output_harmonized() {
    // Mock rationale: Using temporary files to simulate file input.
    let content = "\
2023-01-01T10:00:10Z Event B\n
2023-01-01T10:00:00Z Event A\n
2023-01-01T10:00:10Z Event C (duplicate)\n
2023-01-01T10:00:20Z Event D\n
";
    let file = create_temp_file("test_output_harmonized.log", content);

    Command::cargo_bin("chrono-shard-harmonizer")
        .unwrap()
        .arg(file.to_str().unwrap())
        .arg("-o")
        .assert()
        .success()
        .stdout(predicate::str::contains("--- Harmonized Data Shards ---"))
        .stdout(predicate::str::ends_with("\
2023-01-01T10:00:00Z Event A\n
2023-01-01T10:00:10Z Event B\n
2023-01-01T10:00:20Z Event D\n
")); // Note: Event C is de-duplicated
    
    fs::remove_file(file).unwrap();
}

#[test]
fn test_stdin_input() {
    // Mock rationale: Simulating stdin input by piping a string.
    let content = "\
2023-01-01T10:00:00Z First\n
22023-01-01T10:00:05Z Second\n
"; // Intentionally malformed timestamp for second line
    
    Command::cargo_bin("chrono-shard-harmonizer")
        .unwrap()
        .write_stdin(content)
        .assert()
        .success()
        .stderr(predicate::str::contains("Warning: Could not parse timestamp from line: \"22023-01-01T10:00:05Z Second\"
"))
        .stdout(predicate::str::contains("Input lines processed: 2"))
        .stdout(predicate::str::contains("Valid data shards found: 1"))
        .stdout(predicate::str::contains("Echoes of Time: None detected."))
        .stdout(predicate::str::contains("Temporal Rifts: None detected.")); // Only one valid shard, so no rifts/echoes
}

#[test]
fn test_empty_input() {
    // Mock rationale: Using a temporary empty file.
    let file = create_temp_file("test_empty_input.log", "");

    Command::cargo_bin("chrono-shard-harmonizer")
        .unwrap()
        .arg(file.to_str().unwrap())
        .assert()
        .success()
        .stdout(predicate::str::contains("No valid timestamped data shards found to harmonize."));

    fs::remove_file(file).unwrap();
}
