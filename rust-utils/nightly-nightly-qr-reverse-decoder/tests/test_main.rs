use qr_reverse_decoder::decode_qr;

#[test]
fn test_decode_valid() {
    let input = "QR:!dlroW ,olleH";
    let decoded = decode_qr(input).expect("Should decode valid QR string");
    assert_eq!(decoded, "Hello, World!");
}

#[test]
fn test_decode_invalid_prefix() {
    let input = "INVALID:!dlroW";
    assert!(decode_qr(input).is_none());
}

#[test]
fn test_decode_empty() {
    let input = "QR:";
    let decoded = decode_qr(input).expect("Empty payload should decode to empty string");
    assert_eq!(decoded, "");
}
