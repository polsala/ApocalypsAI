use std::collections::HashMap;

pub fn cipher(input: &str) -> String {
    let mapping: HashMap<char, char> = [
        ('a', '@'), ('b', '#'), ('c', '$'), ('d', '%'), ('e', '3'),
        ('f', '&'), ('g', '9'), ('h', 'h'), ('i', '!'), ('j', '*'),
        ('k', '('), ('l', '|'), ('m', 'm'), ('n', 'n'), ('o', '0'),
        ('p', 'p'), ('q', 'q'), ('r', 'r'), ('s', '5'), ('t', '7'),
        ('u', 'u'), ('v', 'v'), ('w', 'w'), ('x', 'x'), ('y', 'y'),
        ('z', '2')
    ].iter().cloned().collect();

    input
        .chars()
        .map(|c| {
            let lower = c.to_ascii_lowercase();
            if let Some(&sub) = mapping.get(&lower) {
                sub
            } else {
                c
            }
        })
        .collect()
}
