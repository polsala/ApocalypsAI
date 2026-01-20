#[cfg(test)]
mod tests {
    use assert_cmd::Command;
    use predicates::prelude::*;

    #[test]
    fn test_silent_failure_detected() {
        let mut cmd = Command::cargo_bin("void-whistle").unwrap();
        cmd.write_stdin("INFO start\nINFO end\n")
            .arg("--pattern")
            .arg("ERROR")
            .arg("--invert");
        cmd.assert()
            .success()
            .stdout(predicate::str::contains("Inverted check passed"));
    }

    #[test]
    fn test_no_failure_when_present() {
        let mut cmd = Command::cargo_bin("void-whistle").unwrap();
        cmd.write_stdin("INFO start\nERROR crash\nINFO end\n")
            .arg("--pattern")
            .arg("ERROR");
        cmd.assert()
            .success()
            .stdout(predicate::str::is_empty().not());
    }

    #[test]
    fn test_failure_when_missing() {
        let mut cmd = Command::cargo_bin("void-whistle").unwrap();
        cmd.write_stdin("INFO start\nINFO end\n")
            .arg("--pattern")
            .arg("ERROR");
        cmd.assert()
            .success()
            .stdout(predicate::str::contains("Silent failure detected"));
    }
}
