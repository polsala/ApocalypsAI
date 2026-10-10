use rand::{Rng, SeedableRng};
use rand::rngs::StdRng;
use std::env;

static SURVIVAL_QUOTES: &[&str] = &[
    "When the world ends, remember to keep your water filter clean.",
    "A canned bean a day keeps the radiation away.",
];

static WISDOM_QUOTES: &[&str] = &[
    "Even in ruins, a sunrise is still a sunrise.",
    "Hope is the last battery you’ll ever need.",
];

static HUMOR_QUOTES: &[&str] = &[
    "Why did the mutant cross the road? To get to the other side‑effect.",
    "I told my bunker it was time to upgrade – now it’s a smart bunker.",
];

fn get_quotes(category: &str) -> &'static [&'static str] {
    match category {
        "survival" => SURVIVAL_QUOTES,
        "wisdom" => WISDOM_QUOTES,
        "humor" => HUMOR_QUOTES,
        _ => &[
            "When in doubt, hoard more canned beans.",
            "The apocalypse is just a really long power outage.",
        ],
    }
}

fn get_random_quote<R: Rng + ?Sized>(category: Option<&str>, rng: &mut R) -> &'static str {
    let cat = category.unwrap_or("any");
    let quotes = get_quotes(cat);
    let idx = rng.gen_range(0..quotes.len());
    quotes[idx]
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let mut category: Option<&str> = None;
    if args.len() > 1 && args[1] == "--category" && args.len() > 2 {
        category = Some(&args[2]);
    }
    // Use thread_rng for normal execution
    let mut rng = rand::thread_rng();
    let quote = get_random_quote(category, &mut rng);
    println!("{}", quote);
}

// Export for tests
#[cfg(test)]
mod tests {
    use super::*;
    use rand::SeedableRng;

    #[test]
    fn test_survival_category_deterministic() {
        let mut rng = StdRng::seed_from_u64(42);
        let quote = get_random_quote(Some("survival"), &mut rng);
        assert_eq!(quote, "When the world ends, remember to keep your water filter clean.");
    }

    #[test]
    fn test_unknown_category_fallback() {
        let mut rng = StdRng::seed_from_u64(1);
        let quote = get_random_quote(Some("unknown"), &mut rng);
        assert_eq!(quote, "When in doubt, hoard more canned beans.");
    }
}
