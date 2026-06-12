pub fn get_kit(scenario: &str) -> Vec<&'static str> {
    match scenario.to_lowercase().as_str() {
        "zombie" => vec!["Baseball bat", "Spare ammo", "First aid kit", "Water filter"],
        "radiation" => vec!["Geiger counter", "Lead blanket", "Potassium iodide tablets", "N95 mask"],
        "flood" => vec!["Waterproof boots", "Dry bags", "Life jacket", "Portable pump"],
        _ => vec!["Multi‑tool", "Flashlight", "Batteries", "Emergency food"],
    }
}
