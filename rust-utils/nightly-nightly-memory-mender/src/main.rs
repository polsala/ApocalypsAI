use clap::Parser;
use std::fs;
use std::io::{self, Read, Write};
use std::path::PathBuf;

#[derive(Parser, Debug)]
#[clap(author, version, about = "A Rust CLI tool to detect and mend minor data corruptions in text files.", long_about = None)]
struct Args {
    /// Path to the input file to mend
    #[clap(short, long, value_parser)]
    input: PathBuf,

    /// Path to the output file. If not specified, the input file will be overwritten (a backup will be created).
    #[clap(short, long, value_parser)]
    output: Option<PathBuf>,

    /// Placeholder text to insert where corruption is detected
    #[clap(short, long, default_value = "[MENDED]")]
    placeholder: String,

    /// Perform a dry run: detect corruptions and report, but do not write changes.
    #[clap(short, long)]
    dry_run: bool,
}

/// Detects and replaces non-printable control characters or Unicode replacement characters with a placeholder.
/// Returns the mended string and the count of mended instances.
fn mend_content(content: &str, placeholder: &str) -> (String, usize) {
    let mut mended_content = String::new();
    let mut mended_count = 0;

    for c in content.chars() {
        // Check for non-printable ASCII control characters (excluding common whitespace like newline, carriage return, tab)
        // and the Unicode replacement character (U+FFFD) which indicates invalid UTF-8 sequences.
        if (c.is_control() && !c.is_whitespace()) || c == '\u{FFFD}' {
            mended_content.push_str(placeholder);
            mended_count += 1;
        } else {
            mended_content.push(c);
        }
    }
    (mended_content, mended_count)
}

fn main() -> io::Result<()> {
    let args = Args::parse();

    let input_path = &args.input;
    let output_path = args.output.as_ref().unwrap_or(input_path);

    if !input_path.exists() {
        eprintln!("Error: Input file not found at {:?}", input_path);
        return Err(io::Error::new(io::ErrorKind::NotFound, "Input file not found"));
    }

    let original_content = fs::read_to_string(input_path)?;

    let (mended_content, mended_count) = mend_content(&original_content, &args.placeholder);

    if mended_count == 0 {
        println!("No corruptions detected in {:?}. All clear!", input_path);
        return Ok(());
    }

    println!("Detected and mended {} instances of corruption.", mended_count);

    if args.dry_run {
        println!("Dry run complete. No changes written to disk.");
        println!("--- Mended Content Preview ---");
        let preview_len = std::cmp::min(mended_content.len(), 500);
        println!("{}", &mended_content[..preview_len]);
        if mended_content.len() > preview_len {
            println!("... (truncated)");
        }
        println!("----------------------------");
        return Ok(());
    }

    if input_path == output_path {
        let backup_path = input_path.with_extension("bak");
        println!("Creating backup of original file at {:?}", backup_path);
        fs::copy(input_path, &backup_path)?;
    }

    fs::write(output_path, mended_content)?;
    println!("Mending complete. Output written to {:?}", output_path);

    Ok(())
}
