use clap::{Arg, Command};
use colored::*;
use std::fs::File;
use std::io::{self, BufRead, BufReader};
use std::path::Path;

#[derive(Debug, PartialEq)]
enum LogLevel {
    Error,
    Warn,
    Info,
    Debug,
}

impl LogLevel {
    fn from_str(s: &str) -> Option<LogLevel> {
        match s.to_uppercase().as_str() {
            "ERROR" => Some(LogLevel::Error),
            "WARN" => Some(LogLevel::Warn),
            "INFO" => Some(LogLevel::Info),
            "DEBUG" => Some(LogLevel::Debug),
            _ => None,
        }
    }

    fn matches(&self, filter: &Option<LogLevel>) -> bool {
        match filter {
            None => true,
            Some(level) => match (self, level) {
                (LogLevel::Error, LogLevel::Error) => true,
                (LogLevel::Warn, LogLevel::Error) => false,
                (LogLevel::Warn, _) => true,
                (LogLevel::Info, LogLevel::Error) | (LogLevel::Info, LogLevel::Warn) => false,
                (LogLevel::Info, _) => true,
                (LogLevel::Debug, LogLevel::Debug) => true,
                _ => false,
            },
        }
    }
}

fn read_logs_from_file(path: &str, filter: &Option<LogLevel>) -> io::Result<()> {
    let file = File::open(path)?;
    let reader = BufReader::new(file);
    for line in reader.lines() {
        let line = line?;
        process_line(&line, filter);
    }
    Ok(())
}

fn read_logs_from_stdin(filter: &Option<LogLevel>) {
    let stdin = io::stdin();
    let reader = stdin.lock();
    for line in reader.lines() {
        let line = line.unwrap();
        process_line(&line, filter);
    }
}

fn process_line(line: &str, filter: &Option<LogLevel>) {
    let level = if line.contains("ERROR") {
        LogLevel::Error
    } else if line.contains("WARN") {
        LogLevel::Warn
    } else if line.contains("INFO") {
        LogLevel::Info
    } else {
        LogLevel::Debug
    };

    if level.matches(filter) {
        let colored_line = match level {
            LogLevel::Error => line.red(),
            LogLevel::Warn => line.yellow(),
            LogLevel::Info => line.blue(),
            LogLevel::Debug => line.green(),
        };
        println!("{}", colored_line);
    }
}

fn main() {
    let matches = Command::new("Void Siphon Log Aggregator")
        .version("1.0")
        .author("ApocalypsAI")
        .about("Aggregates and colorizes logs from multiple sources")
        .arg(
            Arg::new("level")
                .short('l')
                .long("level")
                .value_name("LEVEL")
                .help("Filter logs by level (ERROR, WARN, INFO, DEBUG)"),
        )
        .arg(
            Arg::new("files")
                .help("Log files to aggregate")
                .multiple_values(true),
        )
        .get_matches();

    let filter_level = matches.value_of("level").and_then(LogLevel::from_str);

    if let Some(files) = matches.values_of("files") {
        for file in files {
            if let Err(e) = read_logs_from_file(file, &filter_level) {
                eprintln!("Failed to read {}: {}", file, e);
            }
        }
    } else {
        read_logs_from_stdin(&filter_level);
    }
}
