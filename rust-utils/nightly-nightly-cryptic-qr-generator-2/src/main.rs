use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        eprintln!("Usage: {} <text>", args[0]);
        std::process::exit(1);
    }
    let text = &args[1];
    match nightly_cryptic_qr_generator::generate_qr(text) {
        Ok(s) => println!("{}", s),
        Err(e) => {
            eprintln!("Error generating QR: {}", e);
            std::process::exit(1);
        }
    }
}
