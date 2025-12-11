use nightly_echo_echo::{echo_double, echo_original, echo_reverse};

#[test]
fn test_echo_original() {
    assert_eq!(echo_original("test"), "ECHO: test");
}

#[test]
fn test_echo_reverse() {
    assert_eq!(echo_reverse("abc"), "ECHO: cba");
}

#[test]
fn test_echo_double() {
    assert_eq!(echo_double("ab"), "ECHO: aabb");
}
