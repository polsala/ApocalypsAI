package main

import (
	"bufio"
	"fmt"
	"net"
	"strings"
	"sync"
	"testing"
	"time"
)

// Helper to start the server in a goroutine on a random available port
func startTestServer(t *testing.T) (string, func()) {
	listener, err := net.Listen("tcp", "127.0.0.1:0") // Listen on a random port
	if err != nil {
		t.Fatalf("Failed to listen: %v", err)
	}
	addr := listener.Addr().String()

	hub := NewHub()
	go hub.Run()

	go func() {
		for {
			conn, err := listener.Accept()
			if err != nil {
				// Listener closed, exit goroutine
				if strings.Contains(err.Error(), "use of closed network connection") {
					return
				}
				t.Logf("Error accepting connection in test server: %v", err)
				continue
			}
			go hub.handleClient(conn)
		}
	}()

	cleanup := func() {
		listener.Close()
		// Give some time for goroutines to shut down
		time.Sleep(100 * time.Millisecond)
	}

	return addr, cleanup
}

// Helper to connect a client and return its connection and a reader
func connectClient(t *testing.T, addr string) (net.Conn, *bufio.Reader) {
	conn, err := net.Dial("tcp", addr)
	if err != nil {
		t.Fatalf("Failed to connect to server: %v", err)
	}
	return conn, bufio.NewReader(conn)
}

// Mock rationale: These tests directly interact with the 'net' package, simulating client connections
// to a locally running server. This provides a deterministic and offline test environment without
// requiring external network resources or complex mocking frameworks. The server itself is the
// system under test, and its network interactions are part of its core functionality.

func TestSingleClientNoBroadcast(t *testing.T) {
	addr, cleanup := startTestServer(t)
	defer cleanup()

	client1Conn, client1Reader := connectClient(t, addr)
	defer client1Conn.Close()

	// Give time for client to register
	time.Sleep(50 * time.Millisecond)

	// Client 1 sends a message
	message := "Hello from client 1"
	fmt.Fprintln(client1Conn, message)

	// There should be no broadcast back to client 1 itself
	client1Conn.SetReadDeadline(time.Now().Add(100 * time.Millisecond))
	_, err := client1Reader.ReadString('\n')
	if err == nil || !strings.Contains(err.Error(), "timeout") {
		t.Errorf("Expected no message back to sender, got: %v", err)
	}
}

func TestTwoClientsBroadcast(t *testing.T) {
	addr, cleanup := startTestServer(t)
	defer cleanup()

	client1Conn, client1Reader := connectClient(t, addr)
	defer client1Conn.Close()

	client2Conn, client2Reader := connectClient(t, addr)
	defer client2Conn.Close()

	// Give time for clients to register
	time.Sleep(50 * time.Millisecond)

	var wg sync.WaitGroup
	wg.Add(1)

	expectedMsg := "Hello from client 1"
	go func() {
		defer wg.Done()
		client2Conn.SetReadDeadline(time.Now().Add(5 * time.Second))
		received, err := client2Reader.ReadString('\n')
		if err != nil {
			t.Errorf("Client 2 failed to read: %v", err)
			return
		}
		if !strings.Contains(received, expectedMsg) {
			t.Errorf("Client 2 received unexpected message. Got: %q, Expected to contain: %q", received, expectedMsg)
		}
		// Check for sender info
		if !strings.Contains(received, client1Conn.RemoteAddr().String()) {
			t.Errorf("Client 2 received message without sender info. Got: %q, Expected to contain: %q", received, client1Conn.RemoteAddr().String())
		}
	}()

	// Client 1 sends a message
	fmt.Fprintln(client1Conn, expectedMsg)

	wg.Wait()

	// Ensure client 1 doesn't get its own message back
	client1Conn.SetReadDeadline(time.Now().Add(100 * time.Millisecond))
	_, err := client1Reader.ReadString('\n')
	if err == nil || !strings.Contains(err.Error(), "timeout") {
		t.Errorf("Expected no message back to sender, got: %v", err)
	}
}

func TestMultipleClientsBroadcast(t *testing.T) {
	addr, cleanup := startTestServer(t)
	defer cleanup()

	clientConns := make([]net.Conn, 3)
	clientReaders := make([]*bufio.Reader, 3)

	for i := 0; i < 3; i++ {
		clientConns[i], clientReaders[i] = connectClient(t, addr)
		defer clientConns[i].Close()
	}

	time.Sleep(50 * time.Millisecond) // Give time for clients to register

	var wg sync.WaitGroup
	expectedMsg := "Broadcast from client 0"

	// Expect client 1 and client 2 to receive the message
	for i := 1; i < 3; i++ {
		wg.Add(1)
		go func(reader *bufio.Reader, clientNum int) {
			defer wg.Done()
			clientConns[clientNum].SetReadDeadline(time.Now().Add(5 * time.Second))
			received, err := reader.ReadString('\n')
			if err != nil {
				t.Errorf("Client %d failed to read: %v", clientNum, err)
				return
			}
			if !strings.Contains(received, expectedMsg) {
				t.Errorf("Client %d received unexpected message. Got: %q, Expected to contain: %q", clientNum, received, expectedMsg)
			}
			if !strings.Contains(received, clientConns[0].RemoteAddr().String()) {
				t.Errorf("Client %d received message without sender info. Got: %q, Expected to contain: %q", clientNum, clientConns[0].RemoteAddr().String())
			}
		}(clientReaders[i], i)
	}

	// Client 0 sends a message
	fmt.Fprintln(clientConns[0], expectedMsg)

	wg.Wait()

	// Ensure client 0 doesn't get its own message back
	clientConns[0].SetReadDeadline(time.Now().Add(100 * time.Millisecond))
	_, err := clientReaders[0].ReadString('\n')
	if err == nil || !strings.Contains(err.Error(), "timeout") {
		t.Errorf("Expected no message back to sender, got: %v", err)
	}
}

func TestClientDisconnect(t *testing.T) {
	addr, cleanup := startTestServer(t)
	defer cleanup()

	client1Conn, client1Reader := connectClient(t, addr)
	defer client1Conn.Close()

	client2Conn, client2Reader := connectClient(t, addr)
	// client2Conn will be closed explicitly

	client3Conn, client3Reader := connectClient(t, addr)
	defer client3Conn.Close()

	time.Sleep(50 * time.Millisecond) // Give time for clients to register

	// Client 2 disconnects
	client2Conn.Close()
	time.Sleep(100 * time.Millisecond) // Give time for unregister to process

	var wg sync.WaitGroup
	expectedMsg := "Message after disconnect"

	// Client 1 sends a message, only client 3 should receive it
	wg.Add(1)
	go func() {
		defer wg.Done()
		client3Conn.SetReadDeadline(time.Now().Add(5 * time.Second))
		received, err := client3Reader.ReadString('\n')
		if err != nil {
			t.Errorf("Client 3 failed to read: %v", err)
			return
		}
		if !strings.Contains(received, expectedMsg) {
			t.Errorf("Client 3 received unexpected message. Got: %q, Expected to contain: %q", received, expectedMsg)
		}
	}()

	fmt.Fprintln(client1Conn, expectedMsg)
	wg.Wait()

	// Ensure client 2 (disconnected) does not receive anything (and doesn't cause issues)
	client2Conn.SetReadDeadline(time.Now().Add(100 * time.Millisecond))
	_, err := client2Reader.ReadString('\n')
	if err == nil || !strings.Contains(err.Error(), "timeout") {
		t.Errorf("Expected no message back to disconnected client, got: %v", err)
	}
}

func TestNoClientsNoBroadcast(t *testing.T) {
	addr, cleanup := startTestServer(t)
	defer cleanup()

	// No clients connected
	time.Sleep(50 * time.Millisecond)

	// Try to send a message (this would typically come from a client, but for testing
	// we can simulate the hub's broadcast channel directly if needed, or just ensure
	// the hub doesn't panic with no clients).
	// For this test, we're just ensuring the server starts and doesn't crash.
	// The hub's broadcast logic already checks len(h.clients) > 1 before broadcasting.

	// Connect a client, send a message, then disconnect. No other clients to receive.
	clientConn, clientReader := connectClient(t, addr)
	defer clientConn.Close()

	time.Sleep(50 * time.Millisecond)

	fmt.Fprintln(clientConn, "Test message with no other clients")

	clientConn.SetReadDeadline(time.Now().Add(100 * time.Millisecond))
	_, err := clientReader.ReadString('\n')
	if err == nil || !strings.Contains(err.Error(), "timeout") {
		t.Errorf("Expected no message back to sender when no other clients, got: %v", err)
	}
}
