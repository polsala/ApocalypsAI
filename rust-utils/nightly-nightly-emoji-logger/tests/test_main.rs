use std::io::Cursor;
use nightly_emoji_logger::process;

#[test]
fn test_process() {
    let input = "First line
Second line
Third line
";
    let mut output = Vec::new();
    process(Cursor::new(input), &mut output).unwrap();
    let output_str = String::from_utf8(output).unwrap();
    let expected = "ð First line
ð Second line
ð¥ Third line
";
    assert_eq!(output_str, expected);
}

