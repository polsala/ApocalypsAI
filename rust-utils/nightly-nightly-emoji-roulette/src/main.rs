use std::env;
use std::io::{self, Read};

const EMOJIS: [&str; 10] = [
    "😀",
    "😃",
    "😄",
    "😁",
    "😆",
    "😅",
    "😂",
    "🤣",
    "😊",
    "😇",
];

fn pick_emoji(word: &str) -> &str {
    let first_char = word.chars().next().unwrap_or('a');
    let idx = match first_char.to_ascii_lowercase() {
        'a'..='z' => (first_char as u8 - b'a') as usize % EMOJIS.len(),
        _ => 0,
    };
    EMOJIS[idx]
}

fn wrap_word(word: &str) -> String {
    let emoji = pick_emoji(word);
    format!("{}{}{}", emoji, word, emoji)
}

fn process_input(input: &str) -> String {
    input
        .split_whitespace()
        .map(wrap_word)
        .collect::<Vec<_>>()
        .join(" ")
}

fn main() {
    let args: Vec<String> = env::args().skip(1).collect();
    let input = if !args.is_empty() {
        args.join(" ")
    } else {
        let mut buffer = String::new();
        io::stdin().read_to_string(&mut buffer).expect("Failed to read stdin");
        buffer.trim().to_string()
    };
    let output = process_input(&input);
    println!("{}", output);
}
