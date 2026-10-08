#[cfg(test)]
mod integration {
    use assert_cmd::Command;
    use predicates::str::contains;

    // Mock rationale: The `assert_cmd` crate provides a convenient way to run the compiled binary
    // and assert on its stdout/stderr without needing external resources.
    // Since the test environment is offline, we rely only on the binary itself.

    #[test]
    fn cli_encodes_argument() {
        let mut cmd = Command::cargo_bin("nightly-rot13-cli").unwrap();
        cmd.arg("Hello, Survivor!");
        cmd.assert()
            .success()
            .stdout(contains("Uryyb, Fhesvire!"));
    }

    #[test]
    fn cli_reads_from_stdin() {
        let mut cmd = Command::cargo_bin("nightly-rot13-cli").unwrap();
        cmd.write_stdin("SecretMessage")
            .assert()
            .success()
            .stdout(contains("FrpergZrffntr"));
    }
}
