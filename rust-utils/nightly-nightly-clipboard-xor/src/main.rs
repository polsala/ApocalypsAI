use std::env;
use std::process;

use clipboard_xor::{decrypt, encrypt};

fn print_usage() {
    eprintln!("Usage:");
    eprintln!("  clipboard-xor encrypt -k <key> <text>");
    eprintln!("  clipboard-xor decrypt -k <key> <hex>");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 5 {
        print_usage();
        process::exit(1);
    }
    let mode = &args[1];
    let key_flag = &args[2];
    if key_flag != "-k" {
        print_usage();
        process::exit(1);
    }
    let key = &args[3];
    let payload = &args[4];
    match mode.as_str() {
        "encrypt" => {
            let out = encrypt(payload, key);
            println!("{}", out);
        }
        "decrypt" => {
            match decrypt(payload, key) {
                Ok(txt) => println!("{}", txt),
                Err(e) => {
                    eprintln!("Error: {}", e);
                    process::exit(1);
                }
            }
        }
        _ => {
            print_usage();
            process::exit(1);
        }
    }
}

