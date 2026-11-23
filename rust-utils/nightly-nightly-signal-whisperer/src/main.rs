use clap::Parser;
use std::collections::HashMap;
use std::io::{self, BufRead};
use regex::Regex;

#[derive(Parser, Debug)]
#[command(author, version, about = "Scans text-based signals for anomalous patterns, repeating sequences, and keywords.", long_about = None)]
struct Args {
    /// Path to the signal file. If not provided, reads from stdin.
    #[arg(short, long)]
    file: Option<String>,

    /// Comma-separated list of keywords to search for.
    #[arg(short, long, value_delimiter = ',')]
    keywords: Vec<String>,

    /// Minimum length for repeating sequences to be considered significant.
    #[arg(short, long, default_value_t = 3)]
    min_repeat_len: usize,

    /// Character frequency threshold (as a percentage) to flag as anomalous.
    #[arg(short, long, default_value_t = 10.0)]
    freq_threshold: f32,
}

fn main() -> io::Result<()> {
    let args = Args::parse();

    let reader: Box<dyn BufRead> = if let Some(file_path) = args.file {
        let file = std::fs::File::open(file_path)?;
        Box::new(io::BufReader::new(file))
    } else {
        Box::new(io::BufReader::new(io::stdin()))
    };

    let mut full_content = String::new();
    for line in reader.lines() {
        full_content.push_str(&line?);
        full_content.push('\n');
    }

    if full_content.trim().is_empty() {
        println!("Whisper: No signal detected. The void is silent.");
        return Ok(());
    }

    // 1. Keyword Detection
    for keyword in &args.keywords {
        let re = Regex::new(&format!("(?i){}", regex::escape(keyword))).unwrap();
        if re.is_match(&full_content) {
            println!("Whisper: A faint echo of a forgotten broadcast detected! Keyword '{}' found.", keyword);
        }
    }

    // 2. Repeating Sequence Detection
    if args.min_repeat_len > 0 {
        let mut sequence_counts: HashMap<String, usize> = HashMap::new();
        let max_scan_len = 50; // Max length of sequence to scan for repeats, to prevent excessive computation

        for len in args.min_repeat_len..=max_scan_len.min(full_content.len()) {
            for i in 0..=(full_content.len() - len) {
                let seq = &full_content[i..(i + len)];
                *sequence_counts.entry(seq.to_string()).or_insert(0) += 1;
            }
        }

        let mut significant_repeats: Vec<(String, usize)> = sequence_counts.into_iter()
            .filter(|(_, count)| *count > 1)
            .collect();

        // Sort by length (desc) and then count (desc) to prioritize longer, more frequent patterns
        significant_repeats.sort_by(|a, b| {
            b.0.len().cmp(&a.0.len()).then_with(|| b.1.cmp(&a.1))
        });

        // Filter out sequences that are strict substrings of other *reported* sequences
        let mut final_repeats = Vec::new();
        for (seq, count) in significant_repeats {
            let mut is_substring_of_longer_reported = false;
            for (f_seq, _) in &final_repeats {
                if f_seq.contains(&seq) && f_seq.len() > seq.len() {
                    is_substring_of_longer_reported = true;
                    break;
                }
            }
            if !is_substring_of_longer_reported {
                final_repeats.push((seq, count));
            }
        }

        for (seq, count) in final_repeats {
            println!("Whisper: A rhythmic pulse detected! Repeating sequence '{}' found {} times.", seq, count);
        }
    }

    // 3. Character Frequency Analysis
    let mut char_counts: HashMap<char, usize> = HashMap::new();
    let total_chars = full_content.chars().filter(|c| c.is_alphanumeric()).count();

    if total_chars > 0 {
        for c in full_content.chars() {
            if c.is_alphanumeric() {
                *char_counts.entry(c).or_insert(0) += 1;
            }
        }

        for (char, count) in char_counts {
            let frequency = (count as f32 / total_chars as f32) * 100.0;
            if frequency >= args.freq_threshold {
                println!("Whisper: An unusual resonance! Character '{}' appears with {}% frequency.", char, format!("{:.2}", frequency));
            }
        }
    }

    Ok(())
}
