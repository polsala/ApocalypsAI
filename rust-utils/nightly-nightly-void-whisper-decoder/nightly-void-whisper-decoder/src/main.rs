use clap::Parser;
use std::io::{self, Read};
use void_whisper_decoder::decode_message;

#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
struct Args {
    /// Input file to decode. Reads from stdin if not provided.
    #[clap(short, long)]
    file: Option<String>,

    /// Apply a simple character interpretation (e.g., X->E, Z->S).
    #[clap(short, long, action)]
    interpret: bool,

    /// Highlight known survival keywords.
    #[clap(short, long, action)]
    highlight_keywords: bool,

    /// Show character frequency analysis.
    #[clap(short, long, action)]
    frequency_analysis: bool,
}

fn main() -> io::Result<()> {
    let args = Args::parse();

    let mut input_content = String::new();

    match args.file {
        Some(file_path) => {
            input_content = std::fs::read_to_string(file_path)?;
        }
        None => {
            io::stdin().read_to_string(&mut input_content)?;
        }
    }

    let decoded_message = decode_message(
        &input_content,
        args.interpret,
        args.highlight_keywords,
        args.frequency_analysis,
    );

    println!("{}", decoded_message);

    Ok(())
}
