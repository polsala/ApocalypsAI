use std::env;
use std::process;

mod cipher;

fn main() {
    let args: Vec<String> = env::args().collect();

    if args.len() < 3 {
        eprintln!("Usage: void-whisperer <encode|decode> <message>");
        process::exit(1);
    }

    let command = &args[1];
    let message = &args[2];

    match command.as_str() {
        "encode" => {
            let encoded = cipher::encode(message);
            println!("{}", encoded);
        },
        "decode" => {
            let decoded = cipher::decode(message);
            println!("{}", decoded);
        },
        _ => {
            eprintln!("Invalid command. Use 'encode' or 'decode'.");
            process::exit(1);
        }
    }
}
