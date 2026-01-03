use std::env;

const WORD_LIST: &[&str] = &[
    "apple", "banana", "cherry", "date", "elderberry",
    "fig", "grape", "honeydew", "kiwi", "lemon",
];

pub struct PassphraseOptions {
    pub words: usize,
    pub include_numbers: bool,
    pub include_symbols: bool,
}

pub fn generate_passphrase(opts: &PassphraseOptions) -> String {
    let seed = env::var("PASSGEN_SEED")
        .ok()
        .and_then(|s| s.parse::<u32>().ok())
        .unwrap_or_else(|| {
            let now = std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .unwrap()
                .as_secs();
            now as u32
        });

    let mut state = seed;
    let mut words = Vec::new();
    for _ in 0..opts.words {
        state = state.wrapping_mul(1664525).wrapping_add(1013904223);
        let idx = (state % WORD_LIST.len() as u32) as usize;
        words.push(WORD_LIST[idx].to_string());
    }

    let mut pass = words.join("-");

    if opts.include_numbers {
        state = state.wrapping_mul(1664525).wrapping_add(1013904223);
        let num = (state % 1000) as u32;
        pass.push_str(&format!("-{:03}", num));
    }

    if opts.include_symbols {
        let symbols = "!@#$%^&*";
        state = state.wrapping_mul(1664525).wrapping_add(1013904223);
        let idx = (state % symbols.len() as u32) as usize;
        pass.push(symbols.chars().nth(idx).unwrap());
    }

    pass
}
