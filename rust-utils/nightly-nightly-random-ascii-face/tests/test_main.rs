use std::process::Command;
use std::str;

fn run_cli(args: &[&str]) -> String {
    let output = Command::new("cargo")
        .args(&["run", "--quiet", "--"])
        .args(args)
        .output()
        .expect("failed to execute process");
    assert!(output.status.success(), "Command failed: {:?}", output);
    str::from_utf8(&output.stdout).unwrap().trim().to_string()
}

#[test]
fn test_deterministic_smile() {
    let output = run_cli(&["--seed", "42", "--style", "smile"]);
    assert_eq!(output, "(^_^)" );
}

#[test]
fn test_random_frown() {
    let output = run_cli(&["--seed", "123", "--style", "frown"]);
    assert_eq!(output, ">_~" );
}

#[test]
fn test_any_style() {
    let output = run_cli(&["--seed", "999"]);
    // Should be one of the faces
    let faces = vec!["(^_^)", ">^.^<", ">_<", ">_~", "(O_O)", "(O_o)"];
    assert!(faces.contains(&output.as_str()));
}
