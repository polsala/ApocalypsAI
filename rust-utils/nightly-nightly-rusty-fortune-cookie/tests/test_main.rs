use std::process::Command;

#[test]
fn test_with_seed() {
    let output = Command::new("cargo")
        .args(&["run", "--quiet", "--", "--seed", "42"])
        .output()
        .expect("failed to execute process");
    let stdout = String::from_utf8_lossy(&output.stdout);
    let expected = "Your fortune: A new friendship will blossom.";
    assert_eq!(stdout.trim(), expected);
}

#[test]
fn test_with_mock_date() {
    let output = Command::new("cargo")
        .env("MOCK_DATE", "2023-01-01")
        .args(&["run", "--quiet"])
        .output()
        .expect("failed to execute process");
    let stdout = String::from_utf8_lossy(&output.stdout);
    let expected = "Your fortune: Your patience will be rewarded.";
    assert_eq!(stdout.trim(), expected);
}

#[test]
fn test_seed_zero() {
    let output = Command::new("cargo")
        .args(&["run", "--quiet", "--", "--seed", "0"])
        .output()
        .expect("failed to execute process");
    let stdout = String::from_utf8_lossy(&output.stdout);
    let expected = "Your fortune: You will find a hidden treasure today.";
    assert_eq!(stdout.trim(), expected);
}

#[test]
fn test_with_date_arg() {
    let output = Command::new("cargo")
        .args(&["run", "--quiet", "--", "--date", "2023-01-01"])
        .output()
        .expect("failed to execute process");
    let stdout = String::from_utf8_lossy(&output.stdout);
    let expected = "Your fortune: Your patience will be rewarded.";
    assert_eq!(stdout.trim(), expected);
}
