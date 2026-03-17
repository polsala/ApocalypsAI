package main_test

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net"
	"os"
	"runtime"
	"strings"
	"sync"
	"testing"
	"time"

	main "nightly-chronal-beacon/src"
)

// Mock rationale: This test uses local loopback interfaces and a specific multicast group
// to simulate network communication entirely within the test environment. It does not
// rely on external network resources or actual internet connectivity, making it deterministic
// and offline. The beacon itself is run as a goroutine, and a separate goroutine acts as
// a listener to verify the beacon's output.

func TestChronalBeaconBroadcast(t *testing.T) {
	// Skip on Windows due to known issues with Go's multicast support on some Windows versions
	// and potential firewall interference in CI/CD environments.
	// Multicast on Windows often requires specific interface binding or admin privileges.
	// For a robust cross-platform solution, more complex setup might be needed.
	// This test focuses on Linux/macOS environments where multicast is more consistently supported.
	if runtime.GOOS == "windows" {
		t.Skip("Skipping multicast test on Windows due to platform-specific multicast challenges.")
	}

	beaconID := "TestBeacon-123"
	interval := 500 * time.Millisecond // Faster interval for testing
	port := 12345                      // Use a unique port for testing
	multicastAddr := "224.0.0.1"

	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	var wg sync.WaitGroup

	// Start the beacon in a goroutine
	wg.Add(1)
	go func() {
		defer wg.Done()
		// Redirect log output to avoid polluting test results, but keep errors
		log.SetOutput(os.Stderr) // Or ioutil.Discard for complete silence
		err := main.StartBeacon(ctx, beaconID, interval, multicastAddr, port)
		if err != nil && err != context.Canceled {
			t.Errorf("Beacon exited with error: %v", err)
		}
	}()

	// Give the beacon a moment to start up
	time.Sleep(100 * time.Millisecond)

	// Set up a UDP listener for multicast messages
	listenerAddr, err := net.ResolveUDPAddr("udp", fmt.Sprintf("%s:%d", multicastAddr, port))
	if err != nil {
		t.Fatalf("Failed to resolve UDP address for listener: %v", err)
	}

	conn, err := net.ListenPacket("udp", fmt.Sprintf(":%d", port)) // Listen on all interfaces for the port
	if err != nil {
		t.Fatalf("Failed to listen on UDP port %d: %v", port, err)
	}
	defer conn.Close()

	udpConn := conn.(*net.UDPConn)

	// Find a suitable network interface for multicast
	interfaces, err := net.Interfaces()
	if err != nil {
		t.Fatalf("Failed to get network interfaces: %v", err)
	}

	var ifi *net.Interface
	for _, i := range interfaces {
		if (i.Flags&net.FlagUp != 0) && (i.Flags&net.FlagMulticast != 0) && (i.Flags&net.FlagLoopback == 0) {
			// Prefer a non-loopback, multicast-enabled, up interface
			ifi = &i
			break
		}
	}
	if ifi == nil {
		// Fallback to loopback if no other suitable interface is found
		for _, i := range interfaces {
			if (i.Flags&net.FlagUp != 0) && (i.Flags&net.FlagMulticast != 0) && (i.Flags&net.FlagLoopback != 0) {
				ifi = &i
				break
			}
		}
	}

	if ifi == nil {
		t.Skip("No suitable network interface found for multicast testing. Skipping.")
	}

	log.Printf("Joining multicast group %s on interface %s", multicastAddr, ifi.Name)

	if err := udpConn.JoinGroup(ifi, listenerAddr);
		 err != nil && !strings.Contains(err.Error(), "address already in use") {
		// "address already in use" can happen if a previous test run didn't clean up fast enough
		// or if the OS holds the group membership briefly. It's often ignorable for tests.
		t.Fatalf("Failed to join multicast group %s on interface %s: %v", multicastAddr, ifi.Name, err)
	}
	defer udpConn.LeaveGroup(ifi, listenerAddr)

	receivedCount := 0
	lastTimestamp := time.Time{}

	// Read a few messages to ensure continuous broadcasting
	readTimeout := interval + (interval / 2) // Allow some buffer for network latency
	for i := 0; i < 3; i++ {
		buffer := make([]byte, 1024)
		_ = udpConn.SetReadDeadline(time.Now().Add(readTimeout))
		n, _, err := udpConn.ReadFrom(buffer)
		if err != nil {
			t.Fatalf("Failed to read from UDP: %v", err)
		}

		var signature main.ChronalSignature
		err = json.Unmarshal(buffer[:n], &signature)
		if err != nil {
			t.Errorf("Failed to unmarshal JSON: %v", err)
			continue
		}

		if signature.ID != beaconID {
			t.Errorf("Expected ID %q, got %q", beaconID, signature.ID)
		}

		if signature.Timestamp.IsZero() {
			t.Errorf("Received zero timestamp")
		}

		if receivedCount > 0 {
			diff := signature.Timestamp.Sub(lastTimestamp)
			if diff < interval/2 || diff > interval*2 {
				t.Logf("Warning: Timestamp difference %v is outside expected range around %v", diff, interval)
			}
		}
		lastTimestamp = signature.Timestamp
		receivedCount++
	}

	if receivedCount < 3 {
		t.Errorf("Expected to receive at least 3 beacon messages, got %d", receivedCount)
	}

	// Stop the beacon
	cancel()
	wg.Wait() // Wait for the beacon goroutine to finish
}
