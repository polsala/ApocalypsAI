use sha2::{Sha256, Digest};
use hex;

/// Purifies the input text by removing empty lines, trimming whitespace,
/// and removing consecutive duplicate lines.
pub fn purify_text(input: &str) -> String {
    let mut purified_lines = Vec::new();
    let mut last_line_added: Option<String> = None;

    for line in input.lines() {
        let trimmed_line = line.trim();
        if !trimmed_line.is_empty() {
            // Only add if not a consecutive duplicate
            if let Some(ref last) = last_line_added {
                if last == trimmed_line {
                    continue;
                }
            }
            purified_lines.push(trimmed_line.to_string());
            last_line_added = Some(trimmed_line.to_string());
        }
    }
    purified_lines.join("\n")
}

/// Calculates the SHA256 hash of the given content.
pub fn calculate_signature(content: &str) -> String {
    let mut hasher = Sha256::new();
    hasher.update(content.as_bytes());
    hex::encode(hasher.finalize())
}
