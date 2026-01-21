# nightly-chaos-monkey-shutdown

Simulate graceful service shutdowns to test system resilience.

## Usage

```bash
./src/chaos_shutdown.sh <service_name> [--force]
```

- `service_name`: Name of the systemd service to stop.
- `--force`: (Optional) Forcefully kill the service if it doesn't stop gracefully.

## Example

```bash
./src/chaos_shutdown.sh nginx
```

## Test

Run the test suite:

```bash
bash tests/test_chaos_shutdown.sh
```
