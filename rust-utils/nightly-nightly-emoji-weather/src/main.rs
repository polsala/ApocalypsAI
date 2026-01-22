use std::env;
use std::process;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        eprintln!("Usage: {} <weather_code>", args[0]);
        process::exit(1);
    }
    let code = &args[1];
    match crate::weather_code_to_emoji(code) {
        Some(emoji) => println!("{}", emoji),
        None => {
            eprintln!("Unknown weather code: {}", code);
            process::exit(1);
        }
    }
}
