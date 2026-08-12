/// Generate a mutant name using the given seed.
/// Returns a string like "Feral Reaper".
pub fn generate_name(seed: u64) -> String {
    const ADJECTIVES: [&str; 10] = [
        "Gloomy",
        "Radiant",
        "Feral",
        "Mutant",
        "Savage",
        "Cursed",
        "Wretched",
        "Vicious",
        "Silent",
        "Grim",
    ];
    const NOUNS: [&str; 10] = [
        "Scavenger",
        "Wanderer",
        "Beast",
        "Ghoul",
        "Reaper",
        "Stalker",
        "Marauder",
        "Ravager",
        "Nomad",
        "Harbinger",
    ];

    let adj_index = (seed as usize) % ADJECTIVES.len();
    let noun_index = ((seed / ADJECTIVES.len() as u64) as usize) % NOUNS.len();
    format!("{} {}", ADJECTIVES[adj_index], NOUNS[noun_index])
}
