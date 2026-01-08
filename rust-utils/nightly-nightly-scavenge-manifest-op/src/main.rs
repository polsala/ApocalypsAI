use clap::Parser;
use std::error::Error;
use std::fs::File;
use serde::Deserialize;

#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Path to the manifest CSV file (name,weight,value)
    #[arg(short, long)]
    manifest: String,

    /// Maximum weight capacity for the manifest
    #[arg(short, long)]
    limit: u32,
}

#[derive(Debug, Deserialize, Clone, PartialEq, Eq)]
struct Item {
    name: String,
    weight: u32,
    value: u32,
}

/// Optimizes a list of items to maximize total value within a given weight limit.
/// Implements the 0/1 Knapsack problem using dynamic programming.
/// Returns the total value, total weight, and a vector of chosen items.
fn optimize_manifest(items: &[Item], weight_limit: u32) -> (u32, u32, Vec<Item>) {
    let n = items.len();
    let w_limit_usize = weight_limit as usize;

    // dp[i][w] stores the maximum value that can be obtained using the first 'i' items
    // with a total weight not exceeding 'w'.
    let mut dp = vec![vec![0; w_limit_usize + 1]; n + 1];

    for i in 1..=n {
        let item = &items[i - 1];
        let item_weight = item.weight as usize;
        let item_value = item.value;

        for w in 0..=w_limit_usize {
            if item_weight <= w {
                // Either include the current item or don't.
                // Take the maximum value.
                dp[i][w] = std::cmp::max(dp[i - 1][w], dp[i - 1][w - item_weight] + item_value);
            } else {
                // Current item is too heavy, cannot include it.
                dp[i][w] = dp[i - 1][w];
            }
        }
    }

    let max_value = dp[n][w_limit_usize];
    let mut current_weight = w_limit_usize;
    let mut chosen_items = Vec::new();
    let mut total_weight_chosen = 0;

    // Backtrack through the DP table to reconstruct the chosen items.
    for i in (1..=n).rev() {
        if dp[i][current_weight] != dp[i - 1][current_weight] {
            // This item was included in the optimal solution for dp[i][current_weight]
            let item = &items[i - 1];
            chosen_items.push(item.clone());
            total_weight_chosen += item.weight;
            current_weight -= item.weight as usize;
        }
    }

    chosen_items.reverse(); // Reverse to get items in their original order or a more natural order

    (max_value, total_weight_chosen, chosen_items)
}

fn main() -> Result<(), Box<dyn Error>> {
    let args = Args::parse();

    let file = File::open(&args.manifest)?;
    let mut rdr = csv::Reader::from_reader(file);
    let mut items = Vec::new();
    for result in rdr.deserialize() {
        let item: Item = result?;
        items.push(item);
    }

    let (total_value, total_weight, chosen_items) = optimize_manifest(&items, args.limit);

    println!("--- Scavenger's Manifest Optimization Report ---");
    println!("Weight Limit: {} units", args.limit);
    println!("Total Value: {} credits", total_value);
    println!("Total Weight: {} units", total_weight);
    println!("\nChosen Items:");
    if chosen_items.is_empty() {
        println!("  No items selected within the weight limit.");
    } else {
        for item in chosen_items {
            println!("  - {} (Weight: {}, Value: {})", item.name, item.weight, item.value);
        }
    }

    Ok(())
}
