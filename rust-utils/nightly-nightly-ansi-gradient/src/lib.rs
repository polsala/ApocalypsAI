pub const COLORS: [&str; 7] = [
    "\x1b[31m", // red
    "\x1b[33m", // orange (approximated with yellow)
    "\x1b[33m", // yellow
    "\x1b[32m", // green
    "\x1b[34m", // blue
    "\x1b[35m", // indigo (magenta)
    "\x1b[35m", // violet (magenta)
];

/// Returns the input `text` wrapped in a repeating ANSI rainbow gradient.
///
/// The function does **not** print anything; it only returns the colored string.
pub fn gradient(text: &str) -> String {
    let mut result = String::new();
    for (i, ch) in text.chars().enumerate() {
        let color = COLORS[i % COLORS.len()];
        result.push_str(color);
        result.push(ch);
    }
    // Reset colors at the end so subsequent terminal output is unaffected.
    result.push_str("\x1b[0m");
    result
}
