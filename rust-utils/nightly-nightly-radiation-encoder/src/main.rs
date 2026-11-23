use std::env;
use std::process;

fn to_base36(val: u8) -> char {
    let v = val % 36;
    if v < 10 {
        (b'0' + v) as char
    } else {
        (b'a' + v - 10) as char
    }
}

fn from_base36(c: char) -> Result<u8, String> {
    match c {
        '0'..='9' => Ok(c as u8 - b'0'),
        'a'..='z' => Ok(c as u8 - b'a' + 10),
        _ => Err(format!("Invalid base36 character: {}", c)),
    }
}

fn checksum(data: &[u8]) -> u8 {
    data.iter().fold(0u8, |acc, &b| acc.wrapping_add(b)) % 36
}

pub fn encode(input: &str) -> String {
    let bytes = input.as_bytes();
    let mut out = String::new();
    for &b in bytes {
        let high = (b >> 4) & 0x0F;
        let low = b & 0x0F;
        out.push(to_base36(high));
        out.push(to_base36(low));
    }
    let cs = checksum(bytes);
    out.push(to_base36(cs));
    out
}

pub fn decode(encoded: &str) -> Result<String, String> {
    if encoded.len() < 3 || (encoded.len() - 1) % 2 != 0 {
        return Err("Encoded string has invalid length".to_string());
    }
    let (data_part, cs_char) = encoded.split_at(encoded.len() - 1);
    let mut bytes = Vec::new();
    let chars: Vec<char> = data_part.chars().collect();
    for pair in chars.chunks(2) {
        let high = from_base36(pair[0])?;
        let low = from_base36(pair[1])?;
        if high > 0x0F || low > 0x0F {
            return Err("Nibble out of range (must be 0‑15)".to_string());
        }
        bytes.push((high << 4) | low);
    }
    let expected_cs = checksum(&bytes);
    let provided_cs = from_base36(cs_char.chars().next().unwrap())?;
    if expected_cs != provided_cs {
        return Err("Checksum mismatch".to_string());
    }
    match String::from_utf8(bytes) {
        Ok(s) => Ok(s),
        Err(_) => Err("Decoded bytes are not valid UTF-8".to_string()),
    }
}

fn print_usage_and_exit() -> ! {
    eprintln!("Usage: radiation-encoder <encode|decode> <message>");
    process::exit(1);
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 3 {
        print_usage_and_exit();
    }
    let command = args[1].as_str();
    let payload = args[2].as_str();
    match command {
        "encode" => {
            let out = encode(payload);
            println!("{}", out);
        }
        "decode" => match decode(payload) {
            Ok(s) => println!("{}", s),
            Err(e) => {
                eprintln!("Error: {}", e);
                process::exit(1);
            }
        },
        _ => print_usage_and_exit(),
    }
}
