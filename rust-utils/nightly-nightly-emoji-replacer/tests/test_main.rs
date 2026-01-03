use std::collections::HashMap;

fn build_map() -> HashMap<&'static str, &'static str> {
    let mut m = HashMap::new();
    m.insert("happy", "😊");
    m.insert("sad", "😢");
    m.insert("love", "❤️");
    m.insert("heart", "❤️");
    m.insert("cool", "😎");
    m.insert("fire", "🔥");
    m
}

fn replace_emojis(input: &str, map: &HashMap<&str, &str>) -> String {
    input
        .split_whitespace()
        .map(|word| {
            let key = word.to_lowercase();
            if let Some(&emoji) = map.get(key.as_str()) {
                emoji
            } else {
                word
            }
        })
        .collect::<Vec<&str>>()
        .join(" ")
}

#[test]
fn test_replace_emojis() {
    let map = build_map();
    let input = "I am happy and in love";
    let expected = "I am 😊 and in ❤️";
    assert_eq!(replace_emojis(input, &map), expected);

    let input2 = "This is cool fire";
    let expected2 = "This is 😎 🔥";
    assert_eq!(replace_emojis(input2, &map), expected2);
}
