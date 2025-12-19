use std::env;
use std::process;

mod ascii_art;
mod fonts;

use ascii_art::AsciiArt;
use fonts::{Font, FontType};

fn main() {
    let args: Vec<String> = env::args().collect();
    
    if args.len() < 2 {
        print_usage();
        process::exit(1);
    }
    
    let command = &args[1];
    
    match command.as_str() {
        "--help" | "-h" => print_usage(),
        "--list-fonts" | "-l" => list_fonts(),
        "--preview-all" | "-p" => preview_all(),
        _ => {
            let text = command;
            let mut font_type = FontType::Standard;
            
            // Check for --font option
            if args.len() >= 4 && args[2] == "--font" {
                font_type = match args[3].as_str() {
                    "standard" => FontType::Standard,
                    "slant" => FontType::Slant,
                    "big" => FontType::Big,
                    "small" => FontType::Small,
                    "script" => FontType::Script,
                    "banner" => FontType::Banner,
                    _ => {
                        eprintln!("Unknown font: {}. Use --list-fonts to see available fonts.", args[3]);
                        process::exit(1);
                    }
                };
            }
            
            let art = AsciiArt::new(text.to_string(), font_type);
            art.print();
        }
    }
}

fn print_usage() {
    println!("Nightly ASCII Art Generator");
    println!("Usage:");
    println!("  nightly-ascii-art-generator <text> [options]");
    println!("  nightly-ascii-art-generator --help | -h");
    println!("  nightly-ascii-art-generator --list-fonts | -l");
    println!("  nightly-ascii-art-generator --preview-all | -p");
    println!("");
    println!("Options:");
    println!("  --font <font>  Use specific font (standard, slant, big, small, script, banner)");
    println!("  --help, -h     Show this help message");
    println!("  --list-fonts, -l  List all available fonts");
    println!("  --preview-all, -p  Preview all fonts with sample text");
}

fn list_fonts() {
    println!("Available fonts:");
    for font in [FontType::Standard, FontType::Slant, FontType::Big, FontType::Small, FontType::Script, FontType::Banner] {
        println!("  {}", font.to_string());
    }
}

fn preview_all() {
    let sample_text = "ApocalypsAI";
    let fonts = [FontType::Standard, FontType::Slant, FontType::Big, FontType::Small, FontType::Script, FontType::Banner];
    
    for font in fonts {
        println!("\n=== {} ===", font.to_string());
        let art = AsciiArt::new(sample_text.to_string(), font);
        art.print();
        println!();
    }
}
