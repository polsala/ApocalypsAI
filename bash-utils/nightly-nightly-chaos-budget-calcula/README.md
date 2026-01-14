# nightly-chaos-budget-calculator

A Bash utility to calculate your daily chaos budget for post-apocalyptic survival scenarios.

## Usage

```bash
./chaos_budget.sh [OPTIONS]
```

### Options

- `-h`, `--help`: Show help message
- `-s`, `--survival-level`: Set survival level (1-10)
- `-r`, `--resources`: Available resources (default: 100)
- `-d`, `--days`: Number of days to plan for (default: 7)

## Examples

```bash
# Calculate chaos budget with default settings
./chaos_budget.sh

# Calculate chaos budget for high survival level
./chaos_budget.sh -s 8 -r 200 -d 14
```

## License

MIT
