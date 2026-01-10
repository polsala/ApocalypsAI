// nightly-issue-labeler

use std::env;
use std::fs;
use std::io::{self, Read};

fn suggest_labels(body: &str) -> Vec<&'static str> {
    let keywords = [
        ("bug", "bug"),
        ("feature", "enhancement"),
        ("documentation", "documentation"),
        ("question", "question"),
        ("performance", "performance"),
        ("security", "security"),
    ];
    let mut labels = Vec::new();
    let body_lower = body.to_lowercase();
    for (kw, label) in &keywords {
        if body_lower.contains(kw) {
            labels.push(*label);
        }
    }
    labels
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let content = if args.len() > 1 {
        // read file
        fs::read_to_string(&args[1]).expect("Failed to read file")
    } else {
        // read stdin
        let mut buffer = String::new();
        io::stdin().read_to_string(&mut buffer).expect("Failed to read stdin");
        buffer
    };
    let labels = suggest_labels(&content);
    if labels.is_empty() {
        println!("No labels found");
    } else {
        println!("{}", labels.join(", "));
    }
}
