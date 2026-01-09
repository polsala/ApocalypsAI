use std::collections::HashMap;

pub fn decode_message(
    input: &str,
    interpret: bool,
    highlight_keywords: bool,
    frequency_analysis: bool,
) -> String {
    let mut decoded = input.to_string();

    // 1. Noise removal
    decoded = decoded
        .replace("[STATIC]", "")
        .replace("_VOID_", "")
        .replace("///", "")
        .replace("---", "")
        .replace("...", "")
        .replace("~", "");

    // 2. Simple character interpretation (whimsical substitution)
    if interpret {
        let mut interpreted_chars = String::new();
        for c in decoded.chars() {
            let interpreted_c = match c {
                'X' => 'E',
                'Z' => 'S',
                'Q' => 'A',
                'J' => 'I',
                'K' => 'C',
                'W' => 'R',
                'V' => 'U',
                'Y' => 'O',
                'P' => 'L',
                'F' => 'T',
                _ => c,
            };
            interpreted_chars.push(interpreted_c);
        }
        decoded = interpreted_chars;
    }

    // 3. Keyword highlighting
    if highlight_keywords {
        let keywords = vec!["WATER", "FOOD", "SHELTER", "DANGER", "SUPPLIES", "SAFE", "HELP"];
        let mut current_text = decoded; // Start with the current decoded text

        for keyword in keywords {
            let lower_keyword = keyword.to_lowercase();
            let mut new_text = String::new();
            let mut last_end = 0;

            // Iterate over all matches of the lowercase keyword in the lowercase version of the current text
            for (start, _) in current_text.to_lowercase().match_indices(&lower_keyword) {
                let end = start + lower_keyword.len();
                // Append the part before the match
                new_text.push_str(&current_text[last_end..start]);
                // Append the highlighted part (preserving original casing)
                new_text.push_str(&format!("[!{}]", &current_text[start..end]));
                last_end = end;
            }
            // Append any remaining part after the last match
            new_text.push_str(&current_text[last_end..]);
            current_text = new_text; // Update current_text for the next keyword
        }
        decoded = current_text; // Assign the final result back to decoded
    }

    // 4. Frequency analysis (appended to the output)
    if frequency_analysis {
        let mut freq_map: HashMap<char, usize> = HashMap::new();
        for c in decoded.chars().filter(|c| c.is_alphabetic()) {
            *freq_map.entry(c.to_ascii_uppercase()).or_insert(0) += 1;
        }

        let mut sorted_freq: Vec<(&char, &usize)> = freq_map.iter().collect();
        sorted_freq.sort_by(|a, b| b.1.cmp(a.1));

        let mut freq_output = "\n--- Frequency Analysis ---\n".to_string();
        for (c, count) in sorted_freq {
            freq_output.push_str(&format!("{}: {}\n", c, count));
        }
        decoded.push_str(&freq_output);
    }

    decoded.trim().to_string()
}
