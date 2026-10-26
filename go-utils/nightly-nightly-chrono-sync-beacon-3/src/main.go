package main

import (
	"errors"
	"flag"
	"fmt"
	"log"
	"net"
	"os"
	"strconv"
	"strings"
	"sync"
	"time"
)

const ( 
	defaultPort     = 8080
	defaultInterval = 1 * time.Second
	bufferSize      = 1024
)

// UDPConn is an interface for UDP network operations, allowing for mocking in tests.
type UDPConn interface {
	WriteToUDP(b []byte, addr *net.UDPAddr) (int, error)
	ReadFromUDP(b []byte) (int, *net.UDPAddr, error)
	Close() error
}

// realUDPConn is a wrapper for *net.UDPConn to implement the UDPConn interface.
type realUDPConn struct {
	*net.UDPConn
}

func (r *realUDPConn) WriteToUDP(b []byte, addr *net.UDPAddr) (int, error) {
	return r.UDPConn.WriteToUDP(b, addr)
}

func (r *realUDPConn) ReadFromUDP(b []byte) (int, *net.UDPAddr, error) {
	return r.UDPConn.ReadFromUDP(b)
}

// beaconMessage represents the data sent in a beacon.
type beaconMessage struct {
	SenderID  string
	Timestamp int64 // Unix nanoseconds
}

// formatBeaconMessage converts a beaconMessage to a string for UDP transmission.
func formatBeaconMessage(msg beaconMessage) string {
	return fmt.Sprintf("%s:%d", msg.SenderID, msg.Timestamp)
}

// parseBeaconMessage parses a string into a beaconMessage.
func parseBeaconMessage(data string) (beaconMessage, error) {
	parts := strings.SplitN(data, ":", 2)
	if len(parts) != 2 {
		return beaconMessage{}, fmt.Errorf("invalid beacon format: %s", data)
	}

	senderID := parts[0]
	timestamp, err := strconv.ParseInt(parts[1], 10, 64)
	if err != nil {
		return beaconMessage{}, fmt.Errorf("invalid timestamp in beacon: %w", err)
	}

	return beaconMessage{SenderID: senderID, Timestamp: timestamp}, nil
}

// calculateDrift calculates the time difference between the sender's timestamp and the receiver's local time.
// A positive duration means the sender's clock is ahead of the receiver's.
// A negative duration means the sender's clock is behind the receiver's.
func calculateDrift(senderTimestamp int64, receiveLocalTime time.Time) time.Duration {
	senderTime := time.Unix(0, senderTimestamp)
	return senderTime.Sub(receiveLocalTime)
}

// runEmitter starts the beacon emitter.
func runEmitter(id string, port int, interval time.Duration, address string, conn UDPConn) {
	log.Printf("Starting Chrono-Sync Beacon Emitter (ID: %s) on %s:%d, interval: %s", id, address, port, interval)

	remoteAddr, err := net.ResolveUDPAddr("udp", fmt.Sprintf("%s:%d", address, port))
	if err != nil {
		log.Fatalf("Failed to resolve remote address: %v", err)
	}

	ticker := time.NewTicker(interval)
	defer ticker.Stop()

	for range ticker.C {
		msg := beaconMessage{
			SenderID:  id,
			Timestamp: time.Now().UnixNano(),
		}
		data := formatBeaconMessage(msg)

		_, err := conn.WriteToUDP([]byte(data), remoteAddr)
		if err != nil {
			log.Printf("Error sending beacon: %v", err)
		} else {
			// log.Printf("Sent beacon: %s", data) // Too verbose for default
		}
	}
}

// runListener starts the beacon listener.
func runListener(port int, address string, conn UDPConn) {
	log.Printf("Starting Chrono-Sync Beacon Listener on %s:%d", address, port)

	buffer := make([]byte, bufferSize)
	for {
		n, senderAddr, err := conn.ReadFromUDP(buffer)
		if err != nil {
			log.Printf("Error reading from UDP: %v", err)
			continue
		}

		receiveLocalTime := time.Now()
		beaconData := string(buffer[:n])

		msg, err := parseBeaconMessage(beaconData)
		if err != nil {
			log.Printf("Error parsing beacon from %s: %v", senderAddr, err)
			continue
		}

		drift := calculateDrift(msg.Timestamp, receiveLocalTime)
		log.Printf("[%s] Received beacon from %s (%s). Drift: %s",
			receiveLocalTime.Format("2006-01-02 15:04:05.000000000"),
			msg.SenderID,
			senderAddr,
			drift,
		)
	}
}

func main() {
	log.SetOutput(os.Stdout)
	log.SetFlags(0) // No default timestamp from log package

	// Common flags
	port := flag.Int("port", defaultPort, "UDP port to use")
	address := flag.String("address", "0.0.0.0", "IP address to bind/send to (e.g., 0.0.0.0 for listen, 239.0.0.1 for multicast, 127.0.0.1 for unicast)")

	// Emitter specific flags
	emitCmd := flag.NewFlagSet("emit", flag.ExitOnError)
	emitID := emitCmd.String("id", "", "Unique identifier for this beacon emitter")
	emitInterval := emitCmd.Duration("interval", defaultInterval, "Interval between sending beacons (e.g., 500ms, 1s)")
	emitAddress := emitCmd.String("address", "127.0.0.1", "IP address to send beacons to (e.g., 239.0.0.1 for multicast, 192.168.1.255 for broadcast)")
	emitPort := emitCmd.Int("port", defaultPort, "UDP port to send beacons on")

	// Listener specific flags
	listenCmd := flag.NewFlagSet("listen", flag.ExitOnError)
	listenAddress := listenCmd.String("address", "0.0.0.0", "IP address to listen on (e.g., 0.0.0.0 for all interfaces, 239.0.0.1 for multicast group)")
	listenPort := listenCmd.Int("port", defaultPort, "UDP port to listen on")

	if len(os.Args) < 2 {
		fmt.Println("Usage: nightly-chrono-sync-beacon <command> [arguments]")
		fmt.Println("Commands:")
		fmt.Println("  emit    Start beacon emitter")
		fmt.Println("  listen  Start beacon listener")
		fmt.Println("Use 'nightly-chrono-sync-beacon <command> -h' for more information about a command.")
		os.Exit(1)
	}

	switch os.Args[1] {
	case "emit":
		emitCmd.Parse(os.Args[2:])
		if *emitID == "" {
			log.Fatal("Emitter ID is required. Use -id flag.")
		}
		addr, err := net.ResolveUDPAddr("udp", fmt.Sprintf("%s:%d", *emitAddress, *emitPort))
		if err != nil {
			log.Fatalf("Failed to resolve UDP address for emitter: %v", err)
		}
		conn, err := net.DialUDP("udp", nil, addr)
		if err != nil {
			log.Fatalf("Failed to create UDP connection for emitter: %v", err)
		}
		defer conn.Close()
		runEmitter(*emitID, *emitPort, *emitInterval, *emitAddress, &realUDPConn{conn})
	case "listen":
		listenCmd.Parse(os.Args[2:])
		addr, err := net.ResolveUDPAddr("udp", fmt.Sprintf("%s:%d", *listenAddress, *listenPort))
		if err != nil {
			log.Fatalf("Failed to resolve UDP address for listener: %v", err)
		}
		conn, err := net.ListenUDP("udp", addr)
		if err != nil {
			log.Fatalf("Failed to listen on UDP: %v", err)
		}
		defer conn.Close()

		// If it's a multicast address, join the group
		if addr.IP.IsMulticast() {
			if err := conn.JoinGroup(addr.IP, nil); err != nil {
				log.Fatalf("Failed to join multicast group %s: %v", addr.IP, err)
			}
			log.Printf("Joined multicast group: %s", addr.IP)
		}

		runListener(*listenPort, *listenAddress, &realUDPConn{conn})
	default:
		fmt.Println("Unknown command: " + os.Args[1])
		os.Exit(1)
	}
}
