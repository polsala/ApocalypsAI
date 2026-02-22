use clap::Parser;
use serde::Deserialize;
use std::error::Error;
use std::fs::File;
use std::path::PathBuf;

#[derive(Debug, Deserialize, Clone)]
struct Item {
    name: String,
    weight: u32,
    value: u32,
}

#[derive(Parser, Debug)]
#[command(author, version, about = "Optimizes a scavenger's pack based on weight and value.", long_about = None)]
struct Args {
    /// The maximum total weight the scavenger can carry.
    #[arg(short = 'w', long)]
    max_weight: u32,

    /// Path to a CSV file containing the items (name, weight, value).
    #[arg(short = 'f', long)]
    items_file: PathBuf,
}

fn main() -> Result<(), Box<dyn Error>> {
    let args = Args::parse();

    println!("Optimizing for max weight: {}", args.max_weight);

    let file = File::open(&args.items_file)?;
    let mut rdr = csv::Reader::from_reader(file);
    let mut items: Vec<Item> = Vec::new();
    for result in rdr.deserialize() {
        let item: Item = result?;
        items.push(item);
    }

    let num_items = items.len();
    let max_weight = args.max_weight as usize;

    // dp[w] will store the maximum value that can be achieved with weight 'w'
    let mut dp = vec![0; max_weight + 1];
    // selected_items_tracker[i][w] stores the items chosen to achieve dp[w] considering items up to index i-1.
    // selected_items_tracker[i+1][w] stores items after considering item 'i'.
    let mut selected_items_tracker: Vec<Vec<Vec<Item>>> = vec![vec![Vec::new(); max_weight + 1]; num_items + 1];

    for i in 0..num_items {
        let item = &items[i];
        let item_weight = item.weight as usize;
        let item_value = item.value;

        for w in 0..=max_weight {
            // Option 1: Don't take the current item 'i'
            selected_items_tracker[i + 1][w] = selected_items_tracker[i][w].clone();
            dp[w] = dp[w]; // Value remains the same as without item 'i'

            // Option 2: Take the current item 'i', if it fits and improves value
            if w >= item_weight {
                if dp[w - item_weight] + item_value > dp[w] {
                    dp[w] = dp[w - item_weight] + item_value;
                    let mut new_selection = selected_items_tracker[i][w - item_weight].clone();
                    new_selection.push(item.clone());
                    selected_items_tracker[i + 1][w] = new_selection;
                }
            }
        }
    }

    let mut total_weight = 0;
    let mut total_value = 0;
    let mut final_selection: Vec<Item> = Vec::new();

    // Find the maximum value achieved and the corresponding weight index
    let mut optimal_weight_idx = 0;
    for w in (0..=max_weight).rev() {
        if dp[w] >= dp[optimal_weight_idx] {
            optimal_weight_idx = w;
        }
    }

    // Reconstruct the selected items using the tracker at the final state
    final_selection = selected_items_tracker[num_items][optimal_weight_idx].clone();

    for item in &final_selection {
        total_weight += item.weight;
        total_value += item.value;
    }

    println!("Selected Items:");
    if final_selection.is_empty() {
        println!("  (No items selected)");
    } else {
        for item in final_selection {
            println!("- {} (Weight: {}, Value: {})", item.name, item.weight, item.value);
        }
    }

    println!("\nTotal Weight: {}", total_weight);
    println!("Total Value: {}", total_value);

    Ok(())
}
