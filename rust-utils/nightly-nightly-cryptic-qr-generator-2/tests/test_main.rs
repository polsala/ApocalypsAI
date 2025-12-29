use nightly_cryptic_qr_generator::generate_qr;

#[test]
fn test_generate_qr_known_input() {
    // Mock rationale: verify that the library produces the exact same ASCII output as the underlying qrcode crate.
    let result = generate_qr("ABC").unwrap();
    let expected = {
        let code = qrcode::QrCode::new(b"ABC").unwrap();
        code.render::<qrcode::render::unicode::Dense1x2>()
            .quiet_zone(false)
            .build()
    };
    assert_eq!(result, expected);
}
