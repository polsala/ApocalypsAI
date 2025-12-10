use std::collections::HashMap;

pub fn decode(emojis: &str) -> Vec<String> {
    let mut map: HashMap<&str, Vec<&str>> = HashMap::new();
    map.insert("🌞", vec!["sun"]);
    map.insert("🌧️", vec!["rain"]);
    map.insert("🍎", vec!["apple"]);
    map.insert("🐱", vec!["cat", "kitten"]);
    map.insert("🚀", vec!["rocket", "launch"]);

    // Split the input by whitespace to get individual emoji tokens
    let tokens: Vec<&str> = emojis.split_whitespace().collect();

    // Start with a single empty combination
    let mut results: Vec<Vec<&str>> = vec![vec![]];

    for token in tokens {
        // Look up possible words for the token; if unknown, keep the token as‑is
        let words = match map.get(token) {
            Some(w) => w.clone(),
            None => vec![token],
        };
        let mut new_results = Vec::new();
        for prefix in &results {
            for w in &words {
                let mut new = prefix.clone();
                new.push(*w);
                new_results.push(new);
            }
        }
        results = new_results;
    }

    // Join each word list into a single phrase string
    results
        .into_iter()
        .map(|words| words.join(" "))
        .collect()
}
