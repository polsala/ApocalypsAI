package main

import (
	"fmt"
	"log"
	"net"
	"os"
	"strconv"
	"strings"
	"time"

	"flag"
)

const (
	defaultPort          = 8080
	defaultMulticastAddr = "224.0.0.1:9999"
	beaconInterval       = 5 * time.Second
	readBufferSize       = 1024
)

// BeaconMessage represents the time message sent by the beacon
type BeaconMessage struct {
	Timestamp int64 // Unix nanoseconds
	SourceID  string
}

// parseBeaconMessage parses a string into a BeaconMessage
func parseBeaconMessage(data []byte) (BeaconMessage, error) {
	parts := strings.SplitN(string(data), "|", 2)
	if len(parts) != 2 {
		return BeaconMessage{}, fmt.Errorf("invalid message format: %s", string(data))
	}
	timestamp, err := strconv.ParseInt(parts[0], 10, 64)
	if err != nil {
		return BeaconMessage{}, fmt.Errorf("invalid timestamp: %w", err)
	}
	return BeaconMessage{Timestamp: timestamp, SourceID: parts[1]}, nil
}

// formatBeaconMessage formats a BeaconMessage into a string
func formatBeaconMessage(msg BeaconMessage) []byte {
	return []byte(fmt.Sprintf("%d|%s", msg.Timestamp, msg.SourceID))
}

// Variables to allow mocking net functions in tests
var (
	netListenUDP         = net.ListenUDP
	netListenMulticastUDP = net.ListenMulticastUDP
	netResolveUDPAddr    = net.ResolveUDPAddr
)

// runBeaconServer starts the time beacon server
func runBeaconServer(port int, multicastAddr string) {
	addr, err := netResolveUDPAddr("udp", multicastAddr)
	if err != nil {
		log.Fatalf("Failed to resolve multicast address: %v", err)
	}

	conn, err := netListenUDP("udp", &net.UDPAddr{Port: port})
	if err != nil {
		log.Fatalf("Failed to listen on UDP port %d: %v", port, err)
	}
	defer conn.Close()

	log.Printf("Chrono-Sync Beacon (Server) active on port %d, broadcasting to %s", port, multicastAddr)

	hostname, _ := os.Hostname()
	if hostname == "" {
		hostname = "unknown-beacon"
	}

	ticker := time.NewTicker(beaconInterval)
	defer ticker.Stop()

	for range ticker.C {
		now := time.Now().UnixNano()
		msg := BeaconMessage{Timestamp: now, SourceID: hostname}
		data := formatBeaconMessage(msg)

		_, err := conn.WriteToUDP(data, addr)
		if err != nil {
			log.Printf("Error broadcasting temporal pulse: %v", err)
		} else {
			log.Printf("Broadcasted temporal pulse from %s: %s", hostname, time.UnixNano(now).Format(time.RFC3339Nano))
		}
	}
}

// runAttunerClient starts the time attuner client
func runAttunerClient(port int, multicastAddr string) {
	addr, err := netResolveUDPAddr("udp", multicastAddr)
	if err != nil {
		log.Fatalf("Failed to resolve multicast address: %v", err)
	}

	conn, err := netListenMulticastUDP("udp", nil, addr)
	if err != nil {
		log.Fatalf("Failed to listen on multicast address %s: %v", multicastAddr, err)
	}
	defer conn.Close()

	conn.SetReadBuffer(readBufferSize)

	log.Printf("Chrono-Sync Attuner (Client) active, listening on %s", multicastAddr)

	buf := make([]byte, readBufferSize)
	for {
		n, src, err := conn.ReadFromUDP(buf)
		if err != nil {
			if opErr, ok := err.(*net.OpError); ok && opErr.Err.Error() == "use of closed network connection" {
				log.Printf("Attuner connection closed, exiting.")
				return // Exit gracefully if connection is closed
			}
			log.Printf("Error reading from UDP: %v", err)
			continue
		}

		receivedTime := time.Now() // Capture local time immediately upon reception
		msg, err := parseBeaconMessage(buf[:n])
		if err != nil {
			log.Printf("Error parsing beacon message from %s: %v", src, err)
			continue
		}

		beaconTime := time.UnixNano(msg.Timestamp)
		offset := receivedTime.Sub(beaconTime)

		log.Printf("Received temporal pulse from %s (%s). Local time: %s, Beacon time: %s. Temporal Drift: %s",
			msg.SourceID, src, receivedTime.Format(time.RFC3339Nano), beaconTime.Format(time.RFC3339Nano), offset)
	}
}

func main() {
	mode := flag.String("mode", "client", "Operation mode: 'server' (beacon) or 'client' (attuner)")
	port := flag.Int("port", defaultPort, "UDP port to listen/send on")
	multicast := flag.String("multicast", defaultMulticastAddr, "Multicast address and port (e.g., 224.0.0.1:9999)")
	flag.Parse()

	if *mode == "server" {
		runBeaconServer(*port, *multicast)
	} else if *mode == "client" {
		runAttunerClient(*port, *multicast)
	} else {
		fmt.Fprintf(os.Stderr, "Invalid mode: %s. Use 'server' or 'client'.\n", *mode)
		flag.Usage()
		os.Exit(1)
	}
}
