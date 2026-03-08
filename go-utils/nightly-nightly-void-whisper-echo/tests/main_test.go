package main

import (
	"bytes"
	"fmt"
	"net"
	"sync"
	"testing"
	"time"
)

// Mock rationale: We are mocking the network interaction by creating a local UDP server
// and client within the test environment. This ensures the test is deterministic and
// does not rely on external network resources or actual internet connectivity.
// The server runs in a goroutine, and the client sends/receives packets on localhost.

const testBufferSize = 1024 // Must match the server's buffer size for accurate testing
const testEchoPrefix = "The void echoes: " // Must match the server's prefix

// runTestServer starts a UDP server in a goroutine that processes a single packet.
// It listens on the provided testPort.
func runTestServer(t *testing.T, wg *sync.WaitGroup, testPort int) {
	defer wg.Done()

	conn, err := net.ListenPacket("udp", fmt.Sprintf(":%d", testPort))
	if err != nil {
		t.Errorf("Server failed to listen on port %d: %v", testPort, err)
		return
	}
	defer conn.Close()

	buffer := make([]byte, testBufferSize)
	conn.SetReadDeadline(time.Now().Add(5 * time.Second)) // Timeout for server read
	
	n, clientAddr, err := conn.ReadFrom(buffer)
	if err != nil {
		// If it's a timeout, it's okay, the client might not have sent anything
		if netErr, ok := err.(net.Error); ok && netErr.Timeout() {
			t.Logf("Server read timeout (no packet received within deadline): %v", err)
			return
		}
		t.Errorf("Server error reading UDP packet: %v", err)
		return
	}

	receivedMsg := string(buffer[:n])
	responseMsg := testEchoPrefix + receivedMsg
	
	// Ensure the response doesn't exceed UDP packet size limits if possible
	if len(responseMsg) > testBufferSize {
		responseMsg = responseMsg[:testBufferSize]
	}

	_, err = conn.WriteTo([]byte(responseMsg), clientAddr)
	if err != nil {
		t.Errorf("Server error writing UDP response: %v", err)
	}
}

func TestUDPEchoServer(t *testing.T) {
	// Find a random available port using a TCP listener, then close it.
	// This is a common trick to get an ephemeral port that's likely free for UDP.
	listener, err := net.Listen("tcp", "127.0.0.1:0")
	if err != nil {
		t.Fatalf("Failed to find an available port: %v", err)
	}
	testPort := listener.Addr().(*net.TCPAddr).Port
	listener.Close() 

	t.Logf("Test server will listen on port %d", testPort)

	var wg sync.WaitGroup
	wg.Add(1)
	go runTestServer(t, &wg, testPort)

	// Give the server a moment to start listening
	time.Sleep(100 * time.Millisecond)

	// Create a UDP client
	serverUDPAddr, err := net.ResolveUDPAddr("udp", fmt.Sprintf("127.0.0.1:%d", testPort))
	if err != nil {
		t.Fatalf("Failed to resolve server UDP address: %v", err)
	}
	clientConn, err := net.DialUDP("udp", nil, serverUDPAddr)
	if err != nil {
		t.Fatalf("Failed to dial UDP server: %v", err)
	}
	defer clientConn.Close()

	testMessage := "Hello, void!"
	expectedResponse := testEchoPrefix + testMessage

	// Send message
	_, err = clientConn.Write([]byte(testMessage))
	if err != nil {
		t.Fatalf("Failed to send UDP message: %v", err)
	}

	// Read response with a timeout
	clientConn.SetReadDeadline(time.Now().Add(5 * time.Second))
	responseBuffer := make([]byte, testBufferSize)
	n, _, err := clientConn.ReadFromUDP(responseBuffer)
	if err != nil {
		t.Fatalf("Failed to read UDP response: %v", err)
	}

	actualResponse := string(responseBuffer[:n])

	if actualResponse != expectedResponse {
		t.Errorf("Expected response \"%s\", got \"%s\"", expectedResponse, actualResponse)
	}

	wg.Wait() // Wait for the server goroutine to finish
}

func TestUDPEchoServer_EmptyMessage(t *testing.T) {
	listener, err := net.Listen("tcp", "127.0.0.1:0")
	if err != nil {
		t.Fatalf("Failed to find an available port: %v", err)
	}
	testPort := listener.Addr().(*net.TCPAddr).Port
	listener.Close()

	t.Logf("Test server will listen on port %d", testPort)

	var wg sync.WaitGroup
	wg.Add(1)
	go runTestServer(t, &wg, testPort)

	time.Sleep(100 * time.Millisecond)

	serverUDPAddr, err := net.ResolveUDPAddr("udp", fmt.Sprintf("127.0.0.1:%d", testPort))
	if err != nil {
		t.Fatalf("Failed to resolve server UDP address: %v", err)
	}
	clientConn, err := net.DialUDP("udp", nil, serverUDPAddr)
	if err != nil {
		t.Fatalf("Failed to dial UDP server: %v", err)
	}
	defer clientConn.Close()

	testMessage := "" // Empty message
	expectedResponse := testEchoPrefix + testMessage

	_, err = clientConn.Write([]byte(testMessage))
	if err != nil {
		t.Fatalf("Failed to send UDP message: %v", err)
	}

	clientConn.SetReadDeadline(time.Now().Add(5 * time.Second))
	responseBuffer := make([]byte, testBufferSize)
	n, _, err := clientConn.ReadFromUDP(responseBuffer)
	if err != nil {
		t.Fatalf("Failed to read UDP response: %v", err)
	}

	actualResponse := string(responseBuffer[:n])

	if actualResponse != expectedResponse {
		t.Errorf("Expected response \"%s\", got \"%s\"", expectedResponse, actualResponse)
	}

	wg.Wait()
}

func TestUDPEchoServer_LongMessage(t *testing.T) {
	listener, err := net.Listen("tcp", "127.0.0.1:0")
	if err != nil {
		t.Fatalf("Failed to find an available port: %v", err)
	}
	testPort := listener.Addr().(*net.TCPAddr).Port
	listener.Close()

	t.Logf("Test server will listen on port %d", testPort)

	var wg sync.WaitGroup
	wg.Add(1)
	go runTestServer(t, &wg, testPort)

	time.Sleep(100 * time.Millisecond)

	serverUDPAddr, err := net.ResolveUDPAddr("udp", fmt.Sprintf("127.0.0.1:%d", testPort))
	if err != nil {
		t.Fatalf("Failed to resolve server UDP address: %v", err)
	}
	clientConn, err := net.DialUDP("udp", nil, serverUDPAddr)
	if err != nil {
		t.Fatalf("Failed to dial UDP server: %v", err)
	}
	defer clientConn.Close()

	// Create a message that's close to the buffer size, ensuring it fits
	// UDP packets have a typical max size (MTU), often around 1472 bytes for data.
	// Our buffer is 1024. Let's ensure the message + prefix fits within this.
	maxMessageLen := testBufferSize - len(testEchoPrefix)
	if maxMessageLen < 0 {
		maxMessageLen = 0
	}
	testMessage := bytes.Repeat([]byte("a"), maxMessageLen).String()
	expectedResponse := testEchoPrefix + testMessage

	_, err = clientConn.Write([]byte(testMessage))
	if err != nil {
		t.Fatalf("Failed to send UDP message: %v", err)
	}

	clientConn.SetReadDeadline(time.Now().Add(5 * time.Second))
	responseBuffer := make([]byte, testBufferSize*2) // Use a larger buffer for reading response to ensure we capture full echo
	n, _, err := clientConn.ReadFromUDP(responseBuffer)
	if err != nil {
		t.Fatalf("Failed to read UDP response: %v", err)
	}

	actualResponse := string(responseBuffer[:n])

	if actualResponse != expectedResponse {
		t.Errorf("Expected response length %d, got %d", len(expectedResponse), len(actualResponse))
		t.Errorf("Expected response \"%s\", got \"%s\"", expectedResponse, actualResponse)
	}

	wg.Wait()
}
