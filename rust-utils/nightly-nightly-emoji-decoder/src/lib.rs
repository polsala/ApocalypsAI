use std::collections::HashMap;

pub fn decode_emoji(s: &str) -> Vec<(&'static str, &'static str)> {
    let map: HashMap<&str, &str> = HashMap::from([
        ("🚀", "rocket"),
        ("🌕", "full moon"),
        ("🔥", "fire"),
        ("💧", "droplet"),
        ("⚡", "high voltage"),
        ("❤️", "heart"),
        ("😂", "joy"),
        ("🤖", "robot"),
        ("🧩", "puzzle piece"),
        ("🌟", "star"),
    ]);
    s.chars()
        .filter_map(|c| {
            let emoji = c.to_string();
            map.get(emoji.as_str()).map(|desc| (emoji.as_str(), *desc))
        })
        .collect()
}
