use assert_cmd::Command;
use predicates::prelude::*;
use tempfile::NamedTempFile;
use std::io::Write;

// Mock rationale: Using tempfile to simulate file input for CLI tests
// ensures tests are deterministic and offline, as no actual filesystem
// interaction outside of a controlled temporary environment is needed.

#[test]
fn test_calculate_cosmic_score_determinism() {
    let task1 = "Scavenge for rations";
    let task2 = "Repair the water purifier";
    let seed1 = 123;
    let seed2 = 456;

    // Same task, same seed should yield same score
    assert_eq!(
        super::calculate_cosmic_score(task1, seed1),
        super::calculate_cosmic_score(task1, seed1)
    );

    // Different task, same seed should yield different score (highly probable)
    assert_ne!(
        super::calculate_cosmic_score(task1, seed1),
        super::calculate_cosmic_score(task2, seed1)
    );

    // Same task, different seed should yield different score (highly probable)
    assert_ne!(
        super::calculate_cosmic_score(task1, seed1),
        super::calculate_cosmic_score(task1, seed2)
    );
}

#[test]
fn test_process_tasks_ordering() {
    let tasks_content = "Task C\nTask A\nTask B";
    let seed = 100; // Fixed seed for determinism

    let cursor = std::io::Cursor::new(tasks_content);
    let processed = super::process_tasks(cursor, seed);

    // The exact scores will vary based on DefaultHasher implementation,
    // but the relative order should be consistent for a given seed.
    // We'll check if they are sorted by score.
    let mut prev_score = 0;
    for (score, _task) in &processed {
        assert!(*score >= prev_score);
        prev_score = *score;
    }

    // Check if all original tasks are present
    let original_tasks: Vec<&str> = tasks_content.lines().filter(|l| !l.is_empty()).collect();
    let processed_tasks: Vec<&str> = processed.iter().map(|(_, t)| t.as_str()).collect();
    assert_eq!(processed_tasks.len(), original_tasks.len());
    assert!(original_tasks.iter().all(|ot| processed_tasks.contains(ot)));
}

#[test]
fn test_cli_with_file_input() -> Result<(), Box<dyn std::error::Error>> {
    // Mock rationale: Using tempfile to simulate file input for CLI tests
    // ensures tests are deterministic and offline.
    let mut file = NamedTempFile::new()?;
    writeln!(file, "Gather cosmic dust")?;
    writeln!(file, "Decipher ancient star charts")?;
    writeln!(file, "Polish the temporal displacement unit")?;
    let file_path = file.path().to_str().unwrap();

    let mut cmd = Command::cargo_bin("nightly-cosmic-choreographer")?;
    cmd.arg("-f").arg(file_path).arg("-s").arg("42");

    cmd.assert()
        .success()
        .stdout(predicate::str::contains("--- Cosmic Choreographer's Nudge (Seed: 42) ---"))
        .stdout(predicate::str::contains("Gather cosmic dust"))
        .stdout(predicate::str::contains("Decipher ancient star charts"))
        .stdout(predicate::str::contains("Polish the temporal displacement unit"))
        .stdout(predicate::str::contains("The cosmos whispers: This is your destiny!")); // Check for the top nudge

    Ok(())
}

#[test]
fn test_cli_with_stdin_input() -> Result<(), Box<dyn std::error::Error>> {
    let mut cmd = Command::cargo_bin("nightly-cosmic-choreographer")?;
    cmd.arg("-s").arg("101");

    // Mock rationale: Providing stdin directly to the command simulates user input
    // without requiring actual interactive console input, making the test deterministic.
    cmd.write_stdin("Calibrate the Chronometer\nRe-align the Quantum Flux Capacitor\n")
        .assert()
        .success()
        .stdout(predicate::str::contains("--- Cosmic Choreographer's Nudge (Seed: 101) ---"))
        .stdout(predicate::str::contains("Calibrate the Chronometer"))
        .stdout(predicate::str::contains("Re-align the Quantum Flux Capacitor"))
        .stdout(predicate::str::contains("The cosmos whispers: This is your destiny!"));

    Ok(())
}

#[test]
fn test_cli_empty_input() -> Result<(), Box<dyn std::error::Error>> {
    // Mock rationale: Using tempfile to simulate an empty file input for CLI tests
    // ensures tests are deterministic and offline.
    let file = NamedTempFile::new()?;
    let file_path = file.path().to_str().unwrap();

    let mut cmd = Command::cargo_bin("nightly-cosmic-choreographer")?;
    cmd.arg("-f").arg(file_path).arg("-s").arg("500");

    cmd.assert()
        .success()
        .stdout(predicate::str::contains("--- Cosmic Choreographer's Nudge (Seed: 500) ---"))
        .stdout(predicate::str::contains("The cosmos is silent. Perhaps there are no tasks to align today?"))
        .stdout(predicate::str::not(predicate::str::contains("The cosmos whispers"))); // No tasks, no specific nudge

    Ok(())
}

#[test]
fn test_cli_invalid_file() -> Result<(), Box<dyn std::error::Error>> {
    let mut cmd = Command::cargo_bin("nightly-cosmic-choreographer")?;
    cmd.arg("-f").arg("non_existent_file.txt").arg("-s").arg("1");

    cmd.assert()
        .failure()
        .stderr(predicate::str::contains("Failed to open tasks file 'non_existent_file.txt'"));

    Ok(())
}

#[test]
fn test_cli_invalid_seed_clap_error() -> Result<(), Box<dyn std::error::Error>> {
    // Mock rationale: Using tempfile to simulate file input for CLI tests
    // ensures tests are deterministic and offline.
    let mut file = NamedTempFile::new()?;
    writeln!(file, "Task 1")?;
    let file_path = file.path().to_str().unwrap();

    let mut cmd = Command::cargo_bin("nightly-cosmic-choreographer")?;
    cmd.arg("-f").arg(file_path).arg("-s").arg("not_a_number");

    // Clap handles invalid arguments, so it should show help and exit with error.
    cmd.assert()
        .failure()
        .stderr(predicate::str::contains("error: invalid digit found in string"));

    Ok(())
}
