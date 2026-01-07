use clap::Parser;
use csv::{ReaderBuilder, WriterBuilder};
use serde::{Deserialize, Serialize};
use std::error::Error;
use std::fs::File;
use std::io::{self, Write};
use std::path::PathBuf;

#[derive(Parser, Debug)]
#[command(author, version, about = "Optimizes and rebalances survival rations.", long_about = None)]
struct Args {
    /// Path to the input CSV file containing ration inventory.
    input_csv: PathBuf,

    /// The desired daily caloric intake.
    #[arg(short = 't', long)]
    target_calories: u32,

    /// Path to save the updated inventory after rebalancing. If not provided, prints to stdout.
    #[arg(short = 'o', long)]
    output_csv: Option<PathBuf>,
}

#[derive(Debug, Deserialize, Serialize, Clone)]
struct RationItem {
    name: String,
    calories_per_unit: u32,
    units_available: u32,
    perishability_score: u8, // 1 (low) to 5 (high)
}

#[derive(Debug, Default)]
struct RationPlan {
    consumed_items: Vec<(String, u32, u32)>, // (name, units, calories)
    total_consumed_calories: u32,
}

fn main() -> Result<(), Box<dyn Error>> {
    let args = Args::parse();

    let mut items = load_ration_items(&args.input_csv)?;

    let (plan, remaining_items) = calculate_ration_plan(&mut items, args.target_calories);

    print_ration_plan(&plan, args.target_calories);

    if let Some(output_path) = args.output_csv {
        save_remaining_items(&output_path, &remaining_items)?;
        println!("\nUpdated inventory saved to: {}", output_path.display());
    } else {
        print_remaining_items(&remaining_items)?;
    }

    Ok(())
}

fn load_ration_items(path: &PathBuf) -> Result<Vec<RationItem>, Box<dyn Error>> {
    let file = File::open(path)?;
    let mut rdr = ReaderBuilder::new().has_headers(true).from_reader(file);
    let mut items = Vec::new();
    for result in rdr.deserialize() {
        let item: RationItem = result?;
        items.push(item);
    }
    Ok(items)
}

fn calculate_ration_plan(
    items: &mut Vec<RationItem>,
    target_calories: u32,
) -> (RationPlan, Vec<RationItem>) {
    // Sort items by perishability (lowest score first, then by calories_per_unit descending for tie-breaking)
    items.sort_by(|a, b| {
        a.perishability_score
            .cmp(&b.perishability_score)
            .then_with(|| b.calories_per_unit.cmp(&a.calories_per_unit))
    });

    let mut plan = RationPlan::default();
    let mut remaining_items = items.clone(); // Clone to modify and return remaining inventory
    let mut current_calories = 0;

    for i in 0..remaining_items.len() {
        if current_calories >= target_calories {
            break;
        }

        let item = &mut remaining_items[i];
        if item.units_available == 0 {
            continue;
        }

        let calories_needed = target_calories - current_calories;
        let units_to_consume = (calories_needed / item.calories_per_unit).min(item.units_available);

        if units_to_consume > 0 {
            let consumed_calories = units_to_consume * item.calories_per_unit;
            plan.consumed_items
                .push((item.name.clone(), units_to_consume, consumed_calories));
            plan.total_consumed_calories += consumed_calories;
            current_calories += consumed_calories;
            item.units_available -= units_to_consume;
        }
    }

    (plan, remaining_items)
}

fn print_ration_plan(plan: &RationPlan, target_calories: u32) {
    println!("--- Daily Ration Plan (Target: {} Calories) ---", target_calories);
    if plan.consumed_items.is_empty() {
        println!("No items consumed to meet target.");
    } else {
        for (name, units, calories) in &plan.consumed_items {
            println!("Consume {} units of {} ({} calories)", units, name, calories);
        }
        println!(
            "Total Consumed: {} calories (Remaining: {} calories to target)",
            plan.total_consumed_calories,
            target_calories.saturating_sub(plan.total_consumed_calories)
        );
    }
}

fn print_remaining_items(items: &[RationItem]) -> Result<(), Box<dyn Error>> {
    println!("\n--- Remaining Inventory ---");
    let mut wtr = WriterBuilder::new().has_headers(true).from_writer(io::stdout());
    wtr.serialize(("name", "units_available", "calories_per_unit", "perishability_score"))?;
    for item in items {
        wtr.serialize((&item.name, item.units_available, item.calories_per_unit, item.perishability_score))?;
    }
    wtr.flush()?;
    Ok(())
}

fn save_remaining_items(path: &PathBuf, items: &[RationItem]) -> Result<(), Box<dyn Error>> {
    let file = File::create(path)?;
    let mut wtr = WriterBuilder::new().has_headers(true).from_writer(file);
    wtr.serialize(("name", "units_available", "calories_per_unit", "perishability_score"))?;
    for item in items {
        wtr.serialize((&item.name, item.units_available, item.calories_per_unit, item.perishability_score))?;
    }
    wtr.flush()?;
    Ok(())
}
