use clap::Parser;

/// Simple mapping of radiation levels to hardy plants.
static PLANT_MAP: phf::Map<&'static str, &'static [&'static str]> = phf::phf_map! {
    "low" => &["Tomato", "Lettuce", "Carrot"],
    "medium" => &["Radish", "Sunflower", "Kale"],
    "high" => &["Radish", "Sunflower", "Kale"],
};

/// Command‑line arguments.
#[derive(Parser, Debug)]
#[command(author, version, about = "Post‑apocalyptic garden planner", long_about = None)]
struct Args {
    /// Name of the location (e.g., "Wasteland Outpost")
    location: String,
    /// Radiation level: low, medium, or high
    #[arg(value_parser = validate_radiation)]
    radiation: String,
}

fn validate_radiation(s: &str) -> Result<String, String> {
    let lower = s.to_lowercase();
    match lower.as_str() {
        "low" | "medium" | "high" => Ok(lower),
        _ => Err(format!("Invalid radiation level '{}'. Use low, medium, or high.", s)),
    }
}

fn recommend_plants(radiation: &str) -> &'static [&'static str] {
    PLANT_MAP.get(radiation).copied().unwrap_or(&[])
}

fn main() {
    let args = Args::parse();
    let plants = recommend_plants(&args.radiation);
    println!("Location: {}", args.location);
    println!("Radiation level: {}", args.radiation);
    println!("Recommended plants:");
    for plant in plants {
        println!(" - {}", plant);
    }
}
