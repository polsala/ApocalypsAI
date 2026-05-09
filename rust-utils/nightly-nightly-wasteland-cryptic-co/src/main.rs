use std::env;
use std::time::{SystemTime, UNIX_EPOCH};
use std::hash::{Hash, Hasher};
use std::collections::hash_map::DefaultHasher;

static ADJECTIVES: &[&str] = &[
    "rusted",
    "howling",
    "shimmering",
    "bleak",
    "crimson",
    "ashen",
    "whispering",
    "cursed",
    "lonely",
    "forgotten",
];

static NOUNS: &[&str] = &[
    "dunes",
    "ruins",
    "wasteland",
    "barricade",
    "silo",
    "cavern",
    "horizon",
    "mirage",
    "storm",
    "silence",
];

static VERBS: &[&str] = &[
    "awaits",
    "beckons",
    "lurks",
    "whispers",
    "howls",
    "shifts",
    "stirs",
    "echoes",
    "flares",
    "glimmers",
];

fn hash_seed(direction: &str, seed: u64) -> u64 {
    let mut hasher = DefaultHasher::new();
    direction.to_ascii_uppercase().hash(&mut hasher);
    seed.hash(&mut hasher);
    hasher.finish()
}

fn generate_hint(direction: &str, seed: u64) -> String {
    let hash = hash_seed(direction, seed);
    let adj = ADJECTIVES[(hash as usize) % ADJECTIVES.len()];
    let noun = NOUNS[((hash >> 8) as usize) % NOUNS.len()];
    let verb = VERBS[((hash >> 16) as usize) % VERBS.len()];
    format!("Follow the {} compass toward the {}, where {} {}.",
        adj, noun, noun, verb)
}

fn parse_seed(arg: Option<String>) -> u64 {
    match arg {
        Some(s) => s.parse::<u64>().unwrap_or_else(|_| {
            eprintln!("Invalid seed '{}', falling back to timestamp.", s);
            current_timestamp()
        }),
        None => current_timestamp(),
    }
}

fn current_timestamp() -> u64 {
    SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_secs()
}

fn print_usage() {
    eprintln!("Usage: nightly-wasteland-cryptic-compass <DIRECTION> [SEED]");
    eprintln!("  DIRECTION: N, E, S, or W (case‑insensitive)");
    eprintln!("  SEED: optional unsigned integer for deterministic output");
}

fn main() {
    let mut args = env::args().skip(1); // skip program name
    let direction = match args.next() {
        Some(d) => d,
        None => {
            print_usage();
            std::process::exit(1);
        }
    };
    let seed_arg = args.next();
    let seed = parse_seed(seed_arg);

    if !["N", "E", "S", "W"].contains(&direction.to_ascii_uppercase().as_str()) {
        eprintln!("Invalid direction '{}'. Must be N, E, S, or W.", direction);
        print_usage();
        std::process::exit(1);
    }

    let hint = generate_hint(&direction, seed);
    println!("{}", hint);
}
