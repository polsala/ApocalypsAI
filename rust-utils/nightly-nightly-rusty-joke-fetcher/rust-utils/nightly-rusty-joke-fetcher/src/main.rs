use std::env;
use nightly_rusty_joke_fetcher::fetch_joke;

fn main() {
    let args: Vec<String> = env::args().collect();
    let url = if args.len() > 1 {
        &args[1]
    } else {
        "https://official-joke-api.appspot.com/random_joke"
    };
    match fetch_joke(url) {
        Ok(joke) => {
            println!("{} {}", joke.setup, joke.punchline);
        }
        Err(e) => {
            eprintln!("Error fetching joke: {}", e);
            std::process::exit(1);
        }
    }
}
