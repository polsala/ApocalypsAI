#[cfg(test)]
mod integration {
    use assert_cmd::Command;
    use predicates::prelude::*;

    #[test]
    fn runs_without_args_and_shows_pretty_grid() {
        let mut cmd = Command::cargo_bin("ansi-color-palette").unwrap();
        cmd.assert()
            .success()
            .stdout(predicate::str::contains("0 ")).and(predicate::str::contains("255"));
    }

    #[test]
    fn json_flag_produces_valid_json_array() {
        let mut cmd = Command::cargo_bin("ansi-color-palette").unwrap();
        cmd.arg("--json");
        cmd.assert()
            .success()
            .stdout(predicate::function(|out: &str| {
                serde_json::from_str::<Vec<serde_json::Value>>(out).map(|v| v.len() == 256).unwrap_or(false)
            }));
    }
}

