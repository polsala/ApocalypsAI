use std::env;
use std::io::{self, Write};

fn generate_palette(start: u8, end: u8) -> String {
    let mut out = String::new();
    for code in start..=end {
        // ANSI escape for foreground 256‑color
        out.push_str(&format!("\x1b[38;5;{}m█\x1b[0m {}\n", code, code));
    }
    out
}

fn parse_arg(arg: Option<String>) -> Result<Option<u8>, String> {
    match arg {
        Some(s) => s.parse::<u8>().map(Some).map_err(|e| format!("Invalid number '{}': {}", s, e)),
        None => Ok(None),
    }
}

fn main() {
    let args: Vec<String> = env::args().skip(1).collect();
    let start = parse_arg(args.get(0).cloned()).unwrap_or(Some(0)).unwrap_or(0);
    let end = parse_arg(args.get(1).cloned()).unwrap_or(Some(255)).unwrap_or(255);
    let start = start.min(255);
    let end = end.min(255);
    let (s, e) = if start <= end { (start, end) } else { (end, start) };
    let output = generate_palette(s, e);
    let _ = io::stdout().write_all(output.as_bytes());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_generate_single() {
        let out = generate_palette(0, 0);
        assert!(out.contains("\x1b[38;5;0m█\x1b[0m 0"));
    }

    #[test]
    fn test_range_order() {
        let out = generate_palette(5, 7);
        let lines: Vec<&str> = out.trim().split('\n').collect();
        assert_eq!(lines.len(), 3);
        assert!(lines[0].contains("5"));
        assert!(lines[2].contains("7"));
    }
}
