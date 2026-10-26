use std::env;
use qrcode::QrCode;
use qrcode::render::unicode;

/// Generate an ASCII QR code for the given text.
/// Returns the rendered string on success.
fn generate_qr(text: &str) -> Result<String, qrcode::types::QrError> {
    let code = QrCode::new(text.as_bytes())?;
    let rendered = code
        .render::<unicode::Dense1x2>()
        .quiet_zone(false)
        .build();
    Ok(rendered)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        eprintln!("Usage: {} <text>", args[0]);
        std::process::exit(1);
    }
    let text = &args[1];
    match generate_qr(text) {
        Ok(qr) => println!("{}", qr),
        Err(e) => {
            eprintln!("Failed to generate QR code: {}", e);
            std::process::exit(1);
        }
    }
}
