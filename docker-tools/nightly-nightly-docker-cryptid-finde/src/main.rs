use std::env;
use cryptid_finder::get_cryptid;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        eprintln!("Usage: {} <location>", args[0]);
        std::process::exit(1);
    }
    let location = &args[1];
    let cryptid = get_cryptid(location);
    println!("{}", cryptid);
}
