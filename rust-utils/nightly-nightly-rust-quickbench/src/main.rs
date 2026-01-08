use std::env;
use std::time::{Duration, Instant};
use std::process;

mod benchmark;
mod stats;
mod output;

use benchmark::Benchmark;
use output::{OutputFormat, Output};

#[derive(Debug)]
struct Args {
    iterations: Option<u64>,
    time_duration: Option<Duration>,
    adaptive: bool,
    warmup: Duration,
    confidence: u8,
    format: OutputFormat,
    quiet: bool,
    code: String,
}

fn parse_args() -> Result<Args, String> {
    let args: Vec<String> = env::args().collect();
    let mut iterations = None;
    let mut time_duration = None;
    let mut adaptive = false;
    let mut warmup = Duration::from_millis(100);
    let mut confidence = 95;
    let mut format = OutputFormat::Table;
    let mut quiet = false;
    let mut code = String::new();
    
    let mut i = 1;
    while i < args.len() {
        match args[i].as_str() {
            "--iterations" => {
                i += 1;
                if i >= args.len() {
                    return Err("--iterations requires a value".to_string());
                }
                iterations = Some(args[i].parse().map_err(|_| "Invalid iterations value")?);
            },
            "--time" => {
                i += 1;
                if i >= args.len() {
                    return Err("--time requires a duration value".to_string());
                }
                time_duration = Some(parse_duration(&args[i])?);
            },
            "--adaptive" => {
                adaptive = true;
            },
            "--warmup" => {
                i += 1;
                if i >= args.len() {
                    return Err("--warmup requires a duration value".to_string());
                }
                warmup = parse_duration(&args[i])?;
            },
            "--confidence" => {
                i += 1;
                if i >= args.len() {
                    return Err("--confidence requires a percentage value".to_string());
                }
                confidence = args[i].parse().map_err(|_| "Invalid confidence value")?;
                if confidence < 90 || confidence > 99 {
                    return Err("Confidence must be between 90 and 99".to_string());
                }
            },
            "--format" => {
                i += 1;
                if i >= args.len() {
                    return Err("--format requires a format type".to_string());
                }
                format = match args[i].as_str() {
                    "json" => OutputFormat::Json,
                    "markdown" => OutputFormat::Markdown,
                    "table" => OutputFormat::Table,
                    _ => return Err("Invalid format: must be json, markdown, or table".to_string()),
                };
            },
            "--quiet" => {
                quiet = true;
            },
            _ => {
                if code.is_empty() {
                    code = args[i].clone();
                } else {
                    return Err(format!("Unknown argument: {}", args[i]));
                }
            },
        }
        i += 1;
    }
    
    if code.is_empty() {
        return Err("No code to benchmark specified".to_string());
    }
    
    if iterations.is_none() && time_duration.is_none() && !adaptive {
        return Err("Must specify one of: --iterations, --time, or --adaptive".to_string());
    }
    
    if iterations.is_some() && time_duration.is_some() {
        return Err("Cannot specify both --iterations and --time".to_string());
    }
    
    if adaptive && (iterations.is_some() || time_duration.is_some()) {
        return Err("Cannot specify --adaptive with --iterations or --time".to_string());
    }
    
    Ok(Args {
        iterations,
        time_duration,
        adaptive,
        warmup,
        confidence,
        format,
        quiet,
        code,
    })
}

fn parse_duration(input: &str) -> Result<Duration, String> {
    if input.ends_with("ms") {
        let value = input.trim_end_matches("ms").parse::<u64>().map_err(|_| "Invalid duration value")?;
        Ok(Duration::from_millis(value))
    } else if input.ends_with("s") {
        let value = input.trim_end_matches("s").parse::<u64>().map_err(|_| "Invalid duration value")?;
        Ok(Duration::from_secs(value))
    } else {
        Err("Duration must end with 'ms' or 's'".to_string())
    }
}

fn main() {
    let args = match parse_args() {
        Ok(args) => args,
        Err(e) => {
            eprintln!("Error: {}", e);
            eprintln!("Usage: quickbench [OPTIONS] <code>");
            eprintln!("  --iterations N     Run exactly N iterations");
            eprintln!("  --time DURATION    Run for specified duration (e.g., 1s, 500ms)");
            eprintln!("  --adaptive         Automatically determine iteration count");
            eprintln!("  --warmup DURATION  Warmup period (default: 100ms)");
            eprintln!("  --confidence PERCENT  Confidence level (90-99, default: 95)");
            eprintln!("  --format FORMAT    Output format: json, markdown, or table");
            eprintln!("  --quiet            Suppress progress output");
            process::exit(1);
        },
    };
    
    if !args.quiet {
        println!("Running benchmark: {}", args.code);
    }
    
    let mut bench = Benchmark::new(&args.code);
    bench.set_warmup(args.warmup);
    bench.set_confidence(args.confidence);
    
    let result = if let Some(iterations) = args.iterations {
        bench.set_iterations(iterations);
        bench.run()
    } else if let Some(duration) = args.time_duration {
        bench.set_time(duration);
        bench.run_time_based()
    } else {
        bench.run_adaptive()
    };
    
    let output = Output::new(args.format);
    output.print(&result);
    
    if !args.quiet {
        println!("\nBenchmark completed successfully!");
    }
}

// Mock implementations for testing
#[cfg(test)]
mod tests {
    use super::*;
    use std::thread;
    
    #[test]
    fn test_parse_duration() {
        assert_eq!(parse_duration("100ms").unwrap(), Duration::from_millis(100));
        assert_eq!(parse_duration("1s").unwrap(), Duration::from_secs(1));
        assert!(parse_duration("invalid").is_err());
    }
    
    #[test]
    fn test_benchmark_functionality() {
        let mut bench = Benchmark::new("test_function");
        bench.set_iterations(100);
        bench.set_warmup(Duration::from_millis(10));
        bench.set_confidence(95);
        
        let result = bench.run_with_function(|| {
            // Simulate some work
            let mut sum = 0;
            for i in 0..1000 {
                sum += i;
            }
            sum
        });
        
        assert!(result.iterations() > 0);
        assert!(result.average() > 0.0);
        assert!(result.median() > 0.0);
    }
    
    #[test]
    fn test_output_formats() {
        let mut bench = Benchmark::new("test");
        bench.set_iterations(10);
        let result = bench.run_with_function(|| 42);
        
        let json_output = Output::new(OutputFormat::Json);
        let markdown_output = Output::new(OutputFormat::Markdown);
        let table_output = Output::new(OutputFormat::Table);
        
        // These should not panic
        json_output.print(&result);
        markdown_output.print(&result);
        table_output.print(&result);
    }
}
