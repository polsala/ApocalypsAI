package tests

import (
	"fmt"
	"net"
	"sync"
	"testing"
	"time"

	// Import the server and client packages using the module path
	server "nightly-chronosync-beacon/src/server"
	client "nightly-chronosync-beacon/src/client"
)

// Mock rationale: We need to control the time returned by the server for deterministic tests.
// By providing a mock `server.GetTimeFunc`, we can ensure the server always returns a predictable timestamp,
// regardless of when the test is run. This makes tests reliable and repeatable.
var mockTime int64 = 1678886400000000000 // March 15, 2023 00:00:00 UTC in nanoseconds

func mockGetTime() int64 {
	return mockTime
}

func TestChronosyncBeacon(t *testing.T) {
	// Find an available UDP port for the test server
	listener, err := net.ListenPacket("udp", "127.0.0.1:0")
	if err != nil {
		t.Fatalf("Failed to find an available port: %v", err)
	}
	testPort := listener.LocalAddr().(*net.UDPAddr).Port
	listener.Close() // Close it, the server will open it again

	testServerAddr := fmt.Sprintf("127.0.0.1:%d", testPort)

	stopChan := make(chan struct{})
	serverReady := make(chan struct{})

	// Start the server in a goroutine
	go func() {
		close(serverReady) // Signal that the server setup is complete
		// Start the server with the mock time function and a stop channel
		err := server.StartServer(testPort, mockGetTime, stopChan) // # Mock rationale: Using mockGetTime for deterministic time.
		if err != nil {
			t.Errorf("Server exited with error: %v", err)
		}
	}()
	<-serverReady // Wait for the server to be ready
	time.Sleep(50 * time.Millisecond) // Give a tiny moment for the listener to actually be active

	t.Run("Client queries beacon and receives correct time", func(t *testing.T) {
		beaconTime, err := client.QueryBeacon(testServerAddr) // # Mock rationale: Client queries the server which uses mockGetTime.
		if err != nil {
			t.Fatalf("Client query failed: %v", err)
		}

		expectedTime := time.Unix(0, mockTime)
		// Allow for a small deviation due to network latency simulation in client's calculation
		// The client adds roundTripTime/2. If roundTripTime is very small (e.g., 0-1ms),
		// the adjustment will be 0 or 1 nanosecond.
		// We'll check if it's very close to the mock time.
		diff := beaconTime.Sub(expectedTime)
		if diff < 0 {
			diff = -diff
		}

		// Allow for a small margin of error (e.g., 100 microseconds) for the client's RTT calculation
		if diff > 100*time.Microsecond {
			t.Errorf("Expected beacon time %s (Unix Nano: %d), got %s (Unix Nano: %d). Difference: %s",
				expectedTime.UTC().Format(time.RFC3339Nano), expectedTime.UnixNano(),
				beaconTime.UTC().Format(time.RFC3339Nano), beaconTime.UnixNano(),
				diff)
		}
	})

	t.Run("Multiple clients query beacon concurrently", func(t *testing.T) {
		numClients := 5
		clientWg := sync.WaitGroup{}
		clientWg.Add(numClients)

		for i := 0; i < numClients; i++ {
			go func(clientID int) {
				defer clientWg.Done()
				beaconTime, err := client.QueryBeacon(testServerAddr)
				if err != nil {
					t.Errorf("Client %d query failed: %v", clientID, err)
					return
				}

				expectedTime := time.Unix(0, mockTime)
				diff := beaconTime.Sub(expectedTime)
				if diff < 0 {
					diff = -diff
				}
				if diff > 100*time.Microsecond {
					t.Errorf("Client %d: Expected beacon time %s (Unix Nano: %d), got %s (Unix Nano: %d). Difference: %s",
						clientID, expectedTime.UTC().Format(time.RFC3339Nano), expectedTime.UnixNano(),
						beaconTime.UTC().Format(time.RFC3339Nano), beaconTime.UnixNano(),
						diff)
				}
			}(i)
		}
		clientWg.Wait()
	})

	// Signal the server to shut down
	close(stopChan)
	time.Sleep(50 * time.Millisecond) // Give server a moment to process shutdown
}
