use assert_cmd::Command;
use predicates::prelude::*;

#[test]
fn cli_without_args_returns_three_emojis() {
    let mut cmd = Command::cargo_bin("nightly-emoji-moodboard").unwrap();
    cmd.assert()
        .success()
        .stdout(predicate::str::is_match(r"^(\S+\s){2}\S+$").unwrap());
}

#[test]
fn cli_with_known_moods_returns_corresponding_emojis() {
    let mut cmd = Command::cargo_bin("nightly-emoji-moodboard").unwrap();
    cmd.args(["happy", "relaxed", "food"])
        .assert()
        .success()
        .stdout(predicate::str::contains("😄").or(predicate::str::contains("😊")))
        .stdout(predicate::str::contains("🧘‍♂️").or(predicate::str::contains("🌿")))
        .stdout(predicate::str::contains("🍕").or(predicate::str::contains("🍔")));
}
