pub fn encode(input: &str) -> String {
    let mut result = String::new();
    for c in input.chars() {
        let lower = c.to_ascii_lowercase();
        let emoji = match lower {
            'a' => "😀",
            'b' => "😁",
            'c' => "😂",
            'd' => "🤣",
            'e' => "😃",
            'f' => "😄",
            'g' => "😅",
            'h' => "😆",
            'i' => "😉",
            'j' => "😊",
            'k' => "😎",
            'l' => "😍",
            'm' => "😘",
            'n' => "🥰",
            'o' => "😗",
            'p' => "😙",
            'q' => "😚",
            'r' => "🙂",
            's' => "🤗",
            't' => "🤩",
            'u' => "🤔",
            'v' => "🤨",
            'w' => "😐",
            'x' => "😑",
            'y' => "😶",
            'z' => "🙄",
            ' ' => "⬜",
            _ => "❓",
        };
        result.push_str(emoji);
    }
    result
}

pub fn decode(input: &str) -> String {
    let mut result = String::new();
    let mut i = 0;
    let chars: Vec<char> = input.chars().collect();
    while i < chars.len() {
        let slice: String = chars[i..].iter().collect();
        let mut matched = false;
        macro_rules! check {
            ($ch:expr, $emoji:expr) => {
                if slice.starts_with($emoji) {
                    result.push($ch);
                    i += $emoji.chars().count();
                    matched = true;
                }
            };
        }
        check!('a', "😀");
        check!('b', "😁");
        check!('c', "😂");
        check!('d', "🤣");
        check!('e', "😃");
        check!('f', "😄");
        check!('g', "😅");
        check!('h', "😆");
        check!('i', "😉");
        check!('j', "😊");
        check!('k', "😎");
        check!('l', "😍");
        check!('m', "😘");
        check!('n', "🥰");
        check!('o', "😗");
        check!('p', "😙");
        check!('q', "😚");
        check!('r', "🙂");
        check!('s', "🤗");
        check!('t', "🤩");
        check!('u', "🤔");
        check!('v', "🤨");
        check!('w', "😐");
        check!('x', "😑");
        check!('y', "😶");
        check!('z', "🙄");
        check!(' ', "⬜");
        if !matched {
            // Unknown placeholder ("❓" during encode) becomes "?"
            result.push('?');
            i += 1;
        }
    }
    result
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn roundtrip() {
        let original = "Hello World";
        let encoded = encode(original);
        let decoded = decode(&encoded);
        assert_eq!(decoded, "hello world");
    }
}
