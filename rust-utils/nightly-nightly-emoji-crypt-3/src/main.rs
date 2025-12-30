use std::collections::HashMap;
use std::env;

fn build_maps() -> (HashMap<char, &'static str>, HashMap<&'static str, char>) {
    let chars = [
        ('a', "😀"), ('b', "😁"), ('c', "😂"), ('d', "😃"), ('e', "😄"),
        ('f', "😅"), ('g', "😆"), ('h', "😉"), ('i', "😊"), ('j', "😋"),
        ('k', "😎"), ('l', "😍"), ('m', "😘"), ('n', "🥰"), ('o', "😗"),
        ('p', "😙"), ('q', "😚"), ('r', "🙂"), ('s', "🤗"), ('t', "🤩"),
        ('u', "🤔"), ('v', "🤨"), ('w', "😐"), ('x', "😑"), ('y', "😶"),
        ('z', "🙄"), (' ', "⬜"),
    ];
    let mut enc = HashMap::new();
    let mut dec = HashMap::new();
    for (c, e) in chars.iter() {
        enc.insert(*c, *e);
        dec.insert(*e, *c);
    }
    (enc, dec)
}

fn encode(input: &str, map: &HashMap<char, &str>) -> String {
    input
        .to_lowercase()
        .chars()
        .map(|c| map.get(&c).copied().unwrap_or_else(|| c.to_string().as_str()))
        .collect()
}

fn decode(input: &str, map: &HashMap<&str, char>) -> String {
    let mut result = String::new();
    let mut i = 0;
    let chars: Vec<char> = input.chars().collect();
    while i < chars.len() {
        // Try to match a two‑character emoji (most emojis are two UTF‑8 code units)
        // We'll attempt to take 2 chars, then 1 if not found.
        let mut matched = false;
        for len in (1..=2).rev() {
            if i + len <= chars.len() {
                let slice: String = chars[i..i + len].iter().collect();
                if let Some(&orig) = map.get(slice.as_str()) {
                    result.push(orig);
                    i += len;
                    matched = true;
                    break;
                }
            }
        }
        if !matched {
            // Pass through unknown characters
            result.push(chars[i]);
            i += 1;
        }
    }
    result
}

fn print_usage() {
    eprintln!("Usage: emoji-crypt <encode|decode> <text>");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 3 {
        print_usage();
        std::process::exit(1);
    }
    let command = args[1].as_str();
    let text = &args[2];
    let (enc_map, dec_map) = build_maps();
    match command {
        "encode" => {
            let out = encode(text, &enc_map);
            println!("{}", out);
        }
        "decode" => {
            let out = decode(text, &dec_map);
            println!("{}", out);
        }
        _ => {
            print_usage();
            std::process::exit(1);
        }
    }
}
