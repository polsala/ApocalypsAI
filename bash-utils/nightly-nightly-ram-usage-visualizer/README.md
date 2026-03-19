# nightly-ram-usage-visualizer

A whimsical Bash utility that visualizes RAM usage as a bar graph and adds a motivational quote when memory usage is critically high.

## Usage

```sh
./ramviz.sh            # reads /proc/meminfo
./ramviz.sh /path/to/meminfo   # for testing with a custom meminfo file
```

## Output

Displays the percentage of RAM used and a 20‑character bar. If usage exceeds 80 %, a random motivational quote is printed.

Example:

```
RAM Usage: 42% [██████----------]
```

When usage is high:

```
RAM Usage: 92% [██████████───────]
Stay cool, the memory will recover.
```

## License

MIT
