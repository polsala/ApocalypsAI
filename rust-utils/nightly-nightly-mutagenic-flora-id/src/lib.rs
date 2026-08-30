use clap::Parser;

#[derive(Debug, PartialEq)]
pub struct FloraEntry {
    pub name: &'static str,
    pub color: &'static str,
    pub shape: &'static str,
    pub glow: bool,
    pub sound: Option<&'static str>,
    pub properties: Vec<&'static str>,
}

// The whimsical flora database
pub const FLORA_DB: &[FloraEntry] = &[
    FloraEntry {
        name: "Gloom Bloom",
        color: "dark-purple",
        shape: "bell",
        glow: true,
        sound: Some("faint-hum"),
        properties: vec!["Poisonous", "Causes temporary blindness"],
    },
    FloraEntry {
        name: "Shimmer Shroom",
        color: "iridescent",
        shape: "umbrella",
        glow: true,
        sound: None,
        properties: vec!["Edible", "Grants enhanced night vision for 1 hour"],
    },
    FloraEntry {
        name: "Whisper Weed",
        color: "pale-green",
        shape: "vine",
        glow: false,
        sound: Some("soft-rustle"),
        properties: vec!["Hallucinogenic", "Induces mild temporal disorientation"],
    },
    FloraEntry {
        name: "Sunpetal",
        color: "bright-yellow",
        shape: "star",
        glow: false,
        sound: None,
        properties: vec!["Edible", "Rich in Vitamin C"],
    },
    FloraEntry {
        name: "Crimson Spore",
        color: "crimson",
        shape: "cluster",
        glow: true,
        sound: Some("low-throb"),
        properties: vec!["Highly Toxic", "Causes rapid cellular decay"],
    },
    FloraEntry {
        name: "Void Blossom",
        color: "black",
        shape: "spiral",
        glow: true,
        sound: Some("deep-resonance"),
        properties: vec!["Temporal Displacement", "Highly Unstable"],
    },
    FloraEntry {
        name: "Glimmer Grass",
        color: "emerald-green",
        shape: "blade",
        glow: true,
        sound: None,
        properties: vec!["Edible", "Provides minor healing"],
    }
];

/// Command-line arguments for flora identification.
#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
pub struct FloraArgs {
    /// Color of the flora (e.g., "red", "dark-purple", "iridescent")
    #[clap(long)]
    pub color: Option<String>,

    /// Shape of the flora (e.g., "bell", "umbrella", "vine", "star")
    #[clap(long)]
    pub shape: Option<String>,

    /// Does the flora glow? (true/false)
    #[clap(long)]
    pub glow: Option<bool>,

    /// Description of any sound the flora makes (e.g., "faint-hum", "soft-rustle", "low-throb")
    #[clap(long)]
    pub sound: Option<String>,
}

pub fn find_flora(args: &FloraArgs) -> Vec<&'static FloraEntry> {
    let mut identified_flora: Vec<&FloraEntry> = Vec::new();

    for entry in FLORA_DB.iter() {
        let mut matches = true;

        if let Some(color) = &args.color {
            if entry.color != color {
                matches = false;
            }
        }
        if let Some(shape) = &args.shape {
            if entry.shape != shape {
                matches = false;
            }
        }
        if let Some(glow) = args.glow {
            if entry.glow != glow {
                matches = false;
            }
        }
        if let Some(sound) = &args.sound {
            // If a sound argument is provided, the entry must have a sound, and it must match.
            // If entry.sound is None, or if it's Some(s) but s != sound, it doesn't match.
            if entry.sound.map_or(true, |s| s != sound) {
                matches = false;
            }
        }
        // If args.sound is None, we don't filter by sound, so 'matches' remains true for this criterion.

        if matches {
            identified_flora.push(entry);
        }
    }
    identified_flora
}
