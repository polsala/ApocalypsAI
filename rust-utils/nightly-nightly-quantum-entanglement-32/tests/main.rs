use std::fs;
use std::path::Path;
use std::process::Command;

const BIN_PATH: &str = "target/release/nightly-quantum-entanglement-checker";

/// Test helper to run the binary and capture output
fn run_checker(args: &[&str]) -> (i32, String, String) {
    let output = Command::new(BIN_PATH)
        .args(args)
        .output()
        .expect("Failed to execute quantum entanglement checker");
    
    let stdout = String::from_utf8_lossy(&output.stdout).to_string();
    let stderr = String::from_utf8_lossy(&output.stderr).to_string();
    let exit_code = output.status.code().unwrap_or(-1);
    
    (exit_code, stdout, stderr)
}

/// Setup test files
fn setup_test_files() {
    // Create test directory
    fs::create_dir_all("tests/data").unwrap();
    
    // Test file 1: Identical content
    fs::write("tests/data/identical1.rs", "fn hello() { println!(\"world\"); }").unwrap();
    fs::write("tests/data/identical2.rs", "fn hello() { println!(\"world\"); }").unwrap();
    
    // Test file 2: Similar content with minor differences
    fs::write("tests/data/similar1.rs", "fn add(a: i32, b: i32) -> i32 { a + b }").unwrap();
    fs::write("tests/data/similar2.rs", "fn add(a: i32, b: i32) -> i32 { b + a }").unwrap();
    
    // Test file 3: Completely different content
    fs::write("tests/data/different1.rs", "fn main() { println!(\"Hello World\"); }").unwrap();
    fs::write("tests/data/different2.rs", "struct Point { x: f64, y: f64; }").unwrap();
    
    // Test file 4: Empty files
    fs::write("tests/data/empty1.rs", "").unwrap();
    fs::write("tests/data/empty2.rs", "").unwrap();
    
    // Test file 5: Large files
    let large_content = "fn test() { " + &"println!(\"test\"); "repeat(1000) + " }";
    fs::write("tests/data/large1.rs", &large_content).unwrap();
    fs::write("tests/data/large2.rs", &large_content).unwrap();
}

/// Cleanup test files
fn cleanup_test_files() {
    let test_files = [
        "tests/data/identical1.rs",
        "tests/data/identical2.rs",
        "tests/data/similar1.rs",
        "tests/data/similar2.rs",
        "tests/data/different1.rs",
        "tests/data/different2.rs",
        "tests/data/empty1.rs",
        "tests/data/empty2.rs",
        "tests/data/large1.rs",
        "tests/data/large2.rs",
        "tests/data/report.json",
    ];
    
    for file in test_files {
        if Path::new(file).exists() {
            fs::remove_file(file).unwrap();
        }
    }
    
    if Path::new("tests/data").exists() {
        fs::remove_dir("tests/data").unwrap();
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_help_output() {
        let (exit_code, stdout, stderr) = run_checker(&["--help"]);
        
        assert_eq!(exit_code, 0);
        assert!(stdout.contains("Quantum-inspired code entanglement checker"));
        assert!(stdout.contains("--file1"));
        assert!(stdout.contains("--file2"));
        assert!(stdout.contains("--uncertainty"));
        assert!(stderr.is_empty());
    }

    #[test]
    fn test_version_output() {
        let (exit_code, stdout, stderr) = run_checker(&["--version"]);
        
        assert_eq!(exit_code, 0);
        assert!(stdout.contains("nightly-quantum-entanglement-checker"));
        assert!(stderr.is_empty());
    }

    #[test]
    fn test_missing_required_arguments() {
        let (exit_code, stdout, stderr) = run_checker(&[]);
        
        assert_ne!(exit_code, 0);
        assert!(stderr.contains("Must specify either --file1 or --text1"));
    }

    #[test]
    fn test_file_not_found() {
        let (exit_code, stdout, stderr) = run_checker(&[
            "--file1", "nonexistent1.rs",
            "--file2", "nonexistent2.rs"
        ]);
        
        assert_ne!(exit_code, 0);
        assert!(stderr.contains("does not exist"));
    }

    #[test]
    fn test_identical_files() {
        setup_test_files();
        
        let (exit_code, stdout, stderr) = run_checker(&[
            "--file1", "tests/data/identical1.rs",
            "--file2", "tests/data/identical2.rs",
            "--uncertainty", "0.1"
        ]);
        
        assert_eq!(exit_code, 0); // Entangled
        assert!(stdout.contains("QUANTUM ENTANGLEMENT DETECTED"));
        assert!(stdout.contains("Similarity Score: 100.000%"));
        assert!(stdout.contains("Confidence Level: VERY_HIGH"));
        assert!(stderr.is_empty());
        
        cleanup_test_files();
    }

    #[test]
    fn test_similar_files_with_uncertainty() {
        setup_test_files();
        
        let (exit_code, stdout, stderr) = run_checker(&[
            "--file1", "tests/data/similar1.rs",
            "--file2", "tests/data/similar2.rs",
            "--uncertainty", "0.2"
        ]);
        
        assert_eq!(exit_code, 0); // Should be entangled with higher uncertainty
        assert!(stdout.contains("QUANTUM ENTANGLEMENT DETECTED"));
        assert!(stdout.contains("Similarity Score:"));
        assert!(stderr.is_empty());
        
        cleanup_test_files();
    }

    #[test]
    fn test_similar_files_without_uncertainty() {
        setup_test_files();
        
        let (exit_code, stdout, stderr) = run_checker(&[
            "--file1", "tests/data/similar1.rs",
            "--file2", "tests/data/similar2.rs",
            "--uncertainty", "0.0"
        ]);
        
        assert_eq!(exit_code, 1); // Should NOT be entangled with zero uncertainty
        assert!(stdout.contains("NO QUANTUM ENTANGLEMENT"));
        assert!(stdout.contains("Similarity Score:"));
        assert!(stderr.is_empty());
        
        cleanup_test_files();
    }

    #[test]
    fn test_different_files() {
        setup_test_files();
        
        let (exit_code, stdout, stderr) = run_checker(&[
            "--file1", "tests/data/different1.rs",
            "--file2", "tests/data/different2.rs",
            "--uncertainty", "0.1"
        ]);
        
        assert_eq!(exit_code, 1); // Not entangled
        assert!(stdout.contains("NO QUANTUM ENTANGLEMENT"));
        assert!(stdout.contains("Similarity Score:"));
        assert!(stderr.is_empty());
        
        cleanup_test_files();
    }

    #[test]
    fn test_empty_files() {
        setup_test_files();
        
        let (exit_code, stdout, stderr) = run_checker(&[
            "--file1", "tests/data/empty1.rs",
            "--file2", "tests/data/empty2.rs",
            "--uncertainty", "0.1"
        ]);
        
        assert_eq!(exit_code, 0); // Identical empty files should be entangled
        assert!(stdout.contains("QUANTUM ENTANGLEMENT DETECTED"));
        assert!(stdout.contains("Similarity Score: 100.000%"));
        assert!(stderr.is_empty());
        
        cleanup_test_files();
    }

    #[test]
    fn test_text_input() {
        let (exit_code, stdout, stderr) = run_checker(&[
            "--text1", "fn test() { return 42; }",
            "--text2", "fn test() { return 42; }",
            "--uncertainty", "0.1"
        ]);
        
        assert_eq!(exit_code, 0); // Identical text should be entangled
        assert!(stdout.contains("QUANTUM ENTANGLEMENT DETECTED"));
        assert!(stdout.contains("Similarity Score: 100.000%"));
        assert!(stderr.is_empty());
    }

    #[test]
    fn test_mixed_input_types() {
        setup_test_files();
        
        let (exit_code, stdout, stderr) = run_checker(&[
            "--file1", "tests/data/identical1.rs",
            "--text2", "fn hello() { println!(\"world\"); }",
            "--uncertainty", "0.1"
        ]);
        
        assert_eq!(exit_code, 0); // File and identical text should be entangled
        assert!(stdout.contains("QUANTUM ENTANGLEMENT DETECTED"));
        assert!(stdout.contains("Similarity Score: 100.000%"));
        assert!(stderr.is_empty());
        
        cleanup_test_files();
    }

    #[test]
    fn test_json_output_format() {
        setup_test_files();
        
        let (exit_code, stdout, stderr) = run_checker(&[
            "--file1", "tests/data/identical1.rs",
            "--file2", "tests/data/identical2.rs",
            "--format", "json"
        ]);
        
        assert_eq!(exit_code, 0);
        assert!(stdout.starts_with("{\n"));
        assert!(stdout.contains("\"entangled\": true"));
        assert!(stdout.contains("\"source_a\""));
        assert!(stdout.contains("\"source_b\""));
        assert!(stdout.contains("\"hash_a\""));
        assert!(stdout.contains("\"hash_b\""));
        assert!(stderr.is_empty());
        
        cleanup_test_files();
    }

    #[test]
    fn test_report_generation() {
        setup_test_files();
        
        let (exit_code, stdout, stderr) = run_checker(&[
            "--file1", "tests/data/identical1.rs",
            "--file2", "tests/data/identical2.rs",
            "--report", "tests/data/report.json",
            "--verbose"
        ]);
        
        assert_eq!(exit_code, 0);
        assert!(stdout.contains("QUANTUM ENTANGLEMENT DETECTED"));
        assert!(stdout.contains("Report saved to:"));
        assert!(stderr.is_empty());
        
        // Verify report file was created
        assert!(Path::new("tests/data/report.json").exists());
        
        let report_content = fs::read_to_string("tests/data/report.json").unwrap();
        assert!(report_content.contains("entangled"));
        assert!(report_content.contains("source_a"));
        assert!(report_content.contains("source_b"));
        
        cleanup_test_files();
    }

    #[test]
    fn test_verbose_output() {
        setup_test_files();
        
        let (exit_code, stdout, stderr) = run_checker(&[
            "--file1", "tests/data/identical1.rs",
            "--file2", "tests/data/identical2.rs",
            "--verbose"
        ]);
        
        assert_eq!(exit_code, 0);
        assert!(stdout.contains("Source A:"));
        assert!(stdout.contains("Source B:"));
        assert!(stdout.contains("Processing Time:"));
        assert!(stderr.is_empty());
        
        cleanup_test_files();
    }

    #[test]
    fn test_uncertainty_validation() {
        let (exit_code, stdout, stderr) = run_checker(&[
            "--text1", "test",
            "--text2", "test",
            "--uncertainty", "1.5"
        ]);
        
        assert_ne!(exit_code, 0);
        assert!(stderr.contains("invalid value\"1.5\"") || stderr.contains("range"));
    }

    #[test]
    fn test_large_files_performance() {
        setup_test_files();
        
        let (exit_code, stdout, stderr) = run_checker(&[
            "--file1", "tests/data/large1.rs",
            "--file2", "tests/data/large2.rs",
            "--verbose"
        ]);
        
        assert_eq!(exit_code, 0);
        assert!(stdout.contains("QUANTUM ENTANGLEMENT DETECTED"));
        assert!(stdout.contains("Processing Time:"));
        
        // Should be fast (under 1000ms for identical large files)
        let lines: Vec<&str> = stdout.lines().collect();
        let processing_time_line = lines.iter().find(|&&line| line.contains("Processing Time:"));
        if let Some(line) = processing_time_line {
            if let Some(time_str) = line.split_whitespace().last() {
                if let Ok(time_ms) = time_str.trim_end_matches("ms").parse::<u32>() {
                    assert!(time_ms < 1000, "Processing took too long: {} ms", time_ms);
                }
            }
        }
        
        assert!(stderr.is_empty());
        
        cleanup_test_files();
    }

    #[test]
    fn test_conflicting_arguments() {
        let (exit_code, stdout, stderr) = run_checker(&[
            "--file1", "test.rs",
            "--text1", "fn test() {}"
        ]);
        
        assert_ne!(exit_code, 0);
        assert!(stderr.contains("cannot be used with"));
    }

    #[test]
    fn test_hash_consistency() {
        // Test that identical content produces identical hashes
        let content = "fn test() { let x = 42; }";
        
        // Write same content to two files
        fs::write("tests/data/hash_test1.rs", content).unwrap();
        fs::write("tests/data/hash_test2.rs", content).unwrap();
        
        let (exit_code1, stdout1, _) = run_checker(&[
            "--file1", "tests/data/hash_test1.rs",
            "--file2", "tests/data/hash_test1.rs",
            "--uncertainty", "0.0"
        ]);
        
        let (exit_code2, stdout2, _) = run_checker(&[
            "--file1", "tests/data/hash_test1.rs",
            "--file2", "tests/data/hash_test2.rs",
            "--uncertainty", "0.0"
        ]);
        
        assert_eq!(exit_code1, 0);
        assert_eq!(exit_code2, 0);
        assert!(stdout1.contains("Similarity Score: 100.000%"));
        assert!(stdout2.contains("Similarity Score: 100.000%"));
        
        cleanup_test_files();
    }
}
