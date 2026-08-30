use std::env;
use std::process;

mod lib;

fn main() {
    let args: Vec<String> = env::args().collect();
    // args[0] is the program name
    let input = if args.len() > 1 { Some(args[1].as_str()) } else { None };
    match lib::parse_and_format(input) {
        Ok(emoji) => println!("{}", emoji),
        Err(msg) => {
            eprintln!("{}", msg);
            process::exit(1);
        }
    }
}
