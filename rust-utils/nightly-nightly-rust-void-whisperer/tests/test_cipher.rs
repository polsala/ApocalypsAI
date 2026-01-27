#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_encode() {
        assert_eq!(encode("hello"), "mjqqt");
        assert_eq!(encode("world"), "btwqi");
        assert_eq!(encode("Hello World!"), "Mjqqt Btwqi!");
    }

    #[test]
    fn test_decode() {
        assert_eq!(decode("mjqqt"), "hello");
        assert_eq!(decode("btwqi"), "world");
        assert_eq!(decode("Mjqqt Btwqi!"), "Hello World!");
    }

    #[test]
    fn test_encode_decode_roundtrip() {
        let original = "Secret Message 123!";
        let encoded = encode(original);
        let decoded = decode(&encoded);
        assert_eq!(decoded, original);
    }
}
