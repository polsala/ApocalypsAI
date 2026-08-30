use std::env;
use qrcode::QrCode;
use qrcode::render::unicode;

/// Encode `text` into a compact Unicode‑block QR code string.
///
/// The function never panics; it returns an empty string on error.
pub fn encode_to_ascii(text: &str) -> String {
    match QrCode::new(text) {
        Ok(code) => code
            .render::<unicode::Dense1x2>()
            .quiet_zone(false)
            .build(),
        Err(_) => String::new(),
    }
}

fn print_usage(program: &str) {
    eprintln!("Usage: {} <text>", program);
    eprintln!("Example: {} \"HELLO\"", program);
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        print_usage(&args[0]);
        std::process::exit(1);
    }
    let ascii = encode_to_ascii(&args[1]);
    if ascii.is_empty() {
        eprintln!("Failed to generate QR code for input.");
        std::process::exit(1);
    }
    println!("{}", ascii);
}

#[cfg(test)]
mod tests {
    use super::encode_to_ascii;

    #[test]
    fn encodes_hello_contains_blocks() {
        let out = encode_to_ascii("HELLO");
        // The output should contain at least one pair of block characters representing a dark module.
        assert!(out.contains("██"), "QR output does not contain expected block characters");
        // It should also contain newline characters separating rows.
        assert!(out.contains('\n'), "QR output should contain line breaks");
    }

    #[test]
    fn empty_input_returns_nonempty_qr() {
        let out = encode_to_ascii("");
        assert!(!out.is_empty(), "Even an empty string should produce a QR code");
    }
}
