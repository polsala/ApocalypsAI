use assert_cmd::Command;
use predicates::prelude::*;

// Mock rationale: The utility uses `chrono::Utc::now().timestamp()` for its default seed,
// which is non-deterministic. For tests, we provide a fixed seed via the `--seed` argument
// to ensure deterministic output. This allows us to test the core logic and output format
// without relying on the current time. The frequency value is whimsical and derived from a hash,
// so we test its format rather than an exact value, while the suggestion is deterministically
// picked from a list based on the hash, allowing for exact string matching.

#[test]
fn test_no_args_output_format() {
    let mut cmd = Command::cargo_bin("nightly-temporal-echo-tuner").unwrap();
    cmd.assert()
        .success()
        .stdout(predicate::str::contains("Temporal Echo Detected!"))
        .stdout(predicate::str::contains("Resonance Frequency:").and(predicate::str::regex(r"\d+\.\d{2} Hz")))
        .stdout(predicate::str::contains("Harmonizing Suggestion:"))
        .stdout(predicate::str::contains("Stay vigilant, fellow temporal traveler!"));
}

#[test]
fn test_with_seed_deterministic_output() {
    let mut cmd = Command::cargo_bin("nightly-temporal-echo-tuner").unwrap();
    cmd.arg("--seed").arg("test_seed_123");
    cmd.assert()
        .success()
        .stdout(predicate::str::contains("Temporal Echo Detected!"))
        .stdout(predicate::str::contains("Resonance Frequency: 46.20 Hz"))
        .stdout(predicate::str::contains("Harmonizing Suggestion: Perform a small, unexpected act of kindness for a stranger."))
        .stdout(predicate::str::contains("Stay vigilant, fellow temporal traveler!"));
}

#[test]
fn test_frequency_only_output() {
    let mut cmd = Command::cargo_bin("nightly-temporal-echo-tuner").unwrap();
    cmd.arg("--seed").arg("test_seed_123").arg("--frequency-only");
    cmd.assert()
        .success()
        .stdout(predicate::str::contains("46.20 Hz\n"))
        .stdout(predicate::str::not(predicate::str::contains("Temporal Echo Detected!")))
        .stdout(predicate::str::not(predicate::str::contains("Harmonizing Suggestion:")));
}

#[test]
fn test_another_seed_deterministic_output() {
    let mut cmd = Command::cargo_bin("nightly-temporal-echo-tuner").unwrap();
    cmd.arg("--seed").arg("another_temporal_flux");
    cmd.assert()
        .success()
        .stdout(predicate::str::contains("Resonance Frequency: 60.64 Hz"))
        .stdout(predicate::str::contains("Harmonizing Suggestion: Gently pat a nearby wall and whisper 'It's okay, you're doing great.'"));
}

#[test]
fn test_empty_seed_string() {
    let mut cmd = Command::cargo_bin("nightly-temporal-echo-tuner").unwrap();
    cmd.arg("--seed").arg("");
    cmd.assert()
        .success()
        .stdout(predicate::str::contains("Resonance Frequency: 104.28 Hz"))
        .stdout(predicate::str::contains("Harmonizing Suggestion: Check if your reflection is truly yours, or just a very good mimic."));
}
