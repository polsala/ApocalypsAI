use std::process::Command;

#[test]
fn test_known_values() {
    let output = Command::new("cargo")
        .args(&["run", "--quiet", "--", "100", "45"])
        .output()
        .expect("failed to execute process");
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Time of flight: 14.42 s"));
    assert!(stdout.contains("Max height: 255.10 m"));
    assert!(stdout.contains("Range: 1019.40 m"));
}

#[test]
fn test_zero_angle() {
    let output = Command::new("cargo")
        .args(&["run", "--quiet", "--", "100", "0"])
        .output()
        .expect("failed to execute process");
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Time of flight: 0.00 s"));
    assert!(stdout.contains("Max height: 0.00 m"));
    assert!(stdout.contains("Range: 0.00 m"));
}

#[test]
fn test_ninety_angle() {
    let output = Command::new("cargo")
        .args(&["run", "--quiet", "--", "100", "90"])
        .output()
        .expect("failed to execute process");
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Time of flight: 20.39 s"));
    assert!(stdout.contains("Max height: 510.20 m"));
    assert!(stdout.contains("Range: 0.00 m"));
}

#[test]
fn test_negative_speed() {
    let output = Command::new("cargo")
        .args(&["run", "--quiet", "--", "-100", "45"])
        .output()
        .expect("failed to execute process");
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Time of flight: -14.42 s"));
    assert!(stdout.contains("Max height: 255.10 m"));
    assert!(stdout.contains("Range: 1019.40 m"));
}
