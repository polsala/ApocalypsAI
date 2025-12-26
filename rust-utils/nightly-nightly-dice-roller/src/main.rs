use std::env;
use nightly_dice_roller::{parse_notation, roll_dice};

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        eprintln!("Usage: {} <dice_notation>", args[0]);
        std::process::exit(1);
    }
    let notation = &args[1];
    match parse_notation(notation) {
        Some((n, m, offset)) => {
            let mut rng = rand::thread_rng();
            let roll = roll_dice(n, m, &mut rng);
            let result = roll as i32 + offset;
            println!("Result: {}", result);
        }
        None => {
            eprintln!("Invalid dice notation. Example: 2d6+3");
            std::process::exit(1);
        }
    }
}
