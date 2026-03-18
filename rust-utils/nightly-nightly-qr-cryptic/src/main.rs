use clap::Parser;
use nightly_qr_cryptic::{generate_qr_matrix, render_ascii, rotate_matrix};

/// Simple QR code generator with optional rotation.
#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// The text to encode into a QR code
    text: String,

    /// Number of 90° clockwise rotations (0‑3)
    #[arg(short, long, default_value_t = 0, value_parser = clap::value_parser!(u8).range(0..=3))]
    rotate: u8,
}

fn main() {
    let args = Args::parse();
    let matrix = generate_qr_matrix(&args.text);
    let rotated = rotate_matrix(matrix, args.rotate);
    let ascii = render_ascii(&rotated);
    print!("{}", ascii);
}
