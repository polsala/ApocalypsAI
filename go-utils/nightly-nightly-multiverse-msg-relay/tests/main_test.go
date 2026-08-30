package main

import (
	"bufio"
	"bytes"
	"fmt"
	"io"
	"log"
	"net"
	"strings"
	"sync"
	"testing"
	"time"
)

// Mock rationale: We need to simulate multiple network listeners (dimensions) and a client sending a message
// to the main relay. Using actual local TCP listeners and dialers within the test provides a realistic
// and deterministic simulation without external dependencies.
// The mock listeners store received messages in a thread-safe buffer for verification.

// mockDimensionListener simulates a destination "dimension" server.
type mockDimensionListener struct {
	addr     string
	messages []string
	mu       sync.Mutex // Protects messages slice
	wg       *sync.WaitGroup
	listener net.Listener
}

func newMockDimensionListener(port int, wg *sync.WaitGroup) *mockDimensionListener {
	return &mockDimensionListener{
		addr:     fmt.Sprintf(":%d", port),
		messages: make([]string, 0),
		wg:       wg,
	}
}

func (m *mockDimensionListener) start() {
	var err error
	m.listener, err = net.Listen("tcp", m.addr)
	if err != nil {
		log.Fatalf("Mock listener failed to start on %s: %v", m.addr, err)
	}
	log.Printf("Mock dimension listener started on %s", m.addr)
	m.wg.Add(1)
	go func() {
		defer m.wg.Done()
		for {
			conn, err := m.listener.Accept()
			if err != nil {
				if strings.Contains(err.Error(), "use of closed network connection") {
					return // Listener closed
				}
				log.Printf("Mock listener %s accept error: %v", m.addr, err)
				continue
			}
			go m.handleMockConnection(conn)
		}
	}()
}

func (m *mockDimensionListener) stop() {
	if m.listener != nil {
		m.listener.Close()
	}
}

func (m *mockDimensionListener) handleMockConnection(conn net.Conn) {
	defer conn.Close()
	message, err := bufio.NewReader(conn).ReadString('\n')
	if err != nil && err != io.EOF {
		log.Printf("Mock listener %s error reading message: %v", m.addr, err)
		return
	}
	message = strings.TrimSpace(message)
	m.mu.Lock()
	m.messages = append(m.messages, message)
	m.mu.Unlock()
	log.Printf("Mock listener %s received: \"%s\"", m.addr, message)
}

func (m *mockDimensionListener) getMessages() []string {
	m.mu.Lock()
	defer m.mu.Unlock()
	return m.messages
}

func TestMultiverseMessageRelay(t *testing.T) {
	// Suppress log output during tests for cleaner output
	log.SetOutput(new(bytes.Buffer))

	relayListenPort := 18080
	destPorts := []int{18081, 18082, 18083}
	relayListenAddr := fmt.Sprintf(":%d", relayListenPort)
	destAddrs := make([]string, len(destPorts))
	for i, p := range destPorts {
		destAddrs[i] = fmt.Sprintf(":%d", p)
	}

	// 1. Start mock dimension listeners
	var mockListenersWg sync.WaitGroup
	mockListeners := make([]*mockDimensionListener, len(destPorts))
	for i, port := range destPorts {
		listener := newMockDimensionListener(port, &mockListenersWg)
		listener.start()
		mockListeners[i] = listener
	}
	defer func() {
		for _, ml := range mockListeners {
			ml.stop()
		}
		mockListenersWg.Wait() // Wait for all mock listener goroutines to exit
	}()

	// 2. Start the main relay server in a goroutine
	// We need to set the global flags for the main package
	oldListenAddr := listenAddr
	oldDestinations := destinations
	listenAddr = relayListenAddr
	destinations = strings.Join(destAddrs, ",")

	var relayServerWg sync.WaitGroup
	relayServerWg.Add(1)
	go func() {
		defer relayServerWg.Done()
		// Call main's startServer directly or simulate main's loop
		// For testing, we can directly call handleConnection or a simplified server loop
		listener, err := net.Listen("tcp", listenAddr)
		if err != nil {
			t.Errorf("Failed to start relay listener: %v", err)
			return
		}
		defer listener.Close()

		// Accept one connection and handle it, then close listener for test simplicity
		conn, err := listener.Accept()
		if err != nil {
			t.Errorf("Relay server accept error: %v", err)
			return
		}
		handleConnection(conn, strings.Split(destinations, ","))
	}()

	// Restore global flags after the test
	defer func() {
		listenAddr = oldListenAddr
		destinations = oldDestinations
	}()

	// Give servers a moment to start
	time.Sleep(100 * time.Millisecond)

	// 3. Send a message to the relay server
	testMessage := "ApocalypsAI Broadcast"
	clientConn, err := net.Dial("tcp", fmt.Sprintf("localhost%s", relayListenAddr))
	if err != nil {
		t.Fatalf("Failed to connect to relay server: %v", err)
	}
	_, err = fmt.Fprintf(clientConn, "%s\n", testMessage)
	if err != nil {
		t.Fatalf("Failed to send message to relay server: %v", err)
	}
	clientConn.Close()

	// 4. Wait for messages to be processed and broadcasted
	// Use a timeout to prevent tests from hanging indefinitely
	timeout := time.After(2 * time.Second)
	done := make(chan bool)
	go func() {
		// Wait for all mock listeners to receive the message
		// This is a bit tricky with concurrent sends. We'll poll.
		for {
			allReceived := true
			for _, ml := range mockListeners {
				if len(ml.getMessages()) == 0 {
					allReceived = false
					break
				}
			}
			if allReceived {
				done <- true
				return
			}
			time.Sleep(50 * time.Millisecond)
		}
	}()

	select {
	case <-done:
		// All messages received
	case <-timeout:
		t.Fatal("Timeout waiting for all mock listeners to receive messages")
	}

	// 5. Assert that each mock listener received the correct message
	for i, ml := range mockListeners {
		receivedMessages := ml.getMessages()
		if len(receivedMessages) != 1 {
			t.Errorf("Mock listener %d (%s) expected 1 message, got %d", i, ml.addr, len(receivedMessages))
			continue
		}
		if receivedMessages[0] != testMessage {
			t.Errorf("Mock listener %d (%s) expected message \"%s\", got \"%s\"", i, ml.addr, testMessage, receivedMessages[0])
		}
	}
}

func TestBroadcastMessage_DialFailure(t *testing.T) {
	// Suppress log output during tests
	log.SetOutput(new(bytes.Buffer))

	// Test that broadcastMessage handles a failed dial gracefully
	// Try to connect to a port that is definitely not listening
	nonExistentAddr := ":9999"
	testMessage := "Failure Test"

	// This should log an error but not panic or crash
	broadcastMessage(nonExistentAddr, testMessage)

	// No direct assertion possible without inspecting logs, but we ensure it doesn't crash.
	// A more robust test would capture log output and assert on its content.
	// For this context, ensuring no panic is sufficient.
}
