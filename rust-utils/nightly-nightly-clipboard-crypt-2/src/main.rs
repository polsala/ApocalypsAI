use std::env;
use std::path::Path;

use nightly_clipboard_crypt::{decrypt_from_file, encrypt_and_save};

fn print_usage() {
    eprintln!("Usage:");
    eprintln!("  encrypt <key> <output_file>   # reads stdin");
    eprintln!("  decrypt <key> <input_file>    # writes to stdout");
}

fn main() -> std::io::Result<()> {
    let args: Vec<String> = env::args().collect();
    if args.len() != 4 {
        print_usage();
        std::process::exit(1);
    }
    let command = &args[1];
    let key = &args[2];
    let file_path = Path::new(&args[3]);

    match command.as_str() {
        "encrypt" => {
            let mut input = String::new();
            std::io::stdin().read_to_string(&mut input)?;
            encrypt_and_save(&input, key, file_path)?;
        }
        "decrypt" => {
            let plaintext = decrypt_from_file(key, file_path)?;
            println!("{}", plaintext);
        }
        _ => {
            print_usage();
            std::process::exit(1);
        }
    }
    Ok(())
}
