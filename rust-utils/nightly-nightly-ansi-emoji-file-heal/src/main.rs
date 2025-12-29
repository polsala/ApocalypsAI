use std::env;
use std::process;
use std::path::Path;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        eprintln!("Usage: {} <directory>", args[0]);
        process::exit(1);
    }
    let dir = Path::new(&args[1]);
    match crate::analyze_path(dir) {
        Ok(files) => {
            for f in files {
                let emoji = if f.healthy { "✅" } else { "❌" };
                println!("📁 {} | {:.1} KB | {} lines | {}", f.path.display(), f.size as f64 / 1024.0, f.lines, emoji);
            }
        }
        Err(e) => {
            eprintln!("Error: {}", e);
            process::exit(1);
        }
    }
}
