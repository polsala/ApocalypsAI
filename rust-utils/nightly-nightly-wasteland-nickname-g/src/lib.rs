pub fn checksum(name: &str) -> u64 {
    name.bytes().map(|b| b as u64).sum()
}

pub fn generate_nickname(name: &str) -> String {
    const ADJECTIVES: [&str; 10] = [
        "Dusty", "Radiant", "Grim", "Wasteland", "Rusty",
        "Silent", "Blazing", "Cinder", "Ashen", "Gritty",
    ];
    const TITLES: [&str; 7] = [
        "the Scavenger", "the Wanderer", "the Survivor", "the Nomad",
        "the Raider", "the Keeper", "the Whisperer",
    ];
    let sum = checksum(name);
    let adj = ADJECTIVES[(sum as usize) % ADJECTIVES.len()];
    let title = TITLES[((sum / ADJECTIVES.len() as u64) as usize) % TITLES.len()];
    format!("{} {} {}", adj, name, title)
}
