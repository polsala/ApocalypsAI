pub fn generate_qr(text: &str) -> Result<String, Box<dyn std::error::Error>> {
    let code = qrcode::QrCode::new(text.as_bytes())?;
    let string = code
        .render::<qrcode::render::unicode::Dense1x2>()
        .quiet_zone(false)
        .build();
    Ok(string)
}
