pub const ADJECTIVES: &[&str] = &["Gleaming", "Mournful", "Silent", "Radiant", "Twisted"];
pub const SUFFIXES: &[&str] = &["folia", "barkus", "petalus", "rootus", "stemma"];

/// Generate a plant name from explicit indices.
///
/// This function is deterministic and used by the test suite.
pub fn generate_name(adjective_idx: usize, suffix_idx: usize) -> String {
    let adj = ADJECTIVES.get(adjective_idx % ADJECTIVES.len()).unwrap_or(&"Mystic");
    let suf = SUFFIXES.get(suffix_idx % SUFFIXES.len()).unwrap_or(&"flora");
    format!("{} {}", adj, suf)
}

/// Generate a random plant name using the `rand` crate.
pub fn random_name() -> String {
    use rand::Rng;
    let mut rng = rand::thread_rng();
    let adj_idx = rng.gen_range(0..ADJECTIVES.len());
    let suf_idx = rng.gen_range(0..SUFFIXES.len());
    generate_name(adj_idx, suf_idx)
}
