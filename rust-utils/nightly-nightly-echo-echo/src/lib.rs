pub fn echo_original(text: &str) -> String {
    format!("ECHO: {}", text)
}

pub fn echo_reverse(text: &str) -> String {
    let rev: String = text.chars().rev().collect();
    format!("ECHO: {}", rev)
}

pub fn echo_double(text: &str) -> String {
    let doubled: String = text.chars().flat_map(|c| std::iter::repeat(c).take(2)).collect();
    format!("ECHO: {}", doubled)
}
