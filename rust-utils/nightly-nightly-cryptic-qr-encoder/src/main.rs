use clap::Parser;

mod lib;

#[derive(Parser)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Text to encode into a QR code
    text: String,
    /// Add a radiation border around the QR code
    #[arg(short, long)]
    radiation: bool,
}

fn main() {
    let args = Args::parse();
    let mut output = lib::generate_qr_ascii(&args.text);
    if args.radiation {
        output = lib::add_radiation_border(&output);
    }
    println!("{}", output);
}

