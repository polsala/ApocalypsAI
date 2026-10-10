use ansi_color_palette::get_ansi_code;

#[test]
fn test_known_colors() {
    assert_eq!(get_ansi_code("red"), Some("31"));
    assert_eq!(get_ansi_code("Bright_Blue"), Some("94"));
    assert_eq!(get_ansi_code("WHITE"), Some("37"));
}

#[test]
fn test_unknown_color() {
    assert_eq!(get_ansi_code("chartreuse"), None);
}
