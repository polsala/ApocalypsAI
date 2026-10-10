use clap::Parser;
use qrcode::QrCode;
use qrcode::render::unicode;

/// Simple program to generate ASCII QR codes
#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Text to encode
    text: String,

    /// Reverse the text before encoding
    #[arg(short, long)]
    reverse: bool,
}

fn main() {
    let args = Args::parse();

    let mut data = args.text;
    if args.reverse {
        data = data.chars().rev().collect();
    }

    // Generate QR code
    let code = QrCode::new(data).expect("Failed to generate QR code");

    // Render as Unicode block characters (dense 1x2)
    let string = code.render::<unicode::Dense1x2>()
        .quiet_zone(false)
        .build();

    println!("{}", string);
}
