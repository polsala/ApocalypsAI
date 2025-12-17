use std::io::{self, Write};

/// Simple ASCII art banner generator
/// Creates a decorative border around the text
pub fn display_ascii_art(text: &str) {
    let width = text.len() + 4;
    let border = "*".repeat(width);
    
    println!("{}
* {} *
{}", border, text, border);
    
    // Add a whimsical footer
    println!("\n   🎭 *Whispers of the cryptic arts...* 🎭");
    println!("   📜 Your message is now suitably mysterious! 📜\n");
}

/// Alternative ASCII art style with boxes
pub fn display_ascii_art_boxed(text: &str) {
    let lines: Vec<&str> = text.lines().collect();
    let max_width = lines.iter().map(|line| line.len()).max().unwrap_or(0) + 4;
    let border = "+".repeat(max_width);
    
    println!("{}");
    for line in lines {
        println!("| {: <width$} |", line, width = max_width - 4);
    }
    println!("{}");
    
    // Add a whimsical footer
    println!("\n   🔮 *The oracle has spoken...* 🔮");
    println!("   🛡️  Your secrets are now in ASCII form! 🛡️\n");
}

/// Display text as a scroll
pub fn display_ascii_art_scroll(text: &str) {
    println!("\n📜 ~~~ Ancient Scroll Unfurled ~~~ 📜\n");
    println!("{}");
    println!("\n📜 ~~~ End of Scroll ~~~ 📜\n");
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::io::Write;

    #[test]
    fn test_display_ascii_art() {
        // This test just ensures the function doesn't panic
        // In a real scenario, you might capture stdout to verify output
        let result = std::panic::catch_unwind(|| {
            display_ascii_art("TEST");
        });
        assert!(result.is_ok());
    }

    #[test]
    fn test_display_ascii_art_boxed() {
        let result = std::panic::catch_unwind(|| {
            display_ascii_art_boxed("TEST");
        });
        assert!(result.is_ok());
    }

    #[test]
    fn test_display_ascii_art_scroll() {
        let result = std::panic::catch_unwind(|| {
            display_ascii_art_scroll("TEST");
        });
        assert!(result.is_ok());
    }
}
