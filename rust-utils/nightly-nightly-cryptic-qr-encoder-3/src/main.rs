use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        eprintln!("Usage: {} <text>", args[0]);
        std::process::exit(1);
    }
    let output = cryptic_qr_encoder::encode_to_ascii(&args[1]);
    println!("{}", output);
}
