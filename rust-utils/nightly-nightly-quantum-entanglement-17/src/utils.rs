use std::fs;
use std::io;

pub fn read_file(path: &str) -> Result<String, io::Error> {
    fs::read_to_string(path)
}

pub fn show_usage() {
    println!("\n{} Quantum Entanglement Checker", "Usage:".bold().underline());
    println!("{} check <file1> <file2>          {} Check if two files are quantumly entangled", "  ".bright_cyan(), "🔬".cyan());
    println!("{} check-inline <code1> <code2>   {} Check inline code snippets", "  ".bright_cyan(), "🔬".cyan());
    println!("{} report <file1> <file2>         {} Generate detailed quantum report", "  ".bright_cyan(), "📊".cyan());
    println!("\n{} Examples:", "Examples:".bold().underline());
    println!("{} cargo run -- check src/main.rs src/lib.rs", "  ".bright_cyan());
    println!("{} cargo run -- check-inline \"fn main() {{}}\" \"fn test() {{}}\"", "  ".bright_cyan());
    println!("{} cargo run -- report src/main.rs src/lib.rs", "  ".bright_cyan());
}

pub fn show_banner() {
    println!("{}
{}  Quantum Entanglement Checker
{}  by ApocalypsAI
{}
", "=".repeat(60).bright_magenta(), "=".repeat(20).bright_cyan(), "=".repeat(15).bright_cyan(), "=".repeat(60).bright_magenta());
}
