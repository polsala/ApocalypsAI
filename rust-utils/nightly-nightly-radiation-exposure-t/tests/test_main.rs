use std::fs::File;
use std::io::Write;
use std::path::PathBuf;
use std::env;

#[test]
fn test_parse_and_compute_valid() {
    // Mock rationale: create a temporary CSV file with known dose values.
    let mut tmp_path = env::temp_dir();
    tmp_path.push("test_exposure_valid.csv");
    let mut file = File::create(&tmp_path).expect("create temp file");
    writeln!(file, "2023-01-01T12:00:00Z,0.5").unwrap();
    writeln!(file, "2023-01-02T08:30:00Z,1.2").unwrap();
    let result = nightly_radiation_exposure_tracker::parse_and_compute(tmp_path.to_str().unwrap());
    assert_eq!(result.unwrap(), 1.7);
    std::fs::remove_file(tmp_path).unwrap();
}

#[test]
fn test_parse_and_compute_invalid_format() {
    // Mock rationale: create a temporary CSV with a malformed line.
    let mut tmp_path = env::temp_dir();
    tmp_path.push("test_exposure_invalid.csv");
    let mut file = File::create(&tmp_path).expect("create temp file");
    writeln!(file, "bad_line_without_comma").unwrap();
    let result = nightly_radiation_exposure_tracker::parse_and_compute(tmp_path.to_str().unwrap());
    assert!(result.is_err());
    std::fs::remove_file(tmp_path).unwrap();
}
