// Integration test for the nightly-scavenger-knapsack CLI
// Mock rationale: we use a temporary file with known contents and invoke the binary via std::process.

#[cfg(test)]
mod integration {
    use std::fs::File;
    use std::io::Write;
    use std::process::Command;
    use tempfile::NamedTempFile;

    #[test]
    fn cli_selects_optimal_items() {
        // Prepare a temporary CSV file
        let mut tmp = NamedTempFile::new().expect("failed to create temp file");
        let csv_content = "Water Bottle,2,3\nCanned Food,3,4\nFirst Aid Kit,5,10\nRadio,1,2\n";
        write!(tmp, "{}", csv_content).expect("failed to write csv");
        let path = tmp.path().to_str().unwrap();

        // Run the compiled binary (assumes cargo build has been executed)
        let output = Command::new("cargo")
            .args(&["run", "--quiet", "--release", "--", "7", path])
            .output()
            .expect("failed to execute process");
        let stdout = String::from_utf8_lossy(&output.stdout);
        // Expected output contains First Aid Kit and Radio
        assert!(stdout.contains("First Aid Kit"), "output missing First Aid Kit: {}", stdout);
        assert!(stdout.contains("Radio"), "output missing Radio: {}", stdout);
    }
}
