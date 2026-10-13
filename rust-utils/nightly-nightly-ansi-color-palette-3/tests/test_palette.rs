use nightly_ansi_color_palette::generate_palette;

#[test]
fn contains_sample_codes() {
    let palette = generate_palette();
    // Verify that a few known codes appear with correct escape sequences
    assert!(palette.contains("\x1b[48;5;0m  0\x1b[0m"));
    assert!(palette.contains("\x1b[48;5;128m128\x1b[0m"));
    assert!(palette.contains("\x1b[48;5;255m255\x1b[0m"));
    // Ensure exactly 256 color entries are present
    let count = palette.matches("\x1b[48;5;").count();
    assert_eq!(count, 256);
}
