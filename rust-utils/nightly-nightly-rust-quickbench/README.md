# Nightly Rust QuickBench

A blazing-fast CLI tool for quick Rust microbenchmarking with statistical analysis. Built with Rust for maximum performance and accuracy.

## Features

- **Sub-microsecond precision** - Leverages Rust's high-performance timing capabilities
- **Statistical analysis** - Automatic confidence intervals and outlier detection
- **Multiple benchmark modes** - Iteration-based, time-based, and adaptive sampling
- **Zero dependencies** - Pure Rust with minimal stdlib usage
- **Cross-platform** - Works on Linux, macOS, and Windows

## Installation

```bash
# Clone and build
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/rust-utils/nightly-rust-quickbench
cargo build --release

# Or install directly
cargo install --git https://github.com/polsala/ApocalypsAI.git nightly-rust-quickbench
```

## Usage

### Basic Benchmarking

```bash
# Benchmark a simple function
quickbench --iterations 1000000 'fibonacci(20)'

# Time-based benchmarking
quickbench --time 5s 'sort_vector()'

# Adaptive sampling (automatic iteration count)
quickbench --adaptive 'complex_algorithm()'
```

### Advanced Features

```bash
# Custom warmup period
quickbench --warmup 100ms --iterations 500000 'my_function()'

# Statistical confidence level
quickbench --confidence 99 --iterations 100000 'performance_critical()'

# Output formats
quickbench --format json --iterations 10000 'benchmark()'
quickbench --format markdown --iterations 10000 'benchmark()'
```

### Programmatic Usage

```rust
use quickbench::Benchmark;

fn main() {
    let mut bench = Benchmark::new("fibonacci");
    
    bench.warmup(|| fibonacci(10));
    bench.iterations(100000);
    
    let result = bench.run(|| fibonacci(20));
    
    println!("Average: {:.2} ns", result.average());
    println!("Median: {:.2} ns", result.median());
    println!("Std Dev: {:.2} ns", result.std_dev());
}

fn fibonacci(n: u32) -> u64 {
    match n {
        0 => 0,
        1 => 1,
        _ => fibonacci(n - 1) + fibonacci(n - 2),
    }
}
```

## Command Line Options

- `--iterations N` - Run exactly N iterations
- `--time DURATION` - Run for specified duration (e.g., 1s, 500ms)
- `--adaptive` - Automatically determine iteration count for statistical significance
- `--warmup DURATION` - Warmup period before actual benchmarking
- `--confidence PERCENT` - Confidence level for statistical analysis (95-99)
- `--format FORMAT` - Output format: json, markdown, or table
- `--quiet` - Suppress progress output

## Output Examples

### Table Format (Default)

```
Benchmark: fibonacci(20)
Iterations: 1,000,000
Confidence: 95%

┌─────────────────┬─────────────┬─────────────┬─────────────┐
│ Statistic       │ Value       │ Min         │ Max         │
├─────────────────┼─────────────┼─────────────┼─────────────┤
│ Mean            │ 1,234.56 ns │ 1,230.12 ns │ 1,238.90 ns │
│ Median          │ 1,232.34 ns │ 1,228.90 ns │ 1,236.78 ns │
│ Std Dev         │ 15.67 ns    │ 12.34 ns    │ 18.90 ns    │
│ Outliers        │ 0.23%       │ 0.10%       │ 0.45%       │
└─────────────────┴─────────────┴─────────────┴─────────────┘
```

### JSON Format

```json
{
  "benchmark": "fibonacci(20)",
  "iterations": 1000000,
  "confidence": 95,
  "statistics": {
    "mean": 1234.56,
    "median": 1232.34,
    "std_dev": 15.67,
    "min": 1230.12,
    "max": 1238.90,
    "outliers": 0.23
  },
  "timing": {
    "total": 1234567890,
    "warmup": 100000000,
    "benchmark": 1134567890
  }
}
```

## Performance Characteristics

- **Timing Resolution**: Nanosecond precision using `std::time::Instant`
- **Memory Overhead**: < 1KB per benchmark instance
- **CPU Usage**: Minimal - pure Rust with no runtime overhead
- **Statistical Accuracy**: Uses robust statistical methods for reliable results

## Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests for your changes
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Why Rust?

This tool is built in Rust because:

- **Performance**: Rust's zero-cost abstractions ensure minimal benchmarking overhead
- **Safety**: Memory safety without garbage collection means consistent timing
- **Precision**: Fine-grained control over timing and memory allocation
- **Portability**: Cross-platform support with consistent behavior

For quick, accurate, and reliable microbenchmarks, Rust QuickBench delivers the precision you need.
