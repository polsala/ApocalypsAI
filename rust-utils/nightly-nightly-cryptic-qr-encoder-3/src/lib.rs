pub fn encode_to_ascii(data: &str) -> String {
    use qrcode::QrCode;
    let code = QrCode::new(data.as_bytes()).expect("Failed to create QR code");
    code.render()
        .light_color(' ')
        .dark_color('█')
        .build()
}
