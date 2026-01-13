use clap::Parser;
use serde::Serialize;

#[derive(Parser)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Output the palette as JSON instead of a pretty grid
    #[arg(short, long)]
    json: bool,
}

#[derive(Serialize)]
struct ColorEntry {
    code: u8,
    sample: String,
}

fn generate_palette() -> Vec<ColorEntry> {
    (0u8..=255)
        .map(|code| ColorEntry {
            code,
            sample: format!("[38;5;{}mâ[0m", code),
        })
        .collect()
}

fn print_pretty(palette: &[ColorEntry]) {
    const ROW_LEN: usize = 16;
    for (i, entry) in palette.iter().enumerate() {
        print!("{:>3} {} ", entry.code, entry.sample);
        if (i + 1) % ROW_LEN == 0 {
            println!();
        }
    }
}

fn main() {
    let args = Args::parse();
    let palette = generate_palette();
    if args.json {
        // Serialize only the code and sample fields
        let json = serde_json::to_string_pretty(&palette).expect("JSON serialization failed");
        println!("{}", json);
    } else {
        print_pretty(&palette);
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use assert_cmd::Command;
    use predicates::prelude::*;

    #[test]
    fn json_output_has_256_entries() {
        let mut cmd = Command::cargo_bin("ansi-color-palette").unwrap();
        cmd.arg("--json");
        cmd.assert()
            .success()
            .stdout(predicate::str::contains(""code": 0"))
            .stdout(predicate::str::contains(""code": 255"));
    }
}

