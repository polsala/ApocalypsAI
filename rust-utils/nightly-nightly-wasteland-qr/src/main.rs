use std::env;
use std::io::Read;
use wasteland_qr::generate_qr_ascii;

fn main() {
    // Collect command‑line arguments; if none are provided, read from stdin.
    let args: Vec<String> = env::args().collect();
    let input = if args.len() > 1 {
        args[1..].join(" ")
    } else {
        let mut buffer = String::new();
        std::io::stdin()
            .read_to_string(&mut buffer)
            .expect("Failed to read stdin");
        buffer.trim().to_string()
    };

    let ascii = generate_qr_ascii(&input);
    println!("{}", ascii);
}
