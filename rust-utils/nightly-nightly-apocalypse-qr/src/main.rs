use clap::Parser;
use nightly_apocalypse_qr::generate_qr_ascii;

/// Simple CLI to generate ASCII QR codes.
#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// The text to encode into a QR code
    data: String,

    /// Wrap the QR code in a radiation‑symbol border
    #[arg(short, long)]
    radiation: bool,
}

fn main() {
    let args = Args::parse();
    let output = generate_qr_ascii(&args.data, args.radiation);
    println!("{}", output);
}
