package main

import (
	"encoding/json"
	"fmt"
	"log"
	"math/rand"
	"net"
	"os"
	"strconv"
	"time"
)

// TimePulse represents the data structure for the time broadcast.
type TimePulse struct {
	Timestamp string  `json:"timestamp"`
	OffsetSec float64 `json:"offset_sec"`
	Message   string  `json:"message"`
}

// UDPSender defines an interface for sending UDP packets.
// This allows for mocking in tests.
type UDPSender interface {
	Send(data []byte, addr *net.UDPAddr) error
}

// RealUDPSender implements UDPSender for actual network operations.
type RealUDPSender struct {
	conn *net.UDPConn
}

// NewRealUDPSender creates a new RealUDPSender.
func NewRealUDPSender(multicastAddr string, port int) (*RealUDPSender, error) {
	addr, err := net.ResolveUDPAddr("udp", fmt.Sprintf("%s:%d", multicastAddr, port))
	if err != nil {
		return nil, fmt.Errorf("failed to resolve UDP address: %w", err)
	}

	conn, err := net.DialUDP("udp", nil, addr)
	if err != nil {
		return nil, fmt.Errorf("failed to dial UDP: %w", err)
	}
	return &RealUDPSender{conn: conn},
		err
}

// Send sends data over UDP.
func (s *RealUDPSender) Send(data []byte, addr *net.UDPAddr) error {
	_, err := s.conn.WriteToUDP(data, addr)
	return err
}

// Close closes the underlying UDP connection.
func (s *RealUDPSender) Close() error {
	if s.conn != nil {
		return s.conn.Close()
	}
	return nil
}

// generateTimePulse creates a TimePulse with a whimsical offset.
func generateTimePulse(maxOffsetSec float64) TimePulse {
	now := time.Now().UTC()
	offset := (rand.Float64()*2 - 1) * maxOffsetSec // Random float between -maxOffsetSec and +maxOffsetSec

	whimsicalTime := now.Add(time.Duration(offset * float64(time.Second)))

	return TimePulse{
		Timestamp: whimsicalTime.Format(time.RFC3339Nano),
		OffsetSec: offset,
		Message:   "A pulse from the Chrono-Sync Orb!",
	}
}

// startOrb begins broadcasting time pulses.
func startOrb(sender UDPSender, multicastAddr string, port int, interval time.Duration, maxOffsetSec float64) {
	log.Printf("Chrono-Sync Orb starting. Broadcasting to %s:%d every %v with max offset %.2f seconds.",
		multicastAddr, port, interval, maxOffsetSec)

	targetAddr, err := net.ResolveUDPAddr("udp", fmt.Sprintf("%s:%d", multicastAddr, port))
	if err != nil {
		log.Fatalf("Failed to resolve target UDP address for sending: %v", err)
	}

	ticker := time.NewTicker(interval)
	defer ticker.Stop()

	for range ticker.C {
		pulse := generateTimePulse(maxOffsetSec)
		data, err := json.Marshal(pulse)
		if err != nil {
			log.Printf("Error marshalling time pulse: %v", err)
			continue
		}

		if err := sender.Send(data, targetAddr); err != nil {
			log.Printf("Error sending time pulse: %v", err)
		} else {
			log.Printf("Sent pulse: %s (Offset: %.2fs)", pulse.Timestamp, pulse.OffsetSec)
		}
	}
}

func main() {
	rand.Seed(time.Now().UnixNano()) // Seed random number generator

	multicastAddr := os.Getenv("ORB_MULTICAST_ADDR")
	if multicastAddr == "" {
		multicastAddr = "224.0.0.1"
	}

	portStr := os.Getenv("ORB_PORT")
	port, err := strconv.Atoi(portStr)
	if err != nil || port == 0 {
		port = 9000
	}

	intervalStr := os.Getenv("ORB_INTERVAL_SECONDS")
	intervalSec, err := strconv.Atoi(intervalStr)
	if err != nil || intervalSec == 0 {
		intervalSec = 3
	}
	interval := time.Duration(intervalSec) * time.Second

	maxOffsetStr := os.Getenv("ORB_MAX_OFFSET_SECONDS")
	maxOffsetSec, err := strconv.ParseFloat(maxOffsetStr, 64)
	if err != nil || maxOffsetSec == 0 {
		maxOffsetSec = 5.0
	}

	sender, err := NewRealUDPSender(multicastAddr, port)
	if err != nil {
		log.Fatalf("Failed to create UDP sender: %v", err)
	}
	defer sender.Close()

	startOrb(sender, multicastAddr, port, interval, maxOffsetSec)
}
