package main

import (
	"fmt"
	"net"
	"os"
	"strconv"
	"time"
)

const (
	defaultPort = 8080
)

// parseBeaconTime parses a time string received from the beacon.
func parseBeaconTime(data []byte) (time.Time, error) {
	return time.Parse(time.RFC3339Nano, string(data))
}

// calculateDrift calculates the time difference between local and beacon time.
func calculateDrift(beaconTime time.Time) time.Duration {
	return time.Since(beaconTime)
}

func main() {
	portStr := os.Getenv("BEACON_PORT")
	port, err := strconv.Atoi(portStr)
	if err != nil || port == 0 {
		port = defaultPort
	}

	// Listen on all available interfaces for the specified UDP port
	addr, err := net.ResolveUDPAddr("udp", fmt.Sprintf(":%d", port))
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error resolving UDP address: %v\n", err)
		os.Exit(1)
	}

	conn, err := net.ListenUDP("udp", addr)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error listening on UDP: %v\n", err)
		os.Exit(1)
	}
	defer conn.Close()

	fmt.Printf("Chrono-Sync Client listening for beacons on UDP port %d...\n", port)

	buffer := make([]byte, 1024)
	for {
		n, _, err := conn.ReadFromUDP(buffer)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Error reading from UDP: %v\n", err)
			continue
		}

		beaconTime, err := parseBeaconTime(buffer[:n])
		if err != nil {
			fmt.Fprintf(os.Stderr, "Error parsing beacon time: %v\n", err)
			continue
		}

		drift := calculateDrift(beaconTime)
		fmt.Printf("Received: %s (Local Drift: %s)\n", beaconTime.Format(time.RFC3339Nano), drift)
	}
}
