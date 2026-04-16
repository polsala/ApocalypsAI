use std::env;

fn color_block(num: u8) -> String {
    // Returns a string with the color number and a colored block.
    // Using ANSI 256‑color foreground.
    format!("\x1b[38;5;{}m{:>3}\x1b[0m", num, num)
}

fn print_grid() {
    for row in 0..16 {
        for col in 0..16 {
            let num = row * 16 + col;
            print!("{} ", color_block(num as u8));
        }
        println!();
    }
}

fn main() {
    let args: Vec<String> = env::args().skip(1).collect();
    if args.is_empty() {
        print_grid();
    } else {
        for arg in args {
            match arg.parse::<u8>() {
                Ok(num) => println!("{}", color_block(num)),
                Err(_) => eprintln!("Invalid color number: {}", arg),
            }
        }
    }
}
