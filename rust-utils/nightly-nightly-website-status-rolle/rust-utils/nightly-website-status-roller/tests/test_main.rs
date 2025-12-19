#[cfg(test)]
mod tests {
    use std::process::Command;
    use std::io::Write;
    use std::fs::File;
    use tempfile::NamedTempFile;
    use mockito::{mock, server_address};

    #[test]
    fn test_status_roller() {
        // Setup mock endpoints
        let _m200 = mock("GET", "/ok")
            .with_status(200)
            .create();
        let _m404 = mock("GET", "/missing")
            .with_status(404)
            .create();

        // Write URLs to temp file
        let tmp_file = NamedTempFile::new().unwrap();
        {
            let mut file = File::create(tmp_file.path()).unwrap();
            writeln!(file, "{}/ok", server_address()).unwrap();
            writeln!(file, "{}/missing", server_address()).unwrap();
        }

        // Run the binary
        let output = Command::new("cargo")
            .args(&["run", "--quiet", "--"])
            .arg(tmp_file.path())
            .output()
            .expect("failed to execute process");

        let stdout = String::from_utf8_lossy(&output.stdout);
        assert!(stdout.contains("200 ✅"));
        assert!(stdout.contains("404 ❌"));
    }
}
