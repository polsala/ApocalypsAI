Nightly Portal Traffic Simulator

This utility simulates whimsical travelers passing through a portal. It runs a concurrent simulation and provides live statistics via an HTTP endpoint.

Usage:
1. Build and run:
   go run src/main.go
2. Access stats:
   curl http://localhost:8080/stats

The JSON response contains:
- total_travelers
- active_travelers
- average_speed
- average_duration_seconds

Testing:
Run go test ./tests
