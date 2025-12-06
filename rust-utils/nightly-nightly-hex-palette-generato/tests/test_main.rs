#[cfg(test)]
mod tests {
    use nightly_hex_palette_generator::{hex_to_rgb, rgb_to_hex, rgb_to_hsl, hsl_to_rgb, generate_palette};

    #[test]
    fn test_hex_to_rgb() {
        assert_eq!(hex_to_rgb("#000000"), Some((0.0, 0.0, 0.0)));
        assert_eq!(hex_to_rgb("FFFFFF"), Some((255.0, 255.0, 255.0)));
        assert_eq!(hex_to_rgb("#1A2B3C"), Some((26.0, 43.0, 60.0)));
        assert_eq!(hex_to_rgb("GGGGGG"), None);
    }

    #[test]
    fn test_rgb_to_hex() {
        assert_eq!(rgb_to_hex((0.0, 0.0, 0.0)), "#000000");
        assert_eq!(rgb_to_hex((255.0, 255.0, 255.0)), "#FFFFFF");
        assert_eq!(rgb_to_hex((26.0, 43.0, 60.0)), "#1A2B3C");
    }

    #[test]
    fn test_rgb_hsl_roundtrip() {
        let original = (123.0, 200.0, 45.0);
        let hsl = rgb_to_hsl(original);
        let rgb = hsl_to_rgb(hsl);
        assert!((original.0 - rgb.0).abs() < 1.0);
        assert!((original.1 - rgb.1).abs() < 1.0);
        assert!((original.2 - rgb.2).abs() < 1.0);
    }

    #[test]
    fn test_generate_palette_count() {
        let base = (180.0, 0.5, 0.5);
        let palette = generate_palette(base, 4);
        assert_eq!(palette.len(), 4);
        let hues: Vec<f64> = palette.iter().map(|rgb| rgb_to_hsl(*rgb).0).collect();
        let expected = vec![180.0, 270.0, 0.0, 90.0];
        for (h, e) in hues.iter().zip(expected.iter()) {
            assert!((h - e).abs() < 1.0);
        }
    }
}
