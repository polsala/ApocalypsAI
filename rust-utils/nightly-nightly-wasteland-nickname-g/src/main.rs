use std::io::{self, Read};
use wasteland_nickname::generate_nickname;

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let name = if args.len() > 1 {
        args[1].clone()
    } else {
        // Read from stdin if no argument supplied
        let mut buffer = String::new();
        io::stdin().read_to_string(&mut buffer).expect("Failed to read stdin");
        buffer.trim().to_string()
    };

    if name.is_empty() {
        eprintln!("Please provide a name via argument or stdin");
        std::process::exit(1);
    }

    let nickname = generate_nickname(&name);
    println!("{}", nickname);
}
