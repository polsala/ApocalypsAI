pub fn generate_palette(start: u8, end: u8) -> String {
    let mut out = String::new();
    for code in start..=end {
        // Print the code using its foreground ANSI 256‑color value
        out.push_str(&format!("\x1b[38;5;{}m{:>3}\x1b[0m ", code, code));
        // Insert a newline every 16 colors for readability
        if (code - start + 1) % 16 == 0 {
            out.push('\n');
        }
    }
    out
}
