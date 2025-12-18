use std::io::{self, Read};

fn emoji_to_letter(c: char) -> Option<char> {
    match c {
        '🐱' => Some('a'),
        '🐶' => Some('b'),
        '🐭' => Some('c'),
        '🐹' => Some('d'),
        '🐰' => Some('e'),
        '🦊' => Some('f'),
        '🐻' => Some('g'),
        '🐼' => Some('h'),
        '🐨' => Some('i'),
        '🐯' => Some('j'),
        _ => None,
    }
}

/// Decode a string of emojis into a plain‑text message.
/// Unknown emojis are ignored.
fn decode(input: &str) -> String {
    input.chars().filter_map(emoji_to_letter).collect()
}

fn main() {
    // Prefer a command‑line argument; fall back to STDIN.
    let arg = std::env::args().nth(1);
    let input = match arg {
        Some(text) => text,
        None => {
            // Read entire STDIN.
            let mut buffer = String::new();
            io::stdin().read_to_string(&mut buffer).expect("Failed to read stdin");
            buffer
        }
    };
    let output = decode(&input.trim());
    println!("{}", output);
}
