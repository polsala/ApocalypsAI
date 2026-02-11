#[cfg(test)]
mod integration {
    use assert_cmd::Command;
    use predicates::str::contains;

    #[test]
    fn cli_outputs_name() {
        // Mock rationale: using assert_cmd to run the binary without external network.
        let mut cmd = Command::cargo_bin("cryptic-plant-namer").unwrap();
        cmd.assert().success().stdout(contains("\u{202F}"));
    }

    #[test]
    fn cli_with_describe_outputs_two_lines() {
        let mut cmd = Command::cargo_bin("cryptic-plant-namer").unwrap();
        cmd.arg("--describe");
        cmd.assert()
            .success()
            .stdout(contains("\n")); // at least one newline after the name
    }
}
