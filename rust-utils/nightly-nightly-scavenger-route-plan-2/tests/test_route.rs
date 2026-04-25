#[cfg(test)]
mod integration {
    use std::process::Command;
    use std::io::Write;
    use std::fs::File;
    use std::env;

    #[test]
    fn test_cli_output() {
        // Mock JSON data (no external files needed)
        let json = r#"[
            {"name": "Base", "x": 0.0, "y": 0.0},
            {"name": "Outpost", "x": 3.0, "y": 4.0},
            {"name": "Cache", "x": 1.0, "y": 1.0}
        ]"#;

        // Write to a temporary file
        let mut tmp = tempfile::NamedTempFile::new().expect("temp file");
        write!(tmp, "{}", json).expect("write temp");
        let tmp_path = tmp.path().to_str().unwrap();

        // Build the binary first (cargo test builds it already)
        let output = Command::new(env::current_dir().unwrap().join("target/debug/scavenger-route-planner"))
            .arg(tmp_path)
            .output()
            .expect("failed to execute binary");

        assert!(output.status.success(), "process exited with error");
        let stdout = String::from_utf8_lossy(&output.stdout);
        // Expected order: Base (start), Cache (closest), Outpost
        assert_eq!(stdout.trim(), "Base, Cache, Outpost");
    }
}
