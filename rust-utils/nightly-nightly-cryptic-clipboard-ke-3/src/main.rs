use std::env;
use std::io::{self, Read, Write};
use cryptic_clipboard::xor_cipher;

fn print_usage() {
    eprintln!("Usage: cryptic-clipboard -e|-d <passphrase>");
    eprintln!("  -e  encrypt stdin");
    eprintln!("  -d  decrypt stdin");
}

fn main() -> io::Result<()> {
    let args: Vec<String> = env::args().collect();
    if args.len() != 3 {
        print_usage();
        std::process::exit(1);
    }
    let _mode = &args[1]; // mode is kept for interface; XOR is symmetric
    let pass = args[2].as_bytes();

    let mut input = Vec::new();
    io::stdin().read_to_end(&mut input)?;

    let output = xor_cipher(&input, pass);
    io::stdout().write_all(&output)?;
    Ok(())
}
