use std::env;
use std::process;

const DEFAULT_ALPHABET: &str = "abcdefghijklmnopqrstuvwxyz";
const DEFAULT_KEY: usize = 3;

fn main() {
    let args: Vec<String> = env::args().collect();

    if args.len() < 2 {
        print_usage();
        process::exit(1);
    }

    let command = &args[1];

    match command.as_str() {
        "encrypt" => encrypt_message(&args[2..]),
        "decrypt" => decrypt_message(&args[2..]),
        _ => {
            eprintln!("Unknown command: {}", command);
            print_usage();
            process::exit(1);
        }
    }
}

fn print_usage() {
    println!(
        "Usage:\n"
        "  nightly-crypto-cipher-box encrypt <message> [--alphabet <alphabet>] [--key <key>]\n"
        "  nightly-crypto-cipher-box decrypt <message> [--alphabet <alphabet>] [--key <key>]\n"
        "\n"
        "Commands:\n"
        "  encrypt  Encrypt a message using a custom substitution cipher\n"
        "  decrypt  Decrypt a message using a custom substitution cipher\n"
        "\n"
        "Options:\n"
        "  --alphabet <alphabet>  Custom alphabet to use (default: abcdefghijklmnopqrstuvwxyz)\n"
        "  --key <key>            Key for the cipher (default: 3)\n"
    );
}

fn encrypt_message(args: &[String]) {
    let (message, alphabet, key) = parse_args(args);
    let encrypted = encrypt(&message, &alphabet, key);
    println!("Encrypted message: {}", encrypted);
}

fn decrypt_message(args: &[String]) {
    let (message, alphabet, key) = parse_args(args);
    let decrypted = decrypt(&message, &alphabet, key);
    println!("Decrypted message: {}", decrypted);
}

fn parse_args(args: &[String]) -> (String, String, usize) {
    let mut message = String::new();
    let mut alphabet = DEFAULT_ALPHABET.to_string();
    let mut key = DEFAULT_KEY;

    let mut i = 0;
    while i < args.len() {
        match args[i].as_str() {
            "--alphabet" => {
                if i + 1 < args.len() {
                    alphabet = args[i + 1].clone();
                    i += 1;
                } else {
                    eprintln!("--alphabet requires a value");
                    process::exit(1);
                }
            }
            "--key" => {
                if i + 1 < args.len() {
                    key = args[i + 1].parse().expect("--key must be a number");
                } else {
                    eprintln!("--key requires a value");
                    process::exit(1);
                }
            }
            _ => {
                if message.is_empty() {
                    message = args[i].clone();
                } else {
                    eprintln!("Unknown argument: {}", args[i]);
                    process::exit(1);
                }
            }
        }
        i += 1;
    }

    if message.is_empty() {
        eprintln!("No message provided");
        process::exit(1);
    }

    (message, alphabet, key)
}

fn encrypt(message: &str, alphabet: &str, key: usize) -> String {
    let alphabet_chars: Vec<char> = alphabet.chars().collect();
    let mut result = String::new();

    for ch in message.chars() {
        if ch.is_ascii_alphabetic() {
            let is_upper = ch.is_ascii_uppercase();
            let ch_lower = ch.to_ascii_lowercase();
            if let Some(pos) = alphabet_chars.iter().position(|&c| c == ch_lower) {
                let new_pos = (pos + key) % alphabet_chars.len();
                let new_char = alphabet_chars[new_pos];
                result.push(if is_upper { new_char.to_ascii_uppercase() } else { new_char });
            } else {
                result.push(ch);
            }
        } else {
            result.push(ch);
        }
    }

    result
}

fn decrypt(message: &str, alphabet: &str, key: usize) -> String {
    let alphabet_chars: Vec<char> = alphabet.chars().collect();
    let mut result = String::new();

    for ch in message.chars() {
        if ch.is_ascii_alphabetic() {
            let is_upper = ch.is_ascii_uppercase();
            let ch_lower = ch.to_ascii_lowercase();
            if let Some(pos) = alphabet_chars.iter().position(|&c| c == ch_lower) {
                let new_pos = (pos + alphabet_chars.len() - (key % alphabet_chars.len())) % alphabet_chars.len();
                let new_char = alphabet_chars[new_pos];
                result.push(if is_upper { new_char.to_ascii_uppercase() } else { new_char });
            } else {
                result.push(ch);
            }
        } else {
            result.push(ch);
        }
    }

    result
}
