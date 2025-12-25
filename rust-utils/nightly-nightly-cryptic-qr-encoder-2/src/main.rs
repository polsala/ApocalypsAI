use clap::Parser;
use nightly_cryptic_qr_encoder::render_qr_ascii;

/// Simple CLI to print an ASCII QR code.
#[derive(Parser)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Text to encode into QR
    text: String,
}

fn main() {
    let args = Args::parse();
    let ascii = render_qr_ascii(&args.text);
    println!("{}", ascii);
}
