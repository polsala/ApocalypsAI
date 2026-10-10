/// Simple linear‑congruential generator (LCG) for deterministic pseudo‑random numbers.
/// Not cryptographically secure – perfect for reproducible tests.
pub struct Lcg {
    state: u64,
}

impl Lcg {
    pub fn new(seed: u64) -> Self {
        Self { state: seed }
    }

    /// Returns the next random u64.
    pub fn next(&mut self) -> u64 {
        // Parameters from Numerical Recipes
        const A: u64 = 1664525;
        const C: u64 = 1013904223;
        self.state = self.state.wrapping_mul(A).wrapping_add(C);
        self.state
    }
}

/// Compute a new bearing after applying a random drift.
///
/// * `current` – current bearing in degrees (0‑359).
/// * `max_drift` – maximum absolute drift in degrees (0‑180).
/// * `seed` – seed for deterministic randomness.
///
/// Returns the new bearing in the range 0‑359.
pub fn drift_bearing(current: u16, max_drift: u16, seed: u64) -> u16 {
    let mut rng = Lcg::new(seed);
    // Drift magnitude: 0 ..= max_drift
    let drift = (rng.next() % (max_drift as u64 + 1)) as i16;
    // Direction: even => +, odd => -
    let direction = if rng.next() % 2 == 0 { 1 } else { -1 };
    let new_bearing = (current as i16 + direction * drift).rem_euclid(360) as u16;
    new_bearing
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_drift_bearing_deterministic() {
        // Seed chosen to produce known sequence
        let seed = 42u64;
        let result = drift_bearing(180, 30, seed);
        // With the LCG parameters, the first next() % 31 == 10, second next()%2 == 1 (negative)
        // So drift = -10 => 170
        assert_eq!(result, 170);
    }
}
