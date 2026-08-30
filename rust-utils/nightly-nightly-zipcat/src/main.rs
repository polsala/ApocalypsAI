use clap::Parser;
use anyhow::Result;
use nightly_zipcat::list_zip;

#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Path to the zip archive
    zip_path: String,

    /// Number of bytes to preview from each file
    #[arg(short, long, default_value_t = 16)]
    preview: usize,

    /// Optional substring filter for entry names
    #[arg(short, long)]
    filter: Option<String>,
}

fn format_bytes(bytes: &[u8]) -> String {
    bytes.iter()
        .map(|b| format!("{:02x}", b))
        .collect::<Vec<_>>()
        .join(" ")
}

fn main() -> Result<()> {
    let args = Args::parse();

    let previews = list_zip(&args.zip_path, args.preview, args.filter.as_deref())?;

    for entry in previews {
        let hex = format_bytes(&entry.preview_bytes);
        println!("{}: {}", entry.name, hex);
    }

    Ok(())
}
