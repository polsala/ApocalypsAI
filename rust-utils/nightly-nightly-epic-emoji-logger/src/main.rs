use std::io::{self, BufRead, Write};

fn process_line(line: &str) -> String {
    let lower = line.to_lowercase();
    let emoji = if lower.contains("error") {
        "❌"
    } else if lower.contains("warning") {
        "⚠️"
    } else if lower.contains("info") {
        "ℹ️"
    } else if lower.contains("debug") {
        "🐛"
    } else {
        "📜"
    };
    format!("{} {}", emoji, line)
}

fn main() {
    let stdin = io::stdin();
    let stdout = io::stdout();
    let mut out = io::BufWriter::new(stdout.lock());

    for line in stdin.lock().lines() {
        match line {
            Ok(l) => {
                let processed = process_line(&l);
                writeln!(out, "{}", processed).expect("Failed to write");
            }
            Err(e) => {
                eprintln!("Error reading line: {}", e);
            }
        }
    }
}
