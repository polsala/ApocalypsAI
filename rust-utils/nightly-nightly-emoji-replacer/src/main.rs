use std::collections::HashMap;
use std::env;

fn build_map() -> HashMap<&'static str, &'static str> {
    let mut m = HashMap::new();
    m.insert("happy", "😊");
    m.insert("sad", "😢");
    m.insert("love", "❤️");
    m.insert("heart", "❤️");
    m.insert("cool", "😎");
    m.insert("fire", "🔥");
    m
}

fn replace_emojis(input: &str, map: &HashMap<&str, &str>) -> String {
    input
        .split_whitespace()
        .map(|word| {
            let key = word.to_lowercase();
            if let Some(&emoji) = map.get(key.as_str()) {
                emoji
            } else {
                word
            }
        })
        .collect::<Vec<&str>>()
        .join(" ")
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: nightly-emoji-replacer <text>");
        std::process::exit(1);
    }
    let input = &args[1];
    let map = build_map();
    let output = replace_emojis(input, &map);
    println!("{}", output);
}
