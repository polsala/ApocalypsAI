use std::process::Command;
use regex::Regex;

#[test]
fn test_emoji_echo() {
    let input = "Test message";
    let output = Command::new("cargo")
        .args(&["run", "--quiet", "--", input])
        .output()
        .expect("failed to execute process");
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains(input));
    let re = Regex::new(r"[😀😃😄😁😆😅😂🤣😊😇🙂🙃😉😌😍🥰😘😗😙😚😋😛😝😜🤪🤨🧐🤓😎🤩🥳😏😒😞😔😟😕🙁☹️😣😖😫😩🥺😢😭😤😠😡🤬🤯😳🥵🥶😱😨😰😥😓🤗🤔🤭🤫🤥😶😐😑😬🙄😯😦😧😮😲🥱😴🤤😪😵🤐🥴🤢🤮🤧😷🤒🤕🤑🤠😈👿👹👺🤡💩👻💀☠️👽🤖🎃😺😸😹😻😼😽🙀😿😾]+$" ).unwrap();
    assert!(re.is_match(stdout.trim()));
}
