package main

import (
	"flag"
	"fmt"
	"net"
	"strconv"
	"time"
)

// QueryBeacon sends a request to the beacon server and returns the beacon's estimated time.
// Exported for testing purposes.
func QueryBeacon(serverAddr string) (time.Time, error) {
	conn, err := net.Dial("udp", serverAddr)
	if err != nil {
		return time.Time{}, fmt.Errorf("failed to dial UDP server: %w", err)
	}
	defer conn.Close()

	// Set a deadline for reading to prevent hanging
	conn.SetReadDeadline(time.Now().Add(5 * time.Second))

	// Record request send time
	requestSendTime := time.Now()

	// Send a dummy request (any data will trigger a response from the beacon)
	_, err = conn.Write([]byte("TIME_REQUEST"))
	if err != nil {
		return time.Time{}, fmt.Errorf("failed to send request: %w", err)
	}

	buffer := make([]byte, 1024)
	n, err := conn.Read(buffer)
	if err != nil {
		return time.Time{}, fmt.Errorf("failed to read response: %w", err)
	}

	// Record response receive time
	responseReceiveTime := time.Now()

	beaconTimeNano, err := strconv.ParseInt(string(buffer[:n]), 10, 64)
	if err != nil {
		return time.Time{}, fmt.Errorf("failed to parse beacon time: %w", err)
	}

	// Calculate estimated beacon time at the moment of response
	// This is a simplified NTP-like calculation:
	// client_receive_time = server_send_time + one_way_delay
	// server_send_time = beacon_time_nano
	// one_way_delay = (response_receive_time - request_send_time) / 2 (assuming symmetric delay)
	// So, estimatedBeaconTimeAtClient = beacon_time_nano + (roundTripTime / 2)
	roundTripTime := responseReceiveTime.Sub(requestSendTime)
	estimatedBeaconTimeAtClient := time.Unix(0, beaconTimeNano).Add(roundTripTime / 2)

	return estimatedBeaconTimeAtClient, nil
}

func main() {
	serverAddr := flag.String("server", "localhost:8080", "Address of the Chronosync Beacon server (e.g., localhost:8080)")
	flag.Parse()

	fmt.Printf("Querying Chronosync Beacon at %s...\n", *serverAddr)

	beaconTime, err := QueryBeacon(*serverAddr)
	if err != nil {
		fmt.Printf("Error querying beacon: %v\n", err)
		return
	}

	fmt.Printf("Beacon Time (UTC): %s (Unix Nano: %d)\n", beaconTime.UTC().Format(time.RFC3339Nano), beaconTime.UnixNano())
}
