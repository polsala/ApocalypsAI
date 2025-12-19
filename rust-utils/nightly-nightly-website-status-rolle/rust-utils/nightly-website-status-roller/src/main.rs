use std::env;
use std::io::{self, BufRead};
use std::process;

fn main() {
    // Print whimsical header
    println!("🌐 Status Roller 🎲");

    // Collect URLs from args or stdin
    let args: Vec<String> = env::args().skip(1).collect();
    let urls = if !args.is_empty() {
        args
    } else {
        // Read from stdin
        let stdin = io::stdin();
        let reader = stdin.lock();
        reader
            .lines()
            .filter_map(|l| l.ok())
            .filter(|l| !l.trim().is_empty())
            .collect()
    };

    if urls.is_empty() {
        eprintln!("No URLs provided. Provide URLs as arguments or via stdin.");
        process::exit(1);
    }

    // Create blocking client
    let client = reqwest::blocking::Client::new();

    for url in urls {
        match client.get(&url).send() {
            Ok(resp) => {
                let status = resp.status();
                let emoji = match status.as_u16() {
                    200 => "✅",
                    404 => "❌",
                    500 => "💥",
                    _ => "⚠️",
                };
                println!("{} {} {}", url, status.as_u16(), emoji);
            }
            Err(_) => {
                println!("{} {} ❌", url, "ERR");
            }
        }
    }
}
