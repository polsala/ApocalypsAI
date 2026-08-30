use cryptic_qr::generate_qr;

#[test]
fn test_generate_qr() {
    let result = generate_qr("test");
    let expected = "+------+\\n| tset |\\n+------+\\n";
    assert_eq!(result, expected);
}
