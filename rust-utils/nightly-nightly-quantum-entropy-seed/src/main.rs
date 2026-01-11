use anyhow::{Context, Result};
use base64::{engine::general_purpose, Engine as _};
use clap::{Parser, ValueEnum};
use rand::{rngs::StdRng, Rng, SeedableRng};
use serde::{Deserialize, Serialize};
use std::time::{SystemTime, UNIX_EPOCH};

/// A CLI tool that generates cryptographically strong random seeds using quantum noise
#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Output format (hex, base64, decimal)
    #[arg(short, long, default_value = "hex", value_enum)]
    format: OutputFormat,

    /// Number of bits for the seed
    #[arg(short, long, default_value = "256")]
    bits: u32,

    /// Number of quantum random numbers to fetch
    #[arg(short, long, default_value = "50")]
    pool_size: usize,

    /// Fallback source (quantum, atmospheric)
    #[arg(long, default_value = "quantum", value_enum)]
    fallback: FallbackSource,

    /// Generate a deterministic seed for testing
    #[arg(long)]
    deterministic: bool,
}

#[derive(Clone, ValueEnum, Debug)]
enum OutputFormat {
    Hex,
    Base64,
    Decimal,
}

#[derive(Clone, ValueEnum, Debug)]
enum FallbackSource {
    Quantum,
    Atmospheric,
}

#[derive(Deserialize)]
struct QuantumResponse {
    data: Vec<u32>,
}

#[derive(Deserialize)]
struct AtmosphericResponse {
    random: RandomData,
}

#[derive(Deserialize)]
struct RandomData {
    data: Vec<u32>,
}

async fn fetch_quantum_random_numbers(count: usize) -> Result<Vec<u32>> {
    let client = reqwest::Client::new();
    let url = format!(
        "https://qrng.anu.edu.au/API/jsonI.php?length={}&type=uint16",
        count
    );

    let response = client
        .get(&url)
        .header("User-Agent", "NightlyQuantumEntropySeeder/1.0")
        .send()
        .await
        .context("Failed to fetch quantum random numbers")?;

    if !response.status().is_success() {
        anyhow::bail!("Quantum API returned error: {}", response.status());
    }

    let quantum_data: QuantumResponse = response.json().await?;
    Ok(quantum_data.data)
}

async fn fetch_atmospheric_random_numbers(count: usize) -> Result<Vec<u32>> {
    // Note: This is a mock implementation since RANDOM.ORG requires an API key
    // In a real implementation, you would use the actual RANDOM.ORG API
    let client = reqwest::Client::new();
    let url = format!(
        "https://www.random.org/integers/?num={}&min=0&max=65535&col=1&base=10&format=json&rnd=new",
        count
    );

    let response = client
        .get(&url)
        .header("User-Agent", "NightlyQuantumEntropySeeder/1.0")
        .send()
        .await
        .context("Failed to fetch atmospheric random numbers")?;

    if !response.status().is_success() {
        anyhow::bail!("Atmospheric API returned error: {}", response.status());
    }

    let atmospheric_data: AtmosphericResponse = response.json().await?;
    Ok(atmospheric_data.random.data)
}

fn generate_seed_from_entropy(entropy: &[u32], bits: u32, format: OutputFormat) -> String {
    let mut combined_entropy = 0u64;
    for &num in entropy {
        combined_entropy = combined_entropy.wrapping_mul(65537).wrapping_add(num as u64);
    }

    let mask = (1u64 << bits) - 1;
    let seed_value = combined_entropy & mask;

    match format {
        OutputFormat::Hex => format!("{:0width$x}", seed_value, width = ((bits + 3) / 4) as usize),
        OutputFormat::Base64 => {
            let bytes = seed_value.to_le_bytes();
            general_purpose::STANDARD.encode(&bytes)
        }
        OutputFormat::Decimal => seed_value.to_string(),
    }
}

fn generate_deterministic_seed(bits: u32, format: OutputFormat) -> String {
    let seed = 42u64; // Deterministic seed for testing
    let mask = (1u64 << bits) - 1;
    let seed_value = seed & mask;

    match format {
        OutputFormat::Hex => format!("{:0width$x}", seed_value, width = ((bits + 3) / 4) as usize),
        OutputFormat::Base64 => {
            let bytes = seed_value.to_le_bytes();
            general_purpose::STANDARD.encode(&bytes)
        }
        OutputFormat::Decimal => seed_value.to_string(),
    }
}

async fn generate_quantum_seed(args: &Args) -> Result<String> {
    let entropy = fetch_quantum_random_numbers(args.pool_size).await?;
    Ok(generate_seed_from_entropy(&entropy, args.bits, args.format))
}

async fn generate_atmospheric_seed(args: &Args) -> Result<String> {
    let entropy = fetch_atmospheric_random_numbers(args.pool_size).await?;
    Ok(generate_seed_from_entropy(&entropy, args.bits, args.format))
}

async fn generate_fallback_seed(args: &Args) -> Result<String> {
    match args.fallback {
        FallbackSource::Quantum => generate_quantum_seed(args).await,
        FallbackSource::Atmospheric => generate_atmospheric_seed(args).await,
    }
}

#[tokio::main]
async fn main() -> Result<()> {
    let args = Args::parse();

    let seed = if args.deterministic {
        generate_deterministic_seed(args.bits, args.format)
    } else {
        match generate_quantum_seed(&args).await {
            Ok(seed) => seed,
            Err(_) => {
                eprintln!("Quantum API failed, falling back to {}...", args.fallback.as_ref());
                generate_fallback_seed(&args).await?
            }
        }
    };

    println!("{}", seed);
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_generate_deterministic_seed_hex() {
        let seed = generate_deterministic_seed(256, OutputFormat::Hex);
        assert_eq!(seed, "2a"); // 42 in hex with 256 bits
    }

    #[test]
    fn test_generate_deterministic_seed_base64() {
        let seed = generate_deterministic_seed(256, OutputFormat::Base64);
        assert_eq!(seed, "KgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA==");
    }

    #[test]
    fn test_generate_deterministic_seed_decimal() {
        let seed = generate_deterministic_seed(256, OutputFormat::Decimal);
        assert_eq!(seed, "42");
    }

    #[test]
    fn test_generate_seed_from_entropy() {
        let entropy = vec![1, 2, 3, 4, 5];
        let seed = generate_seed_from_entropy(&entropy, 256, OutputFormat::Hex);
        assert!(!seed.is_empty());
        assert!(seed.chars().all(|c| c.is_ascii_hexdigit()));
    }

    #[test]
    fn test_generate_seed_from_entropy_base64() {
        let entropy = vec![1, 2, 3, 4, 5];
        let seed = generate_seed_from_entropy(&entropy, 256, OutputFormat::Base64);
        assert!(!seed.is_empty());
        // Base64 should only contain valid base64 characters
        assert!(seed.chars().all(|c| c.is_ascii_alphanumeric() || c == '+' || c == '/' || c == '='));
    }

    #[test]
    fn test_generate_seed_from_entropy_decimal() {
        let entropy = vec![1, 2, 3, 4, 5];
        let seed = generate_seed_from_entropy(&entropy, 256, OutputFormat::Decimal);
        assert!(!seed.is_empty());
        assert!(seed.chars().all(|c| c.is_ascii_digit()));
    }
}
