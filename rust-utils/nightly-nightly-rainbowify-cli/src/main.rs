use std::io::{self, Read};

mod lib;

fn main() {
    // Collect arguments after program name
    let args: Vec<String> = std::env::args().skip(1).collect();
    let input = if !args.is_empty() {
        args.join(" ")
    } else {
        // Read from stdin
        let mut buffer = String::new();
        io::stdin().read_to_string(&mut buffer).expect("Failed to read stdin");
        buffer.trim_end().to_string()
    };
    let output = lib::rainbow(&input);
    println!("{}", output);
}
