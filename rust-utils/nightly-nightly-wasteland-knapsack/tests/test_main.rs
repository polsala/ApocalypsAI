#[test]
fn test_knapsack_cli() {
    // Create a temporary items file
    let input_path = "tests/items.txt";
    let mut file = std::fs::File::create(input_path).expect("cannot create temp file");
    use std::io::Write;
    writeln!(file, "apple 5 10").unwrap();
    writeln!(file, "bread 4 7").unwrap();
    writeln!(file, "candy 2 4").unwrap();

    // Execute the compiled binary
    let output = std::process::Command::new(env!("CARGO_BIN_EXE_nightly-wasteland-knapsack"))
        .arg("7")
        .arg(input_path)
        .output()
        .expect("failed to run binary");

    assert!(output.status.success(), "process exited with error");
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Optimal total value: 14"), "unexpected total value");
    assert!(stdout.contains("- apple"), "apple should be selected");
    assert!(stdout.contains("- candy"), "candy should be selected");

    // Clean up temporary file
    std::fs::remove_file(input_path).unwrap();
}
