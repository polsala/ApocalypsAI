use std::env;
use emoji_mood_mapper::get_emoji;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        eprintln!("Usage: {} <mood>", args[0]);
        std::process::exit(1);
    }
    let mood = &args[1];
    let (emoji, description) = get_emoji(mood);
    println!("{} - {}", emoji, description);
}
