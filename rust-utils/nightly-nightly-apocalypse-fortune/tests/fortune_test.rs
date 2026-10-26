use std::process::Command;

#[test]
fn runs_and_outputs() {
    // Execute the compiled binary via `cargo run`
    let output = Command::new("cargo")
        .args(&["run", "--quiet"])
        .output()
        .expect("failed to execute cargo run");
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    let known = [
        "You will find a fresh water source behind the old billboard.",
        "A friendly mutant will share its secret stash of canned beans.",
        "Radiation levels will drop tomorrow; perfect time to venture out.",
        "Your compass points to a hidden cache of batteries.",
        "A solar flare will power your solar panel for a full day.",
        "You will discover a functional radio and hear good news.",
        "A stray dog will become your loyal companion.",
        "A sudden rain will reveal a safe path through the dunes.",
        "You will stumble upon a library still intact—knowledge is power.",
        "A mysterious traveler will teach you a new survival skill."
    ];
    let trimmed = stdout.trim();
    assert!(known.contains(&trimmed));
}
