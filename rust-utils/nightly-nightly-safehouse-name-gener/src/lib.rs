use rand::prelude::*;
use rand_chacha::ChaCha8Rng;

static ADJECTIVES: &[&str] = &[
    "Radiant", "Dusty", "Silent", "Echoing", "Forgotten", "Shimmering", "Bleak", "Gleaming",
    "Crumbling", "Hidden",
];

static NOUNS: &[&str] = &[
    "Oasis", "Haven", "Sanctum", "Refuge", "Bastion", "Vault", "Citadel", "Shelter", "Outpost",
    "Harbor",
];

/// Generates a safe‑house name based on a deterministic seed.
///
/// The function picks one adjective and one noun from predefined lists using a
/// ChaCha8 RNG seeded with `seed`. The result is formatted as "<Adjective> <Noun>".
pub fn generate_name(seed: u64) -> String {
    let mut rng = ChaCha8Rng::seed_from_u64(seed);
    let adj = ADJECTIVES.choose(&mut rng).unwrap();
    let noun = NOUNS.choose(&mut rng).unwrap();
    format!("{} {}", adj, noun)
}
