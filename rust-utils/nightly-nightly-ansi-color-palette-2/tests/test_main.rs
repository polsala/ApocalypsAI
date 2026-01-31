use assert_cmd::Command;
use predicates::str::contains;

#[test]
fn prints_palette_grid() {
    // Run the compiled binary
    let mut cmd = Command::cargo_bin("nightly-ansi-color-palette").unwrap();
    cmd.assert()
        .success()
        // Spot‑check a few known entries in the output
        .stdout(contains("  0 #000000 █"))
        .stdout(contains("  9 #ff0000 █"))
        .stdout(contains(" 21 #0000ff █"))
        .stdout(contains("232 #080808 █"))
        .stdout(contains("255 #eeeeee █"));
}
