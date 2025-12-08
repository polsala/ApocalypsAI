# nightly-concurrent-survival-checker

A Go utility that concurrently checks survival resource statuses (water, food, shelter) and delivers whimsical alerts using goroutines. Perfect for post-apocalyptic scenario simulations.

## Usage
```bash
$ go run main.go
# Or with custom resource weights
$ go run main.go --water=80 --food=30 --shelter=95
```
