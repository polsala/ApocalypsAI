use clap::{Parser, Subcommand};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs;
use std::path::Path;
use std::time::{SystemTime, UNIX_EPOCH};
use colored::*;

#[derive(Parser)]
#[command(name = "nightly-rust-resource-tracker")]
#[command(about = "A high-performance CLI tool for tracking post-apocalyptic resources")]
#[command(version = "1.0.0")]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    Add { 
        #[arg(short, long)]
        name: String,
        #[arg(short, long)]
        quantity: u32,
        #[arg(short, long)]
        category: String,
    },
    List,
    Update {
        #[arg(short, long)]
        name: String,
        #[arg(short, long)]
        quantity: u32,
    },
    Remove {
        #[arg(short, long)]
        name: String,
    },
    Export {
        #[arg(short, long)]
        format: String,
        #[arg(short, long)]
        output: String,
    },
    Interactive,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct Resource {
    name: String,
    quantity: u32,
    category: String,
    last_updated: u64,
}

#[derive(Debug, Serialize, Deserialize)]
struct ResourceTracker {
    resources: HashMap<String, Resource>,
}

impl ResourceTracker {
    fn new() -> Self {
        Self {
            resources: HashMap::new(),
        }
    }

    fn load() -> Result<Self, Box<dyn std::error::Error>> {
        let data = fs::read_to_string("resources.json")?;
        Ok(serde_json::from_str(&data)?)
    }

    fn save(&self) -> Result<(), Box<dyn std::error::Error>> {
        let data = serde_json::to_string_pretty(self)?;
        fs::write("resources.json", data)?;
        Ok(())
    }

    fn add_resource(&mut self, name: String, quantity: u32, category: String) {
        let now = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_secs();
        
        let resource = Resource {
            name: name.clone(),
            quantity,
            category,
            last_updated: now,
        };
        
        self.resources.insert(name, resource);
        println!("{} Resource added successfully!", "✓".green());
    }

    fn list_resources(&self) {
        if self.resources.is_empty() {
            println!("{} No resources found.", "⚠".yellow());
            return;
        }
        
        println!("\n{} Current Resources:\n", "📊".blue());
        println!("{:<20} {:<10} {:<15} {:<20}", "Name", "Quantity", "Category", "Last Updated");
        println!("{:-<70}", "");
        
        for resource in self.resources.values() {
            println!(
                "{:<20} {:<10} {:<15} {:<20}",
                resource.name,
                resource.quantity.to_string(),
                resource.category,
                resource.last_updated.to_string()
            );
        }
    }

    fn update_quantity(&mut self, name: String, quantity: u32) -> Result<(), String> {
        match self.resources.get_mut(&name) {
            Some(resource) => {
                resource.quantity = quantity;
                resource.last_updated = SystemTime::now()
                    .duration_since(UNIX_EPOCH)
                    .unwrap()
                    .as_secs();
                println!("{} Quantity updated successfully!", "✓".green());
                Ok(())
            },
            None => Err(format!("Resource '{}' not found", name)),
        }
    }

    fn remove_resource(&mut self, name: String) -> Result<(), String> {
        match self.resources.remove(&name) {
            Some(_) => {
                println!("{} Resource removed successfully!", "✓".green());
                Ok(())
            },
            None => Err(format!("Resource '{}' not found", name)),
        }
    }

    fn export_to_json(&self, path: &str) -> Result<(), Box<dyn std::error::Error>> {
        let data = serde_json::to_string_pretty(self)?;
        fs::write(path, data)?;
        println!("{} Exported to {}", "✓".green(), path);
        Ok(())
    }

    fn export_to_csv(&self, path: &str) -> Result<(), Box<dyn std::error::Error>> {
        let mut wtr = csv::Writer::from_path(path)?;
        
        for resource in self.resources.values() {
            wtr.write_record(&[
                &resource.name,
                &resource.quantity.to_string(),
                &resource.category,
                &resource.last_updated.to_string(),
            ])?;
        }
        
        wtr.flush()?;
        println!("{} Exported to {}", "✓".green(), path);
        Ok(())
    }

    fn analytics(&self) {
        if self.resources.is_empty() {
            println!("{} No resources to analyze.", "⚠".yellow());
            return;
        }
        
        let total_quantity: u32 = self.resources.values().map(|r| r.quantity).sum();
        let category_counts: HashMap<String, u32> = self.resources.values()
            .fold(HashMap::new(), |mut acc, r| {
                *acc.entry(r.category.clone()).or_insert(0) += r.quantity;
                acc
            });
        
        println!("\n{} Analytics Dashboard:\n", "📈".magenta());
        println!("Total Resources: {}", total_quantity);
        println!("\nCategory Breakdown:");
        for (category, count) in category_counts.iter() {
            println!("  {}: {}", category, count);
        }
    }
}

fn interactive_mode() -> Result<(), Box<dyn std::error::Error>> {
    println!("{} Welcome to Interactive Mode!", "🎮".cyan());
    println!("Type 'help' for available commands or 'exit' to quit.\n");
    
    let mut tracker = if Path::new("resources.json").exists() {
        ResourceTracker::load()?
    } else {
        ResourceTracker::new()
    };
    
    loop {
        print!("{} ", ">".cyan());
        std::io::Write::flush(&mut std::io::stdout())?;
        
        let mut input = String::new();
        std::io::stdin().read_line(&mut input)?;
        let input = input.trim();
        
        if input.eq_ignore_ascii_case("exit") {
            break;
        }
        
        let parts: Vec<&str> = input.split_whitespace().collect();
        
        match parts.get(0) {
            Some(&"help") => {
                println!("Available commands:");
                println!("  add <name> <quantity> <category> - Add a resource");
                println!("  list - List all resources");
                println!("  update <name> <quantity> - Update resource quantity");
                println!("  remove <name> - Remove a resource");
                println!("  analytics - Show analytics");
                println!("  save - Save changes");
                println!("  exit - Exit interactive mode");
            },
            Some(&"add") => {
                if parts.len() >= 4 {
                    let name = parts[1].to_string();
                    let quantity = parts[2].parse::<u32>().unwrap_or(0);
                    let category = parts[3].to_string();
                    tracker.add_resource(name, quantity, category);
                } else {
                    println!("{} Usage: add <name> <quantity> <category>", "⚠".yellow());
                }
            },
            Some(&"list") => {
                tracker.list_resources();
            },
            Some(&"update") => {
                if parts.len() >= 3 {
                    let name = parts[1].to_string();
                    let quantity = parts[2].parse::<u32>().unwrap_or(0);
                    if let Err(e) = tracker.update_quantity(name, quantity) {
                        println!("{} Error: {}", "✗".red(), e);
                    }
                } else {
                    println!("{} Usage: update <name> <quantity>", "⚠".yellow());
                }
            },
            Some(&"remove") => {
                if let Some(name) = parts.get(1) {
                    if let Err(e) = tracker.remove_resource(name.to_string()) {
                        println!("{} Error: {}", "✗".red(), e);
                    }
                } else {
                    println!("{} Usage: remove <name>", "⚠".yellow());
                }
            },
            Some(&"analytics") => {
                tracker.analytics();
            },
            Some(&"save") => {
                tracker.save()?;
                println!("{} Changes saved!", "✓".green());
            },
            Some(_) => {
                println!("{} Unknown command. Type 'help' for available commands.", "⚠".yellow());
            },
            None => {},
        }
    }
    
    Ok(())
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("{} Nightly Rust Resource Tracker v1.0.0", "🚀".green());
    
    let cli = Cli::parse();
    
    let mut tracker = if Path::new("resources.json").exists() {
        ResourceTracker::load()?
    } else {
        ResourceTracker::new()
    };
    
    match &cli.command {
        Commands::Add { name, quantity, category } => {
            tracker.add_resource(name.clone(), *quantity, category.clone());
        },
        Commands::List => {
            tracker.list_resources();
        },
        Commands::Update { name, quantity } => {
            match tracker.update_quantity(name.clone(), *quantity) {
                Ok(_) => {},
                Err(e) => println!("{} Error: {}", "✗".red(), e),
            }
        },
        Commands::Remove { name } => {
            match tracker.remove_resource(name.clone()) {
                Ok(_) => {},
                Err(e) => println!("{} Error: {}", "✗".red(), e),
            }
        },
        Commands::Export { format, output } => {
            match format.as_str() {
                "json" => tracker.export_to_json(output)?,
                "csv" => tracker.export_to_csv(output)?,
                _ => println!("{} Unsupported format: {}. Use 'json' or 'csv'.", "⚠".yellow(), format),
            }
        },
        Commands::Interactive => {
            interactive_mode()?;
        },
    }
    
    tracker.save()?;
    
    Ok(())
}
