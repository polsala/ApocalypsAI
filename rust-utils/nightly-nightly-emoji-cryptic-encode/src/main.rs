use std::env;
use base64::{engine::general_purpose, Engine as _};

const B64_ALPHABET: &str = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

const EMOJI_TABLE: [&str; 64] = [
    "😀", "😁", "😂", "😃", "😄", "😅", "😆", "😉",
    "😊", "😋", "😎", "😍", "😘", "🥰", "😗", "😙",
    "😚", "☺️", "🤗", "🤔", "🤭", "🤫", "🤥", "😐",
    "😑", "😶", "🙄", "😏", "😣", "😥", "😮", "🤐",
    "😯", "😪", "😫", "🥱", "😴", "🤤", "😛", "😜",
    "😝", "🤪", "🤨", "🧐", "🤓", "🥳", "🤠", "😇",
    "🥺", "🤢", "🤮", "🤧", "😷", "🤒", "🤕", "🤑",
    "😈", "👿", "👹", "👺", "🤡", "💩", "👻", "💀",
];

const PADDING_EMOJI: &str = "🟰";

fn encode_to_emoji(input: &str) -> String {
    let b64 = general_purpose::STANDARD.encode(input);
    b64.chars()
        .map(|c| {
            if c == '=' {
                PADDING_EMOJI.to_string()
            } else {
                let idx = B64_ALPHABET.find(c).expect("Invalid Base64 char");
                EMOJI_TABLE[idx].to_string()
            }
        })
        .collect()
}

fn decode_from_emoji(emoji_str: &str) -> Result<String, String> {
    // Split the emoji string into Unicode grapheme clusters (each emoji is a single cluster)
    // For simplicity we treat each emoji as a fixed-width char because all entries are single codepoints or simple sequences.
    // We'll iterate over the string by char boundaries, matching known emojis.
    let mut b64 = String::new();
    let mut i = 0;
    let chars: Vec<char> = emoji_str.chars().collect();
    while i < chars.len() {
        // Try to match a two‑char emoji like "☺️" or "🟰"
        let mut matched = false;
        for len in (1..=2).rev() {
            if i + len > chars.len() { continue; }
            let slice: String = chars[i..i+len].iter().collect();
            if slice == PADDING_EMOJI {
                b64.push('=');
                i += len;
                matched = true;
                break;
            }
            if let Some(idx) = EMOJI_TABLE.iter().position(|&e| e == slice) {
                let b64_char = B64_ALPHABET.chars().nth(idx).unwrap();
                b64.push(b64_char);
                i += len;
                matched = true;
                break;
            }
        }
        if !matched {
            return Err(format!("Unrecognized emoji at position {}", i));
        }
    }
    general_purpose::STANDARD.decode(&b64)
        .map_err(|e| format!("Base64 decode error: {}", e))
        .and_then(|bytes| String::from_utf8(bytes).map_err(|e| format!("UTF‑8 error: {}", e)))
}

fn print_usage() {
    eprintln!("Usage: <program> <encode|decode> <string>");
    eprintln!("Example: encode \"Hi\" => 🤗😆😴🟰");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 3 {
        print_usage();
        std::process::exit(1);
    }
    let command = args[1].as_str();
    let payload = &args[2];
    match command {
        "encode" => {
            let out = encode_to_emoji(payload);
            println!("{}", out);
        }
        "decode" => {
            match decode_from_emoji(payload) {
                Ok(text) => println!("{}", text),
                Err(e) => {
                    eprintln!("Error: {}", e);
                    std::process::exit(1);
                }
            }
        }
        _ => {
            eprintln!("Invalid command: {}", command);
            print_usage();
            std::process::exit(1);
        }
    }
}
