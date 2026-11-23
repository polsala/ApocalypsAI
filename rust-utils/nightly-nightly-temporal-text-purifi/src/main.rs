use clap::Parser;
use std::fs;
use std::io::{self, Write};
use nightly_temporal_text_purifier::{purify_text, calculate_signature};

#[derive(Parser, Debug)]
#[command(author, version, about = "Purifies text files by removing temporal noise and generates a unique temporal signature.", long_about = None)]
struct Args {
    /// Input file path
    #[arg(short, long)]
    input: String,

    /// Output file path (optional, defaults to stdout)
    #[arg(short, long)]
    output: Option<String>,

    /// Check the temporal signature against a provided hash
    #[arg(short, long)]
    check_signature: Option<String>,
}

fn main() -> io::Result<()> {
    let args = Args::parse();

    let input_content = fs::read_to_string(&args.input)?;

    let purified_content = purify_text(&input_content);
    let signature = calculate_signature(&purified_content);

    if let Some(output_path) = args.output {
        let mut output_file = fs::File::create(&output_path)?;
        output_file.write_all(purified_content.as_bytes())?;
        println!("Purified content written to: {}", output_path);
    } else {
        io::stdout().write_all(purified_content.as_bytes())?;
        io::stdout().write_all(b"\n")?; // Ensure a newline after content
    }

    println!("Temporal Signature: {}", signature);

    if let Some(expected_signature) = args.check_signature {
        if signature == expected_signature {
            println!("Signature check: SUCCESS! The file's temporal integrity is stable.");
            Ok(())
        } else {
            eprintln!("Signature check: FAILED! The file's temporal integrity has been compromised or altered.");
            Err(io::Error::new(io::ErrorKind::InvalidData, "Temporal signature mismatch"))
        }
    } else {
        Ok(())
    }
}
