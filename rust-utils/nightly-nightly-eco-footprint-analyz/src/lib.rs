use csv::ReaderBuilder;
use serde::Deserialize;

#[derive(Deserialize)]
struct Record {
    activity: String,
    co2_kg: f64,
}

/// Computes total CO₂ from CSV content.
/// Returns error if parsing fails.
pub fn compute_total(csv_content: &str) -> Result<f64, Box<dyn std::error::Error>> {
    let mut rdr = ReaderBuilder::new()
        .has_headers(true)
        .from_reader(csv_content.as_bytes());

    let mut total = 0.0;
    for result in rdr.deserialize() {
        let record: Record = result?;
        total += record.co2_kg;
    }
    Ok(total)
}
