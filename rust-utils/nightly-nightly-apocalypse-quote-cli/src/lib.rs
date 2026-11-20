pub const QUOTES: [&'static str; 5] = [
    "The sky fell, but we still code.",
    "When the servers burn, the logs remain.",
    "In the ash of CI, a new build rises.",
    "Debugging the end of the world, one line at a time.",
    "Even the apocalypse needs a good commit message."
];

/// Returns a quote.
///
/// * If `seed` is `Some`, the quote is selected deterministically using the seed modulo the number of quotes.
/// * If `seed` is `None`, a random quote is chosen.
pub fn get_quote(seed: Option<u64>) -> &'static str {
    match seed {
        Some(s) => {
            let idx = (s as usize) % QUOTES.len();
            QUOTES[idx]
        }
        None => {
            use rand::Rng;
            let mut rng = rand::thread_rng();
            let idx = rng.gen_range(0..QUOTES.len());
            QUOTES[idx]
        }
    }
}
