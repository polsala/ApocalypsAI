pub fn generate_palette() -> String {
    let mut out = String::new();
    for i in 0..256 {
        // ANSI background color escape sequence
        out.push_str(&format!("\x1b[48;5;{}m{:>3}\x1b[0m ", i, i));
        if i % 16 == 15 {
            out.push('\n');
        }
    }
    out
}
