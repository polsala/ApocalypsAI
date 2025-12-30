#[cfg(test)]
mod tests {
    use super::super::*;
    use std::collections::HashMap;

    #[test]
    fn test_mapping_consistency() {
        let (enc_map, dec_map) = build_maps();
        // Ensure every encoding has a corresponding decoding entry
        for (c, e) in enc_map.iter() {
            assert_eq!(dec_map.get(e), Some(c));
        }
    }

    #[test]
    fn test_encode_simple() {
        let (enc_map, _) = build_maps();
        let input = "abc";
        let expected = "😀😁😂";
        assert_eq!(encode(input, &enc_map), expected);
    }

    #[test]
    fn test_decode_simple() {
        let (_, dec_map) = build_maps();
        let input = "😀😁😂";
        let expected = "abc";
        assert_eq!(decode(input, &dec_map), expected);
    }

    #[test]
    fn test_roundtrip() {
        let (enc_map, dec_map) = build_maps();
        let original = "hello world";
        let encoded = encode(original, &enc_map);
        let decoded = decode(&encoded, &dec_map);
        assert_eq!(decoded, original);
    }

    #[test]
    fn test_unknown_char_passthrough() {
        let (enc_map, _) = build_maps();
        let input = "rust 1.70!";
        // Digits, punctuation, and period are not in the map and should stay unchanged
        let expected = "😐😙😗😗⬜1.70!";
        assert_eq!(encode(input, &enc_map), expected);
    }
}
