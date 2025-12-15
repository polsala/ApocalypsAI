use rand::{seq::SliceRandom, SeedableRng, rngs::StdRng};
use std::env;

const TASKS: &[&str] = &[
    "Find water",
    "Build shelter",
    "Gather firewood",
    "Cook food",
    "Signal for help",
    "Collect rainwater",
    "Make firestarter",
    "Find edible plants",
    "Set up a trap",
    "Create a compass",
    "Identify safe rocks",
    "Make a rope",
    "Find a source of light",
    "Collect medicinal herbs",
    "Build a raft",
    "Find a way to purify water",
    "Create a shelter from debris",
    "Make a fishing net",
    "Find a way to signal a rescue",
    "Build a fire pit",
    "Collect firewood",
    "Make a shelter",
    "Find a way to get fresh air",
    "Create a signal fire",
    "Find a way to keep warm",
    "Make a shelter from natural materials",
    "Find a way to keep food fresh",
    "Create a shelter from wind",
    "Find a way to keep a fire going",
    "Make a shelter from snow",
    "Find a way to keep a fire burning",
    "Create a shelter from rain",
];

fn generate_card(seed: Option<u64>) -> Vec<Vec<String>> {
    let mut rng: StdRng = match seed {
        Some(s) => StdRng::seed_from_u64(s),
        None => StdRng::from_entropy(),
    };
    let mut tasks: Vec<&str> = TASKS.to_vec();
    tasks.shuffle(&mut rng);
    let selected: Vec<&str> = tasks.into_iter().take(25).collect();
    let mut card = Vec::new();
    for row in 0..5 {
        let mut row_vec = Vec::new();
        for col in 0..5 {
            row_vec.push(selected[row * 5 + col].to_string());
        }
        card.push(row_vec);
    }
    card
}

fn main() {
    let seed = env::var("BINGO_SEED")
        .ok()
        .and_then(|s| s.parse::<u64>().ok());
    let card = generate_card(seed);
    let headers = ["A", "B", "C", "D", "E"];
    for (i, row) in card.iter().enumerate() {
        let mut line = String::new();
        for (j, task) in row.iter().enumerate() {
            if j == 0 {
                line.push_str(&format!("{}: {}", headers[j], task));
            } else {
                line.push_str(&format!("\t{}: {}", headers[j], task));
            }
        }
        println!("{}", line);
    }
}
