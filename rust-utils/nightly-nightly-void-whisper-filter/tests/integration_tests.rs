use assert_cmd::Command;
use predicates::prelude::*;
use std::io::Write;
use tempfile::NamedTempFile;

// Mock rationale: These tests use `assert_cmd` to run the actual compiled binary.
// File I/O is handled by creating temporary files via `tempfile::NamedTempFile`,
// ensuring tests are deterministic and do not rely on external system state or network.

#[test]
fn finds_simple_pattern_in_stdin() {
    let mut cmd = Command::cargo_bin("void-whisper-filter").unwrap();
    cmd.arg("-p").arg("error");
    cmd.write_stdin("info line 1\nerror line 2\nwarning line 3\nerror line 4\n")
        .unwrap();

    cmd.assert()
        .success()
        .stderr(predicate::str::contains("Found 2 void whispers."))
        .stdout(predicate::str::contains("2: \x1b[33merror line 2\x1b[0m\n---\n4: \x1b[33merror line 4\x1b[0m"));
}

#[test]
fn finds_regex_pattern_in_file() {
    let mut file = NamedTempFile::new().unwrap();
    writeln!(file, "log: user logged in").unwrap();
    writeln!(file, "log: failed attempt from 192.168.1.1").unwrap();
    writeln!(file, "log: another user logged out").unwrap();
    writeln!(file, "log: failed attempt from 10.0.0.5").unwrap();
    let file_path = file.path().to_owned();

    let mut cmd = Command::cargo_bin("void-whisper-filter").unwrap();
    cmd.arg("-p").arg(r"failed attempt from \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
        .arg("-f").arg(&file_path);

    cmd.assert()
        .success()
        .stderr(predicate::str::contains("Found 2 void whispers."))
        .stdout(predicate::str::contains("2: \x1b[33mlog: failed attempt from 192.168.1.1\x1b[0m\n---\n4: \x1b[33mlog: failed attempt from 10.0.0.5\x1b[0m"));
}

#[test]
fn no_matches_found() {
    let mut cmd = Command::cargo_bin("void-whisper-filter").unwrap();
    cmd.arg("-p").arg("nonexistent");
    cmd.write_stdin("line 1\nline 2\n").unwrap();

    cmd.assert()
        .success()
        .stderr(predicate::str::contains("Found 0 void whispers."))
        .stdout(predicate::str::is_empty());
}

#[test]
fn handles_empty_input() {
    let mut cmd = Command::cargo_bin("void-whisper-filter").unwrap();
    cmd.arg("-p").arg("pattern");
    cmd.write_stdin("").unwrap();

    cmd.assert()
        .success()
        .stderr(predicate::str::contains("Found 0 void whispers."))
        .stdout(predicate::str::is_empty());
}

#[test]
fn shows_context_lines_before_match() {
    let mut cmd = Command::cargo_bin("void-whisper-filter").unwrap();
    cmd.arg("-p").arg("target").arg("-c").arg("1");
    cmd.write_stdin("line A\nline B\nline C target\nline D\nline E target\n").unwrap();

    cmd.assert()
        .success()
        .stderr(predicate::str::contains("Found 2 void whispers."))
        .stdout(predicate::str::contains("2: line B\n3: \x1b[33mline C target\x1b[0m\n---\n5: \x1b[33mline E target\x1b[0m"));
}

#[test]
fn shows_multiple_context_lines_before_match() {
    let mut cmd = Command::cargo_bin("void-whisper-filter").unwrap();
    cmd.arg("-p").arg("match").arg("-c").arg("2");
    cmd.write_stdin("1\n2\n3\n4 match\n5\n6\n7 match\n").unwrap();

    cmd.assert()
        .success()
        .stderr(predicate::str::contains("Found 2 void whispers."))
        .stdout(predicate::str::contains("2: 2\n3: 3\n4: \x1b[33m4 match\x1b[0m\n---\n6: 6\n7: \x1b[33m7 match\x1b[0m"));
}

#[test]
fn context_at_start_of_file() {
    let mut cmd = Command::cargo_bin("void-whisper-filter").unwrap();
    cmd.arg("-p").arg("start").arg("-c").arg("2");
    cmd.write_stdin("line 1 start\nline 2\nline 3\n").unwrap();

    cmd.assert()
        .success()
        .stderr(predicate::str::contains("Found 1 void whispers."))
        .stdout(predicate::str::contains("1: \x1b[33mline 1 start\x1b[0m")); // No context before line 1
}

#[test]
fn invalid_regex_pattern() {
    let mut cmd = Command::cargo_bin("void-whisper-filter").unwrap();
    cmd.arg("-p").arg("[invalid regex");
    cmd.write_stdin("some text").unwrap();

    cmd.assert()
        .failure()
        .stderr(predicate::str::contains("Invalid regex pattern:"));
}

#[test]
fn context_with_multiple_matches_close_together() {
    let mut cmd = Command::cargo_bin("void-whisper-filter").unwrap();
    cmd.arg("-p").arg("error").arg("-c").arg("1");
    cmd.write_stdin("line 1\nline 2 error\nline 3 error\nline 4\n").unwrap();

    cmd.assert()
        .success()
        .stderr(predicate::str::contains("Found 2 void whispers."))
        .stdout(predicate::str::contains("1: line 1\n2: \x1b[33mline 2 error\x1b[0m\n---\n3: \x1b[33mline 3 error\x1b[0m"));
    // Note: line 2 error is not context for line 3 error because buffer is cleared after first match.
    // This is the intended behavior for this simplified 'before' context.
}
