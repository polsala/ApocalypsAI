pub fn recommended_steps(source: &str, contamination_ppm: u32) -> Vec<&'static str> {
    let mut steps = Vec::new();

    // Sourceâspecific preâtreatment
    match source.to_lowercase().as_str() {
        "rain" => steps.push("Collect in clean container"),
        "well" => steps.push("Preâfilter through cloth"),
        "river" | "pond" | "lake" => steps.push("Preâfilter through coarse material"),
        _ => steps.push("Assume unknown source; treat cautiously"),
    }

    // Contamination thresholds (ppm)
    if contamination_ppm > 0 && contamination_ppm <= 50 {
        steps.push("Boil for 1 minute");
    } else if contamination_ppm <= 200 {
        steps.push("Boil for 5 minutes");
        steps.push("Add chlorine tablets (1 per liter)");
    } else {
        steps.push("Boil for 10 minutes");
        steps.push("Add chlorine tablets (2 per liter)");
        steps.push("Use activated carbon filter");
    }

    steps
}

