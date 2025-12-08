use clap::{Parser, Subcommand};
use rusqlite::{params, Connection, Result};
use serde::{Deserialize, Serialize};
use std::path::Path;
use std::time::{SystemTime, UNIX_EPOCH};
use std::fs;
use std::io::Write;
use chrono::{NaiveDate, Utc};
use colored::*;

mod database;
mod commands;
mod config;
mod export;

use commands::*;
use config::Config;

#[derive(Parser)]
#[command(author, version, about, long_about = None)]
#[command(propagate_version = true)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Initialize a new resource database
    Init,
    /// Add a new resource
    Add {
        #[arg(short, long)]
        name: String,
        #[arg(short, long)]
        quantity: i32,
        #[arg(short, long)]
        category: String,
        #[arg(short, long)]
        expires: Option<String>,
        #[arg(short, long)]
        location: Option<String>,
    },
    /// List all resources
    List,
    /// Update resource quantity
    Update {
        #[arg(short, long)]
        name: String,
        #[arg(short, long)]
        quantity: Option<i32>,
        #[arg(short, long)]
        location: Option<String>,
    },
    /// Remove a resource
    Remove {
        #[arg(short, long)]
        name: String,
    },
    /// Check for expired items
    CheckExpired,
    /// Generate survival report
    Report {
        #[arg(short, long, default_value = "30")]
        days: i64,
    },
    /// Export data to various formats
    Export {
        #[arg(short, long)]
        format: String,
        #[arg(short, long)]
        output: String,
    },
    /// Backup database
    Backup {
        #[arg(short, long)]
        path: String,
    },
}

#[derive(Debug, Clone)]
struct Resource {
    id: i32,
    name: String,
    quantity: i32,
    category: String,
    expires: Option<String>,
    location: Option<String>,
    created_at: String,
    updated_at: String,
}

impl Resource {
    fn new(name: String, quantity: i32, category: String, expires: Option<String>, location: Option<String>) -> Self {
        let now = Utc::now().to_rfc3339();
        Resource {
            id: 0,
            name,
            quantity,
            category,
            expires,
            location,
            created_at: now.clone(),
            updated_at: now,
        }
    }
}

fn main() {
    let cli = Cli::parse();
    
    match &cli.command {
        Commands::Init => {
            println!("{} Initializing resource tracker database...", "[INFO]".green());
            if let Err(e) = database::init_database() {
                eprintln!("{} Failed to initialize database: {}", "[ERROR]".red(), e);
                std::process::exit(1);
            }
            println!("{} Database initialized successfully!", "[SUCCESS]".green());
        }
        Commands::Add { name, quantity, category, expires, location } => {
            if let Err(e) = add_resource(name, *quantity, category, expires.clone(), location.clone()) {
                eprintln!("{} Failed to add resource: {}", "[ERROR]".red(), e);
                std::process::exit(1);
            }
            println!("{} Resource added successfully!", "[SUCCESS]".green());
        }
        Commands::List => {
            if let Err(e) = list_resources() {
                eprintln!("{} Failed to list resources: {}", "[ERROR]".red(), e);
                std::process::exit(1);
            }
        }
        Commands::Update { name, quantity, location } => {
            if let Err(e) = update_resource(name, quantity, location) {
                eprintln!("{} Failed to update resource: {}", "[ERROR]".red(), e);
                std::process::exit(1);
            }
            println!("{} Resource updated successfully!", "[SUCCESS]".green());
        }
        Commands::Remove { name } => {
            if let Err(e) = remove_resource(name) {
                eprintln!("{} Failed to remove resource: {}", "[ERROR]".red(), e);
                std::process::exit(1);
            }
            println!("{} Resource removed successfully!", "[SUCCESS]".green());
        }
        Commands::CheckExpired => {
            if let Err(e) = check_expired() {
                eprintln!("{} Failed to check expired items: {}", "[ERROR]".red(), e);
                std::process::exit(1);
            }
        }
        Commands::Report { days } => {
            if let Err(e) = generate_report(*days) {
                eprintln!("{} Failed to generate report: {}", "[ERROR]".red(), e);
                std::process::exit(1);
            }
        }
        Commands::Export { format, output } => {
            if let Err(e) = export_data(format, output) {
                eprintln!("{} Failed to export data: {}", "[ERROR]".red(), e);
                std::process::exit(1);
            }
            println!("{} Data exported successfully to {}!", "[SUCCESS]".green(), output);
        }
        Commands::Backup { path } => {
            if let Err(e) = backup_database(path) {
                eprintln!("{} Failed to backup database: {}", "[ERROR]".red(), e);
                std::process::exit(1);
            }
            println!("{} Database backed up successfully!", "[SUCCESS]".green());
        }
    }
}

fn add_resource(name: &str, quantity: i32, category: &str, expires: Option<String>, location: Option<String>) -> Result<()> {
    let conn = database::connect()?;
    let resource = Resource::new(name.to_string(), quantity, category.to_string(), expires, location);
    
    conn.execute(
        "INSERT INTO resources (name, quantity, category, expires, location, created_at, updated_at) 
         VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7)",
        params![
            resource.name,
            resource.quantity,
            resource.category,
            resource.expires,
            resource.location,
            resource.created_at,
            resource.updated_at,
        ],
    )?;
    
    Ok(())
}

fn list_resources() -> Result<()> {
    let conn = database::connect()?;
    let mut stmt = conn.prepare("SELECT id, name, quantity, category, expires, location, created_at, updated_at FROM resources ORDER BY name")?;
    
    let resource_iter = stmt.query_map([], |row| {
        Ok(Resource {
            id: row.get(0)?,
            name: row.get(1)?,
            quantity: row.get(2)?,
            category: row.get(3)?,
            expires: row.get(4)?,
            location: row.get(5)?,
            created_at: row.get(6)?,
            updated_at: row.get(7)?,
        })
    })?;
    
    println!("\n{} Current Resources:", "[INFO]".cyan().bold());
    println!("{}", "─".repeat(80).cyan());
    
    for resource in resource_iter {
        let r = resource?;
        let status = if r.quantity <= 5 {
            "LOW".red().bold()
        } else if r.expires.is_some() {
            let expiry_date = NaiveDate::parse_from_str(&r.expires.clone().unwrap(), "%Y-%m-%d").unwrap();
            let today = Utc::now().date_naive();
            if expiry_date < today {
                "EXPIRED".red().bold()
            } else if (expiry_date - today).num_days() <= 7 {
                "NEAR EXPIRY".yellow().bold()
            } else {
                "OK".green().bold()
            }
        } else {
            "OK".green().bold()
        };
        
        println!("{} | {} | Qty: {} | Cat: {} | Loc: {} | Exp: {}",
            status,
            r.name.cyan(),
            r.quantity.to_string().yellow(),
            r.category.blue(),
            r.location.clone().unwrap_or("Unknown".to_string()).magenta(),
            r.expires.clone().unwrap_or("N/A".to_string()).red()
        );
    }
    
    Ok(())
}

fn update_resource(name: &str, quantity: &Option<i32>, location: &Option<String>) -> Result<()> {
    let conn = database::connect()?;
    let now = Utc::now().to_rfc3339();
    
    if let Some(qty) = quantity {
        conn.execute(
            "UPDATE resources SET quantity = ?1, updated_at = ?2 WHERE name = ?3",
            params![qty, now, name],
        )?;
    }
    
    if let Some(loc) = location {
        conn.execute(
            "UPDATE resources SET location = ?1, updated_at = ?2 WHERE name = ?3",
            params![loc, now, name],
        )?;
    }
    
    Ok(())
}

fn remove_resource(name: &str) -> Result<()> {
    let conn = database::connect()?;
    conn.execute("DELETE FROM resources WHERE name = ?1", params![name])?;
    Ok(())
}

fn check_expired() -> Result<()> {
    let conn = database::connect()?;
    let today = Utc::now().date_naive().format("%Y-%m-%d").to_string();
    
    let mut stmt = conn.prepare(
        "SELECT name, expires FROM resources WHERE expires IS NOT NULL AND expires < ?1"
    )?;
    
    let expired_iter = stmt.query_map(params![today], |row| {
        Ok((row.get::<_, String>(0)?, row.get::<_, String>(1)?))
    })?;
    
    println!("\n{} Expired Items:", "[WARNING]".red().bold());
    println!("{}", "─".repeat(40).red());
    
    let mut found = false;
    for item in expired_iter {
        let (name, expiry) = item?;
        println!("{} - Expired: {}", name.red().bold(), expiry.red());
        found = true;
    }
    
    if !found {
        println!("{} No expired items found!", "[SUCCESS]".green());
    }
    
    Ok(())
}

fn generate_report(days: i64) -> Result<()> {
    let conn = database::connect()?;
    let cutoff_date = Utc::now().date_naive() + chrono::Duration::days(days);
    let cutoff_str = cutoff_date.format("%Y-%m-%d").to_string();
    
    println!("\n{} Survival Report (Next {} days):", "[INFO]".cyan().bold(), days);
    println!("{}", "─".repeat(60).cyan());
    
    // Low quantity items
    let mut stmt = conn.prepare("SELECT name, quantity FROM resources WHERE quantity <= 5")?;
    let low_items = stmt.query_map([], |row| {
        Ok((row.get::<_, String>(0)?, row.get::<_, i32>(1)?))
    })?;
    
    println!("\n{} Low Quantity Items:", "[WARNING]".yellow().bold());
    for item in low_items {
        let (name, qty) = item?;
        println!("  - {} ({} remaining)", name.yellow(), qty.to_string().red());
    }
    
    // Items expiring soon
    let mut stmt = conn.prepare(
        "SELECT name, expires FROM resources WHERE expires IS NOT NULL AND expires <= ?1"
    )?;
    let expiring_items = stmt.query_map(params![cutoff_str], |row| {
        Ok((row.get::<_, String>(0)?, row.get::<_, String>(1)?))
    })?;
    
    println!("\n{} Items Expiring Soon:", "[WARNING]".red().bold());
    for item in expiring_items {
        let (name, expiry) = item?;
        println!("  - {} (expires: {})", name.red(), expiry.red());
    }
    
    // Category summary
    let mut stmt = conn.prepare(
        "SELECT category, SUM(quantity) FROM resources GROUP BY category"
    )?;
    let category_summary = stmt.query_map([], |row| {
        Ok((row.get::<_, String>(0)?, row.get::<_, i32>(1)?))
    })?;
    
    println!("\n{} Category Summary:", "[INFO]".cyan().bold());
    for item in category_summary {
        let (category, total) = item?;
        println!("  - {}: {} items", category.blue(), total.to_string().yellow());
    }
    
    Ok(())
}

fn export_data(format: &str, output: &str) -> Result<()> {
    let conn = database::connect()?;
    let mut stmt = conn.prepare("SELECT id, name, quantity, category, expires, location, created_at, updated_at FROM resources")?;
    
    let resources: Vec<Resource> = stmt.query_map([], |row| {
        Ok(Resource {
            id: row.get(0)?,
            name: row.get(1)?,
            quantity: row.get(2)?,
            category: row.get(3)?,
            expires: row.get(4)?,
            location: row.get(5)?,
            created_at: row.get(6)?,
            updated_at: row.get(7)?,
        })
    })?.map(|r| r.unwrap()).collect();
    
    match format.to_lowercase().as_str() {
        "json" => export::to_json(&resources, output)?,
        "csv" => export::to_csv(&resources, output)?,
        "yaml" => export::to_yaml(&resources, output)?,
        _ => return Err(rusqlite::Error::InvalidQuery),
    }
    
    Ok(())
}

fn backup_database(path: &str) -> Result<()> {
    let conn = database::connect()?;
    let db_path = database::get_db_path();
    
    if let Some(parent) = Path::new(path).parent() {
        fs::create_dir_all(parent)?;
    }
    
    fs::copy(db_path, path)?;
    Ok(())
}

trait Display {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
}

impl Display for Resource {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "Resource {{ id: {}, name: {}, quantity: {}, category: {}, expires: {:?}, location: {:?} }}",
            self.id, self.name, self.quantity, self.category, self.expires, self.location)
    }
}
