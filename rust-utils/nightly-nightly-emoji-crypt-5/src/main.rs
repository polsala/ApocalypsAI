use std::env;
mod lib;

fn print_usage() {
    eprintln!("Usage: nightly-emoji-crypt <encode|decode> <text>");
    eprintln!("Example: nightly-emoji-crypt encode \"hello world\"");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 3 {
        print_usage();
        std::process::exit(1);
    }
    let command = args[1].as_str();
    let payload = args[2].as_str();
    match command {
        "encode" => println!("{}", lib::encode(payload)),
        "decode" => println!("{}", lib::decode(payload)),
        _ => {
            print_usage();
            std::process::exit(1);
        }
    }
}
