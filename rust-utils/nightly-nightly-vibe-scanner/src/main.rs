use clap::Parser;
use std::collections::HashMap;
use std::io::{self, Read};

#[derive(Debug, PartialEq, Eq, Clone, Copy)]
enum Vibe {
    Hopeful,
    Despairing,
    Chaotic,
    Resourceful,
    Neutral,
}

impl std::fmt::Display for Vibe {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{:?}", self)
    }
}

#[derive(Parser, Debug)]
#[command(author, version, about = "Scans text for apocalyptic vibes.", long_about = None)]
struct Args {
    /// Optional file to read input from. If not provided, reads from stdin.
    #[arg(short, long)]
    file: Option<String>,
}

fn get_vibe_keywords() -> HashMap<Vibe, Vec<&'static str>> {
    let mut map = HashMap::new();
    map.insert(Vibe::Hopeful, vec!["hope", "future", "build", "grow", "together", "dawn", "survive", "rebuild", "resilience", "optimism"]);
    map.insert(Vibe::Despairing, vec!["doom", "despair", "lost", "end", "alone", "ruin", "darkness", "hopeless", "no escape", "futility", "gloom"]);
    map.insert(Vibe::Chaotic, vec!["chaos", "anarchy", "madness", "scream", "fight", "unrest", "shattered", "broken", "turmoil", "disorder"]);
    map.insert(Vibe::Resourceful, vec!["scavenge", "craft", "repair", "find", "gather", "resource", "ingenuity", "solution", "make do", "improvise", "salvage"]);
    map
}

fn scan_vibe(text: &str) -> (Vibe, Vec<String>) {
    let text_lower = text.to_lowercase();
    let keywords_map = get_vibe_keywords();
    let mut vibe_scores: HashMap<Vibe, usize> = HashMap::new();
    let mut detected_keywords: Vec<String> = Vec::new();

    for (vibe, keywords) in keywords_map.iter() {
        for keyword in keywords.iter() {
            if text_lower.contains(keyword) {
                *vibe_scores.entry(*vibe).or_insert(0) += 1;
                detected_keywords.push(keyword.to_string());
            }
        }
    }

    if detected_keywords.is_empty() {
        return (Vibe::Neutral, detected_keywords);
    }

    let mut dominant_vibe = Vibe::Neutral;
    let mut max_score = 0;

    // Prioritize specific vibes over Neutral if any keywords are found
    for (vibe, score) in vibe_scores.iter() {
        if *score > max_score {
            max_score = *score;
            dominant_vibe = *vibe;
        } else if *score == max_score {
            // Simple tie-breaking: prefer Hopeful > Resourceful > Chaotic > Despairing
            // This is arbitrary but provides deterministic behavior.
            dominant_vibe = match (dominant_vibe, *vibe) {
                (Vibe::Hopeful, _) => Vibe::Hopeful,
                (_, Vibe::Hopeful) => Vibe::Hopeful,
                (Vibe::Resourceful, _) => Vibe::Resourceful,
                (_, Vibe::Resourceful) => Vibe::Resourceful,
                (Vibe::Chaotic, _) => Vibe::Chaotic,
                (_, Vibe::Chaotic) => Vibe::Chaotic,
                (Vibe::Despairing, _) => Vibe::Despairing,
                (_, Vibe::Despairing) => Vibe::Despairing,
                _ => dominant_vibe, // Should not happen if keywords are found
            };
        }
    }

    detected_keywords.sort_unstable();
    detected_keywords.dedup();

    (dominant_vibe, detected_keywords)
}

fn main() -> io::Result<()> {
    let args = Args::parse();

    let mut input_text = String::new();

    match args.file {
        Some(file_path) => {
            let mut file = std::fs::File::open(&file_path)?;
            file.read_to_string(&mut input_text)?;
        }
        None => {
            io::stdin().read_to_string(&mut input_text)?;
        }
    }

    if input_text.trim().is_empty() {
        println!("Vibe: Neutral");
        println!("Detected Keywords: None");
        return Ok(());
    }

    let (vibe, keywords) = scan_vibe(&input_text);

    println!("Vibe: {}", vibe);
    if keywords.is_empty() {
        println!("Detected Keywords: None");
    } else {
        println!("Detected Keywords: {}", keywords.join(", "));
    }

    Ok(())
}
