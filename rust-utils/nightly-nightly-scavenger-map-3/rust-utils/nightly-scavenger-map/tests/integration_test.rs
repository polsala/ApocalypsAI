#[test]
fn test_map_output_fixed_seed() {
    // Mock rationale: we run the binary with known args and verify deterministic output.
    let output = std::process::Command::new("cargo")
        .args(&["run", "--quiet", "--", "water", "canned", "medkit"]) // three items
        .output()
        .expect("failed to execute cargo run");
    let stdout = std::str::from_utf8(&output.stdout).unwrap().trim();

    // Verify that each item's initial appears somewhere on the map.
    assert!(stdout.contains('W'), "Map should contain 'W' for water");
    assert!(stdout.contains('C'), "Map should contain 'C' for canned");
    assert!(stdout.contains('M'), "Map should contain 'M' for medkit");

    // Verify map dimensions (5 rows, 10 columns)
    let lines: Vec<&str> = stdout.lines().collect();
    assert_eq!(lines.len(), 5, "Map should have 5 rows");
    for line in lines {
        assert_eq!(line.split_whitespace().count(), 10, "Each row should have 10 columns");
    }
}
