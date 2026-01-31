use std::fmt::Write;

mod lib;

fn main() {
    // Print a 16×16 grid (indices 0‑255)
    for row in 0..16 {
        let mut line = String::new();
        for col in 0..16 {
            let idx = row * 16 + col;
            let (r, g, b) = lib::rgb_from_256(idx as u8);
            let hex = format!("#{:02x}{:02x}{:02x}", r, g, b);
            // ANSI true‑color escape for a solid block
            let block = format!("\x1b[38;2;{r};{g};{b}m█\x1b[0m");
            write!(&mut line, "{:>3} {} {} ", idx, hex, block).unwrap();
        }
        println!("{}", line);
    }
}
