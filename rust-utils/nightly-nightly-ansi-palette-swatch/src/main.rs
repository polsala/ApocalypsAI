use std::env;
use nightly_ansi_palette_swatch::generate_palette;

fn parse_range(arg: &str) -> Option<(u8, u8)> {
    let parts: Vec<&str> = arg.split('-').collect();
    if parts.len() != 2 {
        return None;
    }
    let start = parts[0].parse::<u8>().ok()?;
    let end = parts[1].parse::<u8>().ok()?;
    if start > end || end > 255 {
        return None;
    }
    Some((start, end))
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let mut start = 0u8;
    let mut end = 255u8;
    if args.len() == 3 && args[1] == "--range" {
        if let Some((s, e)) = parse_range(&args[2]) {
            start = s;
            end = e;
        } else {
            eprintln!("Invalid range. Use --range START-END where 0 <= START <= END <= 255");
            std::process::exit(1);
        }
    } else if args.len() != 1 {
        eprintln!("Usage: {} [--range START-END]", args[0]);
        std::process::exit(1);
    }

    let palette = generate_palette(start, end);
    println!("{}", palette);
}
