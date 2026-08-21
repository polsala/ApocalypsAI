use clap::Parser;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs;
use std::io::{self, Read, Write};
use std::path::PathBuf;

#[derive(Parser, Debug)]
#[clap(author, version, about = "A high-performance CLI tool to validate and mend resource manifests (YAML, JSON, TOML) for consistency and completeness.")]
struct Args {
    /// Path to the resource manifest file (YAML, JSON, or TOML).
    input_file: PathBuf,

    /// Path to write the mended manifest. If not provided, output is printed to stdout.
    #[clap(short, long)]
    output: Option<PathBuf>,

    /// Output format (yaml, json, toml). Defaults to the input file's format if not specified.
    #[clap(short, long, value_parser = ["yaml", "json", "toml"])]
    format: Option<String>,

    /// Enable verbose output, showing detailed mending actions.
    #[clap(short, long)]
    verbose: bool,

    /// Only validate and report errors, do not output a mended file.
    #[clap(long)]
    check_only: bool,
}

#[derive(Debug, Serialize, Deserialize, PartialEq, Clone)]
struct Resource {
    item: String,
    quantity: u32,
    unit: String,
    #[serde(default = "default_status")]
    status: String,
}

fn default_status() -> String {
    "Unknown".to_string()
}

#[derive(Debug, Serialize, Deserialize, PartialEq, Clone)]
struct Manifest {
    cache_id: String,
    location: String,
    last_inspected: String,
    resources: Vec<Resource>,
}

impl Manifest {
    /// Attempts to mend the manifest, returning a new mended manifest and a list of mending actions.
    fn mend(&mut self, verbose: bool) -> Vec<String> {
        let mut mending_actions = Vec::new();

        // Validate and mend last_inspected date format
        if let Err(_) = chrono::DateTime::parse_from_rfc3339(&self.last_inspected) {
            let original = self.last_inspected.clone();
            self.last_inspected = chrono::Utc::now().to_rfc3339();
            mending_actions.push(format!("Mended 'last_inspected' from '{}' to current UTC time due to invalid format.", original));
        }

        for resource in &mut self.resources {
            // Mend unit if missing or generic
            if resource.unit.is_empty() || resource.unit.to_lowercase() == "item" || resource.unit.to_lowercase() == "unit" {
                let inferred_unit = match resource.item.to_lowercase().as_str() {
                    s if s.contains("kit") => "kit",
                    s if s.contains("water") => "liter",
                    s if s.contains("food") || s.contains("ration") => "pack",
                    s if s.contains("battery") => "unit",
                    s if s.contains("ammo") => "round",
                    s if s.contains("fuel") => "gallon",
                    _ => "unit", // Default fallback
                };
                if resource.unit != inferred_unit.to_string() {
                    mending_actions.push(format!("Mended unit for '{}' from '{}' to '{}'.", resource.item, resource.unit, inferred_unit));
                    resource.unit = inferred_unit.to_string();
                }
            }

            // Status is handled by serde default, but we can add more logic here if needed.
            if verbose && resource.status == default_status() {
                mending_actions.push(format!("Defaulted status for '{}' to '{}'.", resource.item, resource.status));
            }
        }
        mending_actions
    }
}

fn parse_manifest<R: Read>(reader: R, format: &str) -> Result<Manifest, String> {
    let content = io::read_to_string(reader).map_err(|e| format!("Failed to read input: {}", e))?;
    match format {
        "yaml" => serde_yaml::from_str(&content).map_err(|e| format!("Failed to parse YAML: {}", e)),
        "json" => serde_json::from_str(&content).map_err(|e| format!("Failed to parse JSON: {}", e)),
        "toml" => toml::from_str(&content).map_err(|e| format!("Failed to parse TOML: {}", e)),
        _ => Err(format!("Unsupported input format: {}", format)),
    }
}

fn serialize_manifest<W: Write>(writer: W, manifest: &Manifest, format: &str) -> Result<(), String> {
    match format {
        "yaml" => serde_yaml::to_writer(writer, manifest).map_err(|e| format!("Failed to serialize to YAML: {}", e)),
        "json" => serde_json::to_writer_pretty(writer, manifest).map_err(|e| format!("Failed to serialize to JSON: {}", e)),
        "toml" => toml::to_string_pretty(manifest).map(|s| write!(writer, "{}", s)).map_err(|e| format!("Failed to serialize to TOML: {}", e)),
        _ => Err(format!("Unsupported output format: {}", format)),
    }
}

fn main() -> Result<(), String> {
    let args = Args::parse();

    let input_path = &args.input_file;
    let input_format = input_path.extension()
                                 .and_then(|s| s.to_str())
                                 .unwrap_or("unknown");

    if !matches!(input_format, "yaml" | "json" | "toml") {
        return Err(format!("Unsupported input file extension: {}. Expected .yaml, .json, or .toml", input_format));
    }

    let file = fs::File::open(input_path).map_err(|e| format!("Failed to open input file '{}': {}", input_path.display(), e))?;
    let mut manifest = parse_manifest(file, input_format)?;

    let mending_actions = manifest.mend(args.verbose);

    if !mending_actions.is_empty() {
        eprintln!("Manifest Mending Report:");
        for action in mending_actions {
            eprintln!("- {}", action);
        }
    }

    if args.check_only {
        eprintln!("\nManifest checked. No output generated due to --check-only flag.");
        return Ok(());
    }

    let output_format = args.format.as_deref().unwrap_or(input_format);

    match args.output {
        Some(output_path) => {
            let file = fs::File::create(&output_path).map_err(|e| format!("Failed to create output file '{}': {}", output_path.display(), e))?;
            serialize_manifest(file, &manifest, output_format)?;
            eprintln!("\nMended manifest written to '{}' in {} format.", output_path.display(), output_format);
        }
        None => {
            serialize_manifest(io::stdout(), &manifest, output_format)?;
            eprintln!("\nMended manifest printed to stdout in {} format.", output_format);
        }
    }

    Ok(())
}
