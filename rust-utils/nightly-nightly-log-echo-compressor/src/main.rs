use clap::Parser;
use regex::Regex;
use std::io::{self, BufReader, BufWriter, Write, Read};
use std::fs::File;

#[derive(Parser, Debug)]
#[clap(author, version, about = "Compresses repetitive log entries, reducing 'temporal echoes'.", long_about = None)]
struct Args {
    /// Path to the input log file.
    #[clap(name = "INPUT_FILE")]
    input_file: String,

    /// Path to the output file. If not specified, output will be printed to stdout.
    #[clap(short, long)]
    output: Option<String>,

    /// A regular expression pattern to identify and strip timestamps or other variable parts from log lines before comparison.
    /// The matched part will be ignored for de-duplication, but the original line (or the first occurrence's line) will be printed.
    #[clap(short, long)]
    regex: Option<String>,
}

fn main() -> io::Result<()> {
    let args = Args::parse();

    let input = File::open(&args.input_file)?;
    let reader = BufReader::new(input);

    let mut output_writer: Box<dyn Write> = match &args.output {
        Some(path) => Box::new(BufWriter::new(File::create(path)?)),
        None => Box::new(BufWriter::new(io::stdout())),
    };

    let regex_pattern = args.regex.map(|p| Regex::new(&p).expect("Invalid regex pattern"));

    let mut last_original_line: Option<String> = None;
    let mut last_stripped_line: Option<String> = None;
    let mut count: usize = 0;

    for line_result in reader.lines() {
        let original_line = line_result?;
        let current_stripped_line = match &regex_pattern {
            Some(re) => re.replace_all(&original_line, "").to_string(),
            None => original_line.clone(),
        };

        if let Some(ref ls_line) = last_stripped_line {
            if *ls_line == current_stripped_line {
                count += 1;
            } else {
                // New unique line found, write the previous one
                if let Some(ref lo_line) = last_original_line {
                    if count > 1 {
                        writeln!(output_writer, "{} (x{})", lo_line, count)?;
                    } else {
                        writeln!(output_writer, "{}", lo_line)?;
                    }
                }
                // Reset for the new line
                last_original_line = Some(original_line);
                last_stripped_line = Some(current_stripped_line);
                count = 1;
            }
        } else {
            // First line encountered
            last_original_line = Some(original_line);
            last_stripped_line = Some(current_stripped_line);
            count = 1;
        }
    }

    // Write the last accumulated line if any
    if let Some(ref lo_line) = last_original_line {
        if count > 1 {
            writeln!(output_writer, "{} (x{})", lo_line, count)?;
        } else {
            writeln!(output_writer, "{}", lo_line)?;
        }
    }

    output_writer.flush()?;

    Ok(())
}
