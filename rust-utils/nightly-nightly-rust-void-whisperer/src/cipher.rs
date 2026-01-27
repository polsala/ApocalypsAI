const SHIFT: u8 = 5;

pub fn encode(input: &str) -> String {
    input.chars().map(|c| {
        if c.is_ascii_alphabetic() {
            let base = if c.is_ascii_lowercase() { b'a' } else { b'A' };
            let offset = (c as u8 - base + SHIFT) % 26;
            (base + offset) as char
        } else {
            c
        }
    }).collect()
}

pub fn decode(input: &str) -> String {
    input.chars().map(|c| {
        if c.is_ascii_alphabetic() {
            let base = if c.is_ascii_lowercase() { b'a' } else { b'A' };
            let offset = (c as u8 - base + 26 - SHIFT) % 26;
            (base + offset) as char
        } else {
            c
        }
    }).collect()
}
