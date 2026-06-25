use clap::Parser;
use qrcodegen::{QrCode, QrCodeEcc};

/// Simple CLI to render a QR‑code as ASCII art.
#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// The text to encode into a QR‑code.
    #[arg(value_name = "TEXT")]
    text: String,
}

fn generate_qr_ascii(text: &str) -> String {
    // Encode the text with low error correction (sufficient for terminal display).
    let qr = QrCode::encode_text(text, QrCodeEcc::Low).expect("Failed to encode QR");
    let size = qr.size();
    let mut lines = Vec::with_capacity(size);
    for y in 0..size {
        let mut line = String::with_capacity(size * 2);
        for x in 0..size {
            if qr.get_module(x, y) {
                line.push_str("██"); // black module
            } else {
                line.push_str("  "); // white module
            }
        }
        lines.push(line);
    }
    lines.join("\n")
}

fn main() {
    let args = Args::parse();
    let ascii_qr = generate_qr_ascii(&args.text);
    println!("{}", ascii_qr);
}

#[cfg(test)]
mod tests {
    use super::generate_qr_ascii;

    #[test]
    fn same_input_produces_same_output() {
        let a = generate_qr_ascii("https://example.com");
        let b = generate_qr_ascii("https://example.com");
        assert_eq!(a, b);
    }

    #[test]
    fn different_inputs_produce_different_outputs() {
        let a = generate_qr_ascii("foo");
        let b = generate_qr_ascii("bar");
        assert_ne!(a, b);
    }

    #[test]
    fn output_is_non_empty_and_has_expected_chars() {
        let out = generate_qr_ascii("test");
        assert!(!out.is_empty(), "Output should not be empty");
        // Only spaces and block characters are allowed.
        for ch in out.chars() {
            assert!(ch == ' ' || ch == '\u{2588}' || ch == '\n', "Unexpected character in output");
        }
    }
}
