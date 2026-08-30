/// Generates a deterministic scavenger route.
///
/// The algorithm sorts the input locations alphabetically and then rotates the
/// list left by `seed % len` positions. This guarantees the same output for the
/// same input and seed, without any external randomness.
///
/// # Arguments
///
/// * `locations` – Slice of location names.
/// * `seed` – An arbitrary u64 used to compute the rotation offset.
///
/// # Returns
///
/// A `Vec<String>` containing the ordered route.
pub fn generate_route(locations: &[&str], seed: u64) -> Vec<String> {
    let mut locs: Vec<&str> = locations.to_vec();
    // Alphabetical order provides a stable baseline.
    locs.sort();
    if !locs.is_empty() {
        let shift = (seed as usize) % locs.len();
        locs.rotate_left(shift);
    }
    locs.iter().map(|s| s.to_string()).collect()
}
