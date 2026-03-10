use std::process::Command;
use std::fs::File;
use std::io::Write;
use std::env;

#[test]
fn test_cli_output() {
    // Create a temporary CSV file with sample items
    let mut temp_path = env::temp_dir();
    temp_path.push("items_test.csv");
    let mut file = File::create(&temp_path).expect("create temp file");
    // name,weight,value
    writeln!(file, "Water,10,60").unwrap();
    writeln!(file, "Food,20,100").unwrap();
    writeln!(file, "Medkit,30,120").unwrap();
    drop(file);

    // Build the binary (quiet to keep test output clean)
    let build = Command::new("cargo")
        .args(&["build", "--quiet"])
        .output()
        .expect("cargo build");
    assert!(build.status.success(), "cargo build failed");

    // Determine the path to the compiled binary
    let mut exe_path = env::current_dir().unwrap();
    exe_path.push("target");
    exe_path.push("debug");
    #[cfg(target_os = "windows")]
    { exe_path.push("nightly_scavenger_knapsack.exe"); }
    #[cfg(not(target_os = "windows"))]
    { exe_path.push("nightly_scavenger_knapsack"); }

    // Run the binary with a capacity that forces selection of Food + Medkit (total weight 50)
    let output = Command::new(exe_path)
        .args(&["--capacity", "50", temp_path.to_str().unwrap()])
        .output()
        .expect("run binary");
    assert!(output.status.success(), "binary exited with error");
    let stdout = String::from_utf8_lossy(&output.stdout);
    // Expected total value: 220 (Food + Medkit)
    assert!(stdout.contains("Total value: 220"), "unexpected total value");
    assert!(stdout.contains("Food"), "Food not selected");
    assert!(stdout.contains("Medkit"), "Medkit not selected");

    // Clean up temporary file
    std::fs::remove_file(temp_path).unwrap();
}
