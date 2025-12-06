use std::env;
use std::process;
use nightly_hex_palette_generator::{hex_to_rgb, rgb_to_hex, generate_palette, rgb_to_hsl};

fn print_usage() {
    eprintln!("Usage: nightly-hex-palette-generator <hex_color> [count]");
    eprintln!("Example: nightly-hex-palette-generator #3498db 7");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 || args.len() > 3 {
        print_usage();
        process::exit(1);
    }
    let hex = args[1].trim();
    let count: usize = if args.len() == 3 {
        args[2].parse().unwrap_or_else(|_| {
            eprintln!("Invalid count: {}", args[2]);
            process::exit(1);
        })
    } else {
        5
    };
    let base_rgb = match hex_to_rgb(hex) {
        Some(rgb) => rgb,
        None => {
            eprintln!("Invalid hex color: {}", hex);
            process::exit(1);
        }
    };
    let base_hsl = rgb_to_hsl(base_rgb);
    let palette = generate_palette(base_hsl, count);
    for color in palette {
        println!("{}", rgb_to_hex(color));
    }
}
