use clap::Parser;
use qrcode::QrCode;
use qrcode::render::unicode;

/// Simple CLI to render a string as an ASCII QR code.
#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// The text to encode into a QR code
    #[arg(value_name = "TEXT")]
    text: String,
}

fn generate_qr_ascii(input: &str) -> String {
    // Create the QR code with default error correction (Low)
    let code = QrCode::new(input.as_bytes()).expect("Failed to create QR code");
    // Render using Unicode block characters for better terminal appearance.
    // The `unicode::Dense1x2` renderer maps two vertical pixels to one character.
    let image = code.render::<unicode::Dense1x2>().quiet_zone(false).build();
    image
}

fn main() {
    let args = Args::parse();
    let ascii_qr = generate_qr_ascii(&args.text);
    println!("{}", ascii_qr);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_qr_output_is_non_empty() {
        let out = generate_qr_ascii("test");
        assert!(!out.is_empty(), "QR output should not be empty");
    }

    #[test]
    fn test_qr_contains_block_characters() {
        let out = generate_qr_ascii("hello");
        // The dense Unicode renderer uses characters like '█' and '▇'.
        // Ensure at least one of them appears.
        let has_block = out.chars().any(|c| c == '█' || c == '▇' || c == '▆' || c == '▅' || c == '▄' || c == '▃' || c == '▂' || c == '▁');
        assert!(has_block, "QR output should contain block characters");
    }
}
