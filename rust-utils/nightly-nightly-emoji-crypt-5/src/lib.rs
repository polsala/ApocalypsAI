use std::collections::HashMap;

pub fn get_encode_map() -> HashMap<char, &'static str> {
    let mut m = HashMap::new();
    m.insert('a', "😀");
    m.insert('b', "😁");
    m.insert('c', "😂");
    m.insert('d', "😃");
    m.insert('e', "😄");
    m.insert('f', "😅");
    m.insert('g', "😆");
    m.insert('h', "😉");
    m.insert('i', "😊");
    m.insert('j', "😋");
    m.insert('k', "😎");
    m.insert('l', "😍");
    m.insert('m', "😘");
    m.insert('n', "🥰");
    m.insert('o', "😗");
    m.insert('p', "😙");
    m.insert('q', "😚");
    m.insert('r', "☺️");
    m.insert('s', "🤗");
    m.insert('t', "🤩");
    m.insert('u', "🤔");
    m.insert('v', "🤨");
    m.insert('w', "😐");
    m.insert('x', "😑");
    m.insert('y', "😶");
    m.insert('z', "🙄");
    m.insert(' ', "🟦");
    m
}

pub fn get_decode_map() -> HashMap<&'static str, char> {
    let enc = get_encode_map();
    let mut dec = HashMap::new();
    for (k, v) in enc {
        dec.insert(v, k);
    }
    dec
}

pub fn encode(input: &str) -> String {
    let map = get_encode_map();
    let mut out = String::new();
    for ch in input.chars() {
        if let Some(&emoji) = map.get(&ch) {
            out.push_str(emoji);
        } else {
            out.push(ch);
        }
    }
    out
}

pub fn decode(input: &str) -> String {
    let map = get_decode_map();
    let mut out = String::new();
    let mut i = 0;
    let chars: Vec<char> = input.chars().collect();
    while i < chars.len() {
        // Try to match two‑character emojis (e.g., "☺️")
        let mut matched = false;
        // Look ahead up to 2 chars (most emojis are 1 char, but "☺️" is 2)
        for len in (1..=2).rev() {
            if i + len <= chars.len() {
                let slice: String = chars[i..i + len].iter().collect();
                if let Some(&orig) = map.get(slice.as_str()) {
                    out.push(orig);
                    i += len;
                    matched = true;
                    break;
                }
            }
        }
        if !matched {
            out.push(chars[i]);
            i += 1;
        }
    }
    out
}
