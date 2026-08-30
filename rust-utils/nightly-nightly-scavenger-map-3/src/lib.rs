pub fn generate_map(width: usize, height: usize, seed: u64) -> String {
    use rand::{Rng, SeedableRng};
    use rand::rngs::StdRng;

    let mut rng = StdRng::seed_from_u64(seed);
    let symbols = ['.', 'W', 'F', 'M', 'T'];
    let mut lines = Vec::with_capacity(height);

    for _ in 0..height {
        let line: String = (0..width)
            .map(|_| {
                let idx = rng.gen_range(0..symbols.len());
                symbols[idx]
            })
            .collect();
        lines.push(line);
    }
    lines.join("\n")
}
