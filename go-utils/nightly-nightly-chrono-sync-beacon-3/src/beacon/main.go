package main

import (
	"fmt"
	"net"
	"os"
	"strconv"
	"time"
)

const (
	defaultPort     = 8080
	defaultInterval = 1 * time.Second
)

// formatTime returns the given time formatted as RFC3339Nano.
func formatTime(t time.Time) string {
	return t.UTC().Format(time.RFC3339Nano)
}

// sendBeacon writes the given time string to the provided network connection.
func sendBeacon(conn net.Conn, timeStr string) error {
	_, err := conn.Write([]byte(timeStr))
	return err
}

func main() {
	portStr := os.Getenv("BEACON_PORT")
	port, err := strconv.Atoi(portStr)
	if err != nil || port == 0 {
		port = defaultPort
	}

	intervalStr := os.Getenv("BEACON_INTERVAL_SECONDS")
	intervalSeconds, err := strconv.Atoi(intervalStr)
	if err != nil || intervalSeconds == 0 {
		intervalSeconds = int(defaultInterval.Seconds())
	}
	interval := time.Duration(intervalSeconds) * time.Second

	targetAddrStr := os.Getenv("BEACON_TARGET_ADDR")
	if targetAddrStr == "" {
		targetAddrStr = fmt.Sprintf("127.0.0.1:%d", port) // Default to localhost for local testing
	} else {
		targetAddrStr = fmt.Sprintf("%s:%d", targetAddrStr, port)
	}

	targetAddr, err := net.ResolveUDPAddr("udp", targetAddrStr)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error resolving target UDP address: %v\n", err)
		os.Exit(1)
	}

	conn, err := net.DialUDP("udp", nil, targetAddr)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error dialing UDP: %v\n", err)
		os.Exit(1)
	}
	defer conn.Close()

	fmt.Printf("Chrono-Sync Beacon broadcasting to %s every %s...\n", targetAddr, interval)

	for {
		timeStr := formatTime(time.Now())
		err := sendBeacon(conn, timeStr)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Error sending beacon: %v\n", err)
		} else {
			fmt.Printf("Broadcasted: %s\n", timeStr)
		}
		time.Sleep(interval)
	}
}
