use assert_cmd::Command;

#[test]
fn cli_encode_hello_world() {
    let mut cmd = Command::cargo_bin("nightly-emoji-crypt").unwrap();
    cmd.arg("encode").arg("hello world");
    cmd.assert()
        .success()
        .stdout("🦊🐘🦁🦁🦒 🌞🦁🦒🦁🦊\n");
}

#[test]
fn cli_decode_emoji() {
    let mut cmd = Command::cargo_bin("nightly-emoji-crypt").unwrap();
    cmd.arg("decode").arg("🦊🐘🦁🦁🦒 🌞🦁🦒🦁🦊");
    cmd.assert()
        .success()
        .stdout("hello world\n");
}
