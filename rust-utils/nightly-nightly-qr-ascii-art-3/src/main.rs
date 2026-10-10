use std::env;
use qr_ascii::generate_qr_ascii;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        eprintln!("Usage: {} <text>", args[0]);
        std::process::exit(1);
    }
    let input = &args[1];
    let ascii = generate_qr_ascii(input);
    println!("{}", ascii);
}
