use ansi_color_palette::get_ansi_code;
use std::env;

fn main() {
    let args: Vec<String> = env::args().skip(1).collect();
    if args.is_empty() {
        eprintln!("Usage: <color>");
        std::process::exit(1);
    }
    let color = &args[0];
    match get_ansi_code(color) {
        Some(code) => println!("{}", code),
        None => {
            eprintln!("Unsupported color: {}", color);
            std::process::exit(1);
        }
    }
}
