#[cfg(test)]
mod integration {
    use assert_cmd::Command;
    use std::fs;
    use std::io::Write;
    use tempfile::NamedTempFile;

    // Mock rationale: we create a temporary JSON file with known items,
    // invoke the compiled binary with a capacity, and assert the output contains
    // the expected selected items.
    #[test]
    fn test_cli_output() {
        // Prepare mock input JSON
        let json = r#"[
            {"name": "canned beans", "weight": 2, "value": 5},
            {"name": "water bottle", "weight": 3, "value": 4},
            {"name": "first‑aid kit", "weight": 5, "value": 10},
            {"name": "flashlight", "weight": 1, "value": 2}
        ]"#;
        let mut tmp = NamedTempFile::new().expect("temp file");
        write!(tmp, "{}", json).expect("write json");
        let path = tmp.path().to_str().unwrap();

        // Run the binary with capacity 5
        let mut cmd = Command::cargo_bin("nightly_scavenger_knapsack").expect("binary");
        cmd.arg(path).arg("5");
        cmd.assert()
            .success()
            .stdout(predicates::str::contains("canned beans"))
            .stdout(predicates::str::contains("flashlight"))
            .stdout(predicates::str::contains("Total weight: 3"))
            .stdout(predicates::str::contains("Total value: 7"));
    }
}
