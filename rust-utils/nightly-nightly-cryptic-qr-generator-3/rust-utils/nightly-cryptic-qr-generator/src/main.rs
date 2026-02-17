use std::env;
use cryptic_qr::generate_qr;

fn print_usage() {
    eprintln!("Usage: cryptic-qr <text>");
}

fn main() {
    let args: Vec<String> = env::args().skip(1).collect();
    if args.is_empty() {
        print_usage();
        std::process::exit(1);
    }
    let input = args.join(" ");
    let qr = generate_qr(&input);
    println!("{}", qr);
}
