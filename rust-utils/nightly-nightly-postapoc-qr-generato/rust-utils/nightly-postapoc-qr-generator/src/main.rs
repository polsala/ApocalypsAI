use clap::Parser;
use qrcode::QrCode;
use qrcode::render::unicode;
use colored::*;

/// Post-apocalyptic ASCII QR code generator
#[derive(Parser)]
#[command(author, version, about = "Generate an ASCII QR code for the wasteland")]
struct Args {
    /// Text to encode into the QR code
    #[arg()]
    text: String,
}

fn main() {
    let args = Args::parse();
    let code = QrCode::new(args.text).expect("Failed to generate QR code");
    let qr_string = code
        .render::<unicode::Dense1x2>()
        .dark_color("\u{2588}\u{2588}")
        .light_color("  ")
        .build();
    println!("{}", qr_string.blue());
}
