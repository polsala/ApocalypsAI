use emoji_phrase_decoder::decode;

#[test]
fn test_single_mapping() {
    let result = decode("🌞 🍎");
    assert_eq!(result, vec!["sun apple"]);
}

#[test]
fn test_multiple_mapping() {
    let mut result = decode("🐱");
    result.sort();
    let mut expected = vec!["cat", "kitten"];
    expected.sort();
    assert_eq!(result, expected);
}
