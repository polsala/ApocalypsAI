use nightly_echo_echo::reverse_string;

#[test]
fn test_reverse_string() {
    assert_eq!(reverse_string("hello"), "olleh");
    assert_eq!(reverse_string("Rust"), "tsuR");
    assert_eq!(reverse_string(""), "");
}
