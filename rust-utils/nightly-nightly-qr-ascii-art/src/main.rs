use std::env;
use qrcode::QrCode;
use qrcode::render::unicode;

fn main() {
    let args: Vec<String> = env::args().collect();
    let input = if args.len() > 1 {
        &args[1]
    } else {
        eprintln!("Usage: {} <text>", args[0]);
        std::process::exit(1);
    };
    match generate_qr_ascii(input) {
        Ok(s) => println!("{}", s),
        Err(e) => {
            eprintln!("Error generating QR: {}", e);
            std::process::exit(1);
        }
    }
}

fn generate_qr_ascii(data: &str) -> Result<String, Box<dyn std::error::Error>> {
    let code = QrCode::new(data.as_bytes())?;
    let string = code.render::<unicode::Dense1x2>()
        .quiet_zone(false)
        .build();
    Ok(string)
}
