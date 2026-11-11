mod cli;
mod scrubber;

use cli::Cli;
use scrubber::Scrubber;
use clap::Parser;
use std::process;

fn main() {
    let cli = Cli::parse();

    if let Err(e) = run(cli) {
        eprintln!("\nError: {}", e);
        process::exit(1);
    }
}

fn run(cli: Cli) -> Result<(), String> {
    let scrubber = Scrubber::new(
        cli.path,
        cli.duration,
        cli.exclude,
        cli.dry_run,
        cli.force,
        cli.verbose,
    )?;

    println!("\nScanning for temporal echoes in '{}'...", scrubber.path().display());

    let decayed_files = scrubber.scan_for_decayed_files()?;

    if decayed_files.is_empty() {
        println!("No files found succumbing to digital entropy within the specified duration.");
        return Ok(());
    }

    println!("\nFound {} files fading into the void:", decayed_files.len());
    for file in &decayed_files {
        println!("  - {}", file.display());
    }

    if scrubber.dry_run() {
        println!("\n(Dry run complete. No files were actually scrubbed.)");
    } else {
        println!("\nInitiating temporal cleansing...");
        let scrubbed_count = scrubber.perform_scrub(decayed_files)?;
        println!("\nThe digital dust has settled. {} files scrubbed.", scrubbed_count);
    }

    Ok(())
}
