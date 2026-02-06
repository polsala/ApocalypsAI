#[test]
fn test_unfair_trade_cli() {
    // Run the binary via `cargo run` with sample arguments.
    let output = std::process::Command::new("cargo")
        .args(&["run", "--quiet", "--", "give", "water=2", "receive", "ammo=1"])
        .output()
        .expect("failed to execute cargo");
    let stdout = String::from_utf8_lossy(&output.stdout);
    // water=2 => value 4, ammo=1 => value 5, so the giver loses value.
    assert!(stdout.contains("Unfair trade"));
}
