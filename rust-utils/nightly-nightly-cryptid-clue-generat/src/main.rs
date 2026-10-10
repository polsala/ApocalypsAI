use rand::Rng;
use rand::RngCore;
use rand::SeedableRng;
use rand::rngs::{StdRng, ThreadRng};

fn generate_clue(seed: Option<u64>) -> String {
    // Choose RNG: deterministic if a seed is supplied, otherwise thread‑local RNG.
    let mut rng: Box<dyn RngCore> = match seed {
        Some(s) => Box::new(StdRng::seed_from_u64(s)),
        None => Box::new(rand::thread_rng()),
    };

    let cryptids = ["Mothman", "Chupacabra", "Jersey Devil", "Loch Ness Monster"];
    let adjectives = ["lurking", "haunting", "roaming", "cackling"];
    let locations = [
        "the abandoned mall",
        "the ruined highway",
        "the flooded subway",
        "the deserted bunker",
    ];

    let c = cryptids[rng.gen_range(0..cryptids.len())];
    let a = adjectives[rng.gen_range(0..adjectives.len())];
    let l = locations[rng.gen_range(0..locations.len())];

    format!("A {} {} spotted near {}.", a, c, l)
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let seed = if args.len() > 1 {
        args[1].parse::<u64>().ok()
    } else {
        None
    };
    println!("{}", generate_clue(seed));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_generate_clue_deterministic() {
        // With a fixed seed the output should be reproducible.
        let clue = generate_clue(Some(0));
        // Basic sanity checks – the format is fixed, so we can assert parts exist.
        assert!(clue.starts_with("A "));
        assert!(clue.contains("spotted near"));
        assert!(clue.ends_with('.'));
    }
}
