use std::env;
use qr_code_artist::encode_to_ascii;

fn print_usage() {
    eprintln!("Usage: qr-code-artist \"<text>\"");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        print_usage();
        std::process::exit(1);
    }
    let output = encode_to_ascii(&args[1]);
    println!("{}", output);
}
