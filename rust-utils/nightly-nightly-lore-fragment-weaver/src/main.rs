use std::fs;
use std::io::{self, Write};
use std::path::PathBuf;
use clap::Parser;

/// A high-performance CLI tool to weave disparate text 'lore fragments' from multiple files
/// into a single output, marking each fragment's origin.
#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
struct Args {
    /// Input text files to weave. Can be specified multiple times.
    #[clap(short, long, value_parser, required = true)]
    input: Vec<PathBuf>,

    /// Output file to write the woven lore to. If not specified, prints to stdout.
    #[clap(short, long, value_parser)]
    output: Option<PathBuf>,
}

fn main() -> io::Result<()> {
    let args = Args::parse();

    let mut woven_content = String::new();

    for path in args.input {
        let filename = path.file_name()
                           .unwrap_or_default()
                           .to_string_lossy();
        
        let content = match fs::read_to_string(&path) {
            Ok(c) => c,
            Err(e) => {
                eprintln!("Error reading file {}: {}", path.display(), e);
                return Err(e);
            }
        };
        
        woven_content.push_str(&format!("\n--- LORE FRAGMENT FROM: {} ---\n\n", filename));
        woven_content.push_str(&content);
        woven_content.push_str("\n\n--- END FRAGMENT ---\n");
    }

    if let Some(output_path) = args.output {
        fs::write(output_path, woven_content.as_bytes())?;
    } else {
        io::stdout().write_all(woven_content.as_bytes())?;
    }

    Ok(())
}
