use clap::Parser;
use qrcode::QrCode;
use qrcode::render::unicode;

/// Simple program to generate an ASCII QR code from input text
#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Text to encode into QR code
    #[arg(value_name = "TEXT")]
    text: String,
}

fn generate_qr(text: &str) -> String {
    let code = QrCode::new(text.as_bytes()).unwrap();
    code.render::<unicode::Dense1x2>()
        .quiet_zone(false)
        .build()
}

fn main() {
    let args = Args::parse();
    let qr = generate_qr(&args.text);
    println!("{}", qr);
}
