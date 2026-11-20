#[cfg(test)]
mod tests {
    use super::super::*; // bring encode/decode into scope

    #[test]
    fn test_encode_decode_roundtrip() {
        let original = "Apocalypse";
        let encoded = encode(original);
        let decoded = decode(&encoded).expect("Decoding should succeed");
        assert_eq!(original, decoded);
    }

    #[test]
    fn test_checksum_validation() {
        let original = "test";
        let mut encoded = encode(original);
        // Corrupt the checksum character (last char)
        let last = encoded.pop().unwrap();
        let corrupted = if last == '0' { '1' } else { '0' };
        encoded.push(corrupted);
        let result = decode(&encoded);
        assert!(result.is_err(), "Checksum mismatch should produce an error");
        assert_eq!(result.unwrap_err(), "Checksum mismatch");
    }
}
