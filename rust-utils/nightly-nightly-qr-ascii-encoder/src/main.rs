use std::env;
use qr_ascii_encoder::encode_to_ascii;

fn main() {
    let args: Vec<String> = env::args().skip(1).collect();
    if args.is_empty() {
        eprintln!("Usage: {} <text>", env::args().next().unwrap());
        std::process::exit(1);
    }
    let input = args.join(" ");
    let ascii = encode_to_ascii(&input);
    print!("{}", ascii);
}
