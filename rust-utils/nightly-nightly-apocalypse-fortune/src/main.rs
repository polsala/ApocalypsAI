use rand::seq::SliceRandom;
use rand::rngs::StdRng;
use rand::SeedableRng;

static FORTUNES: &[&str] = &[
    "You will find a fresh water source behind the old billboard.",
    "A friendly mutant will share its secret stash of canned beans.",
    "Radiation levels will drop tomorrow; perfect time to venture out.",
    "Your compass points to a hidden cache of batteries.",
    "A solar flare will power your solar panel for a full day.",
    "You will discover a functional radio and hear good news.",
    "A stray dog will become your loyal companion.",
    "A sudden rain will reveal a safe path through the dunes.",
    "You will stumble upon a library still intact—knowledge is power.",
    "A mysterious traveler will teach you a new survival skill."
];

fn get_fortune<R: rand::Rng + ?Sized>(rng: &mut R) -> &'static str {
    FORTUNES.choose(rng).unwrap_or(&"Stay hopeful.")
}

fn main() {
    let mut rng = rand::thread_rng();
    let fortune = get_fortune(&mut rng);
    println!("{}", fortune);
}

#[cfg(test)]
mod tests {
    use super::*;
    use rand::rngs::StdRng;
    use rand::SeedableRng;

    #[test]
    fn deterministic_fortune() {
        // Seed with a known value (all zeros)
        let seed: [u8; 32] = [0; 32];
        let mut rng = StdRng::from_seed(seed);
        let fortune = get_fortune(&mut rng);
        // With this seed, the chosen fortune should be the first in the list
        assert_eq!(fortune, "You will find a fresh water source behind the old billboard.");
    }
}
