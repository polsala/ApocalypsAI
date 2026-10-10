use std::collections::hash_map::DefaultHasher;
use std::hash::{Hash, Hasher};

/// A cryptid paired with one or more habitat tags.
struct Cryptid {
    name: &'static str,
    habitats: &'static [&'static str],
}

static CRYPTIDS: &[Cryptid] = &[
    Cryptid { name: "The Wendigo", habitats: &["forest", "cold"] },
    Cryptid { name: "Mokele‑Mbembe", habitats: &["swamp", "river"] },
    Cryptid { name: "Chupacabra", habitats: &["desert", "cave"] },
    Cryptid { name: "Jersey Devil", habitats: &["mountain", "forest"] },
    Cryptid { name: "Mongolian Death Worm", habitats: &["desert", "sand"] },
    Cryptid { name: "Lake Monster", habitats: &["lake", "water"] },
    Cryptid { name: "Skinwalker", habitats: &["urban", "plains"] },
    Cryptid { name: "Bunyip", habitats: &["swamp", "river"] },
    Cryptid { name: "Yeti", habitats: &["mountain", "cold"] },
    Cryptid { name: "Mothman", habitats: &["urban", "forest"] },
];

/// Compute a deterministic hash of the input string and map it to a cryptid.
pub fn get_cryptid(location: &str) -> &'static str {
    // Normalise input to lower case for case‑insensitive matching.
    let loc = location.to_ascii_lowercase();
    // Find the first cryptid whose habitats contain the location keyword.
    let matching: Vec<&Cryptid> = CRYPTIDS
        .iter()
        .filter(|c| c.habitats.iter().any(|h| *h == loc))
        .collect();
    let candidates = if matching.is_empty() { CRYPTIDS } else { matching.as_slice() };
    // Deterministic hash → index.
    let mut hasher = DefaultHasher::new();
    loc.hash(&mut hasher);
    let hash = hasher.finish();
    let idx = (hash as usize) % candidates.len();
    candidates[idx].name
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_forest() {
        assert_eq!(get_cryptid("forest"), "The Wendigo");
    }
    #[test]
    fn test_desert() {
        assert_eq!(get_cryptid("desert"), "Mongolian Death Worm");
    }
    #[test]
    fn test_unknown() {
        // "space" is not a known habitat, falls back to full list.
        // Hash of "space" yields a deterministic cryptid.
        assert_eq!(get_cryptid("space"), "Mothman");
    }
}
