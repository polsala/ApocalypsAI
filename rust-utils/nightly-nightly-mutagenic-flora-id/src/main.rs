use nightly_mutagenic_flora_id::{find_flora, FloraArgs};

fn main() {
    let args = FloraArgs::parse();
    let identified_flora = find_flora(&args);

    if identified_flora.is_empty() {
        println!("No flora identified with the given characteristics.");
    } else {
        println!("Identified Flora:");
        for flora in identified_flora {
            println!("- Name: {}", flora.name);
            println!("  Properties: {}", flora.properties.join(", "));
        }
    }
}
