use clap::{Arg, Command};
use std::fs;
use std::io::{self, Write};

mod ciphers;
mod ascii_art;

use ciphers::*;
use ascii_art::display_ascii_art;

fn main() {
    let matches = Command::new("Nightly Cipher Canvas")
        .version("1.0.0")
        .author("ApocalypsAI")
        .about("A whimsical CLI tool that encrypts text into ASCII art ciphers")
        .arg(
            Arg::new("text")
                .short('t')
                .long("text")
                .value_name("TEXT")
                .help("Text to encrypt")
                .required(true)
        )
        .arg(
            Arg::new("cipher")
                .short('c')
                .long("cipher")
                .value_name("CIPHER")
                .help("Cipher type: caesar, atbash, vigenere")
                .required(true)
                .possible_values(["caesar", "atbash", "vigenere"])
        )
        .arg(
            Arg::new("shift")
                .short('s')
                .long("shift")
                .value_name("SHIFT")
                .help("Caesar cipher shift (default: 3)")
                .default_value("3")
        )
        .arg(
            Arg::new("key")
                .short('k')
                .long("key")
                .value_name("KEY")
                .help("Vigenère cipher key")
        )
        .arg(
            Arg::new("ascii")
                .short('a')
                .long("ascii")
                .help("Display encrypted text as ASCII art")
        )
        .arg(
            Arg::new("output")
                .short('o')
                .long("output")
                .value_name("FILE")
                .help("Output file path")
        )
        .arg(
            Arg::new("help")
                .short('h')
                .long("help")
                .help("Show help information")
        )
        .get_matches();

    let text = matches.get_one::<String>("text").unwrap();
    let cipher_type = matches.get_one::<String>("cipher").unwrap();
    let ascii_art = matches.get_flag("ascii");
    let output_file = matches.get_one::<String>("output");

    // Validate inputs
    if cipher_type == "vigenere" {
        if matches.get_one::<String>("key").is_none() {
            eprintln!("Error: Vigenère cipher requires a key (-k, --key)\nFor help, run: cargo run -- --help");
            std::process::exit(1);
        }
    }

    // Encrypt the text
    let encrypted_text = match cipher_type.as_str() {
        "caesar" => {
            let shift: i32 = matches.get_one::<String>("shift")
                .unwrap()
                .parse()
                .unwrap_or_else(|_| {
                    eprintln!("Error: Invalid shift value. Please provide a valid integer.\nFor help, run: cargo run -- --help");
                    std::process::exit(1);
                });
            
            // Easter egg for shift 42
            if shift == 42 {
                println!("\n🤖 *Beep boop* The Answer to the Ultimate Question of Life, the Universe, and Everything!*");
                println!("   Your message will be shifted by 42 positions. May the odds be ever in your favor!\n");
            }
            
            caesar_cipher(text, shift)
        },
        "atbash" => atbash_cipher(text),
        "vigenere" => {
            let key = matches.get_one::<String>("key").unwrap();
            if key.is_empty() {
                eprintln!("Error: Vigenère cipher key cannot be empty.\nFor help, run: cargo run -- --help");
                std::process::exit(1);
            }
            vigenere_cipher(text, key)
        },
        _ => {
            eprintln!("Error: Unknown cipher type. Use: caesar, atbash, or vigenere\nFor help, run: cargo run -- --help");
            std::process::exit(1);
        }
    };

    // Display or save the result
    if ascii_art {
        println!("\n🎨 *Displaying encrypted text as ASCII art...*\n");
        display_ascii_art(&encrypted_text);
    } else {
        println!("\n🔒 Encrypted text: {}", encrypted_text);
    }

    if let Some(file_path) = output_file {
        match fs::write(file_path, &encrypted_text) {
            Ok(_) => println!("\n💾 Encrypted message saved to: {}", file_path),
            Err(e) => {
                eprintln!("Error: Failed to write to file '{}': {}\nFor help, run: cargo run -- --help", file_path, e);
                std::process::exit(1);
            }
        }
    }
    
    println!("\n✨ Encryption complete! May your secrets be safe and your ASCII art be majestic!\n");
}
