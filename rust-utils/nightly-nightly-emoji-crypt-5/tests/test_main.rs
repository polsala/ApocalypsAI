#[cfg(test)]
mod tests {
    use super::*;
    use crate::lib::{encode, decode};

    #[test]
    fn test_encode_basic() {
        let input = "abc xyz";
        let expected = "😀😁😂🟦😶🙄😑";
        assert_eq!(encode(input), expected);
    }

    #[test]
    fn test_decode_basic() {
        let input = "😀😁😂🟦😶🙄😑";
        let expected = "abc xyz";
        assert_eq!(decode(input), expected);
    }

    #[test]
    fn test_roundtrip() {
        let original = "hello world";
        let encoded = encode(original);
        let decoded = decode(&encoded);
        assert_eq!(decoded, original);
    }
}
