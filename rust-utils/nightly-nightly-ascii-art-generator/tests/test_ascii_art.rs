use nightly_ascii_art_generator::ascii_art::AsciiArt;
use nightly_ascii_art_generator::fonts::FontType;

#[test]
fn test_basic_ascii_art() {
    let art = AsciiArt::new("A".to_string(), FontType::Standard);
    let result = art.generate_art(&FontType::Standard.get_font());
    
    assert_eq!(result.len(), 6);
    assert!(result[0].contains("A"));
}

#[test]
fn test_empty_string() {
    let art = AsciiArt::new("".to_string(), FontType::Standard);
    let result = art.generate_art(&FontType::Standard.get_font());
    
    assert_eq!(result.len(), 6);
    for line in result {
        assert_eq!(line, "");
    }
}

#[test]
fn test_unknown_character() {
    let art = AsciiArt::new("?".to_string(), FontType::Standard);
    let result = art.generate_art(&FontType::Standard.get_font());
    
    assert_eq!(result.len(), 6);
    assert!(result[2].contains("?"));
}

#[test]
fn test_multiple_characters() {
    let art = AsciiArt::new("AB".to_string(), FontType::Standard);
    let result = art.generate_art(&FontType::Standard.get_font());
    
    assert_eq!(result.len(), 6);
    // Each line should contain both A and B characters
    for line in result {
        assert!(line.contains("A") || line.contains("B"));
    }
}

#[test]
fn test_font_type_to_string() {
    assert_eq!(FontType::Standard.to_string(), "standard");
    assert_eq!(FontType::Slant.to_string(), "slant");
    assert_eq!(FontType::Big.to_string(), "big");
    assert_eq!(FontType::Small.to_string(), "small");
    assert_eq!(FontType::Script.to_string(), "script");
    assert_eq!(FontType::Banner.to_string(), "banner");
}
