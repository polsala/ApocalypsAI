use clap::Parser;
use nightly_qr_ascii_art::generate_qr_ascii;

#[derive(Parser)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Input text to encode. If omitted, reads from stdin.
    text: Option<String>,
}

fn main() {
    let args = Args::parse();
    let input = match args.text {
        Some(t) => t,
        None => {
            let mut buf = String::new();
            std::io::Read::read_to_string(&mut std::io::stdin(), &mut buf).unwrap();
            buf.trim_end().to_string()
        }
    };
    let ascii = generate_qr_ascii(&input);
    print!("{}", ascii);
}
