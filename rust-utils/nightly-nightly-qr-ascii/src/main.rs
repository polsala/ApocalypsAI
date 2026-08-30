use qrcode::QrCode;
use qrcode::render::unicode;

/// Generate an ASCII representation of a QR code for the given data.
///
/// The function returns a `String` containing the rendered QR code.
/// It uses a dense 1x2 Unicode renderer, mapping dark modules to the
/// block character `█` and light modules to a space.
fn generate_qr_ascii(data: &str) -> String {
    // `QrCode::new` returns a Result; we unwrap because the input is always
    // valid UTF‑8 and the QR algorithm cannot fail for reasonable lengths.
    let code = QrCode::new(data.as_bytes()).unwrap();
    code.render::<unicode::Dense1x2>()
        .dark_color('█')
        .light_color(' ')
        .build()
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() != 2 {
        eprintln!("Usage: {} <text>", args[0]);
        std::process::exit(1);
    }
    let qr = generate_qr_ascii(&args[1]);
    println!("{}", qr);
}
