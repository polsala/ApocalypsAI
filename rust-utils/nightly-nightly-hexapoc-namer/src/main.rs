use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        eprintln!("Usage: {} <hex-color>", args[0]);
        std::process::exit(1);
    }
    let input = args[1].trim_start_matches('#');
    match hex_to_name(input) {
        Ok(name) => println!("{}", name),
        Err(e) => {
            eprintln!("Error: {}", e);
            std::process::exit(1);
        }
    }
}

fn hex_to_name(hex: &str) -> Result<String, String> {
    if hex.len() != 6 {
        return Err("Hex color must be 6 characters".into());
    }
    let r = u8::from_str_radix(&hex[0..2], 16).map_err(|_| "Invalid red component")?;
    let g = u8::from_str_radix(&hex[2..4], 16).map_err(|_| "Invalid green component")?;
    let b = u8::from_str_radix(&hex[4..6], 16).map_err(|_| "Invalid blue component")?;

    let adjectives = [
        "ashen", "blazing", "radioactive", "mutated", "wasteland", "crimson", "stormy", "frozen",
    ];
    let nouns = [
        "dawn", "horizon", "storm", "ruin", "sands", "shadows", "ember", "void",
    ];

    let sum = r as usize + g as usize + b as usize;
    let sum_sq = (r as usize * r as usize)
        + (g as usize * g as usize)
        + (b as usize * b as usize);

    let adj = adjectives[sum % adjectives.len()];
    let noun = nouns[sum_sq % nouns.len()];

    Ok(format!("{} {}", adj, noun))
}

// Unit tests
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_known_colors() {
        // Mock rationale: deterministic mapping based on simple hash
        assert_eq!(hex_to_name("ff4500").unwrap(), "blazing ember");
        assert_eq!(hex_to_name("00ff00").unwrap(), "ashen horizon");
        assert_eq!(hex_to_name("0000ff").unwrap(), "ashen void");
    }
}
