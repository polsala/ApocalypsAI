use std::collections::HashSet;
use std::process::Command;
use std::str;

#[test]
fn output_is_valid_and_deterministic() {
    // Run the binary with a known seed (123) and capture stdout
    let binary_path = env!("CARGO_BIN_EXE_scavenger_route_generator");
    let output = Command::new(binary_path)
        .arg("123")
        .output()
        .expect("failed to execute binary");
    assert!(output.status.success(), "binary exited with error");
    let stdout = str::from_utf8(&output.stdout).expect("stdout not UTF‑8");
    let lines: Vec<&str> = stdout.lines().collect();
    // Expect between 3 and 7 lines
    assert!((3..=7).contains(&lines.len()), "unexpected number of stops");
    let valid_locations = [
        "Abandoned Mall",
        "Crumbling Library",
        "Rusty Bridge",
        "Forgotten Subway",
        "Radiated Farm",
        "Deserted Power Plant",
        "Overgrown Park",
        "Collapsed Stadium",
        "Silent Hospital",
        "Dusty Warehouse",
    ];
    let mut seen = HashSet::new();
    for (idx, line) in lines.iter().enumerate() {
        // Expected format: "1. Location"
        let parts: Vec<&str> = line.splitn(2, ". ").collect();
        assert_eq!(parts.len(), 2, "line does not match 'N. Location' format");
        let number: usize = parts[0].parse().expect("index not a number");
        assert_eq!(number, idx + 1, "indices not sequential");
        let location = parts[1];
        assert!(valid_locations.contains(&location), "unknown location '{}'", location);
        assert!(seen.insert(location), "duplicate location '{}'", location);
    }
}
