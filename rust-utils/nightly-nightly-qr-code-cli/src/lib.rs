pub fn generate_qr(data: &str) -> String {
    let code = qrcode::QrCode::new(data.as_bytes()).unwrap();
    // Render using dense Unicode block characters (2 rows per line)
    code.render::<qrcode::render::unicode::Dense1x2>()
        .quiet_zone(false)
        .build()
}
