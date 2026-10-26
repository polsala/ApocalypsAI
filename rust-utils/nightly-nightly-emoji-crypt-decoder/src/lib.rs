/// Mapping from words to emojis. Only a small, whimsical set is provided.
const WORD_TO_EMOJI: &[(&str, &str)] = &[\
    ("apple", "🍎"),\
    ("rocket", "🚀"),\
    ("fire", "🔥"),\
    ("heart", "❤️"),\
    ("star", "⭐"),\
    ("coffee", "☕"),\
    ("book", "📚"),\
];\n\n/// Encode a space‑separated string of words into emojis.
/// Unknown words are left unchanged.
pub fn encode(input: &str) -> String {\n    input\
        .split_whitespace()\
        .map(|word| {\
            WORD_TO_EMOJI\
                .iter()\
                .find(|(w, _)| *w == word)\
                .map(|(_, e)| *e)\
                .unwrap_or(word)\
        })\
        .collect::<Vec<&str>>()\
        .join(" ")\n}\n\n/// Decode a space‑separated string of emojis back into words.
/// Unknown emojis are left unchanged.
pub fn decode(input: &str) -> String {\n    input\
        .split_whitespace()\
        .map(|emoji| {\
            WORD_TO_EMOJI\
                .iter()\
                .find(|(_, e)| *e == emoji)\
                .map(|(w, _)| *w)\
                .unwrap_or(emoji)\
        })\
        .collect::<Vec<&str>>()\
        .join(" ")\n}\n
