package main

import (
	"bufio"
	"io"
	"net"
	"strings"
	"sync"
	"testing"
	"time"
)

// Helper to find an available port for testing
func getFreePort() (string, error) {
	addr, err := net.ResolveTCPAddr("tcp", "localhost:0")
	if err != nil {
		return "", err
	}
	listener, err := net.ListenTCP("tcp", addr)
	if err != nil {
		return "", err
	}
	defer listener.Close()
	return strings.Split(listener.Addr().String(), ":")[1], nil
}

func TestBroadcastServer_SingleClient(t *testing.T) {
	port, err := getFreePort()
	if err != nil {
		t.Fatalf("Failed to get free port: %v", err)
	}

	server := NewBroadcastServer()

	var serverWg sync.WaitGroup
	serverWg.Add(1)
	go func() {
		defer serverWg.Done()
		server.Start(port)
	}()

	// Give server a moment to start listening
	time.Sleep(100 * time.Millisecond)

	// Connect a client
	clientConn, err := net.Dial("tcp", "localhost:"+port)
	if err != nil {
		t.Fatalf("Failed to connect client: %v", err)
	}
	defer clientConn.Close()

	// Give server a moment to register client
	time.Sleep(100 * time.Millisecond)

	testMessage := "Hello, void!"
	server.Broadcast(testMessage)

	// Read from client connection
	reader := bufio.NewReader(clientConn)
	clientMsg, err := reader.ReadString('\n')
	if err != nil {
		t.Fatalf("Client failed to read message: %v", err)
	}

	expectedMsg := testMessage + "\n"
	if clientMsg != expectedMsg {
		t.Errorf("Expected message %q, got %q", expectedMsg, clientMsg)
	}

	server.Stop()
	serverWg.Wait() // Wait for server to fully shut down
}

func TestBroadcastServer_MultipleClients(t *testing.T) {
	port, err := getFreePort()
	if err != nil {
		t.Fatalf("Failed to get free port: %v", err)
	}

	server := NewBroadcastServer()

	var serverWg sync.WaitGroup
	serverWg.Add(1)
	go func() {
		defer serverWg.Done()
		server.Start(port)
	}()
	time.Sleep(100 * time.Millisecond)

	numClients := 3
	clientConns := make([]net.Conn, numClients)
	clientReaders := make([]*bufio.Reader, numClients)
	for i := 0; i < numClients; i++ {
		conn, err := net.Dial("tcp", "localhost:"+port)
		if err != nil {
			t.Fatalf("Failed to connect client %d: %v", i, err)
		}
		clientConns[i] = conn
		clientReaders[i] = bufio.NewReader(conn)
	}
	defer func() {
		for _, conn := range clientConns {
			conn.Close()
		}
	}()

	time.Sleep(100 * time.Millisecond) // Give server time to register clients

	testMessage := "Whisper to all!"
	server.Broadcast(testMessage)

	expectedMsg := testMessage + "\n"
	for i, reader := range clientReaders {
		clientMsg, err := reader.ReadString('\n')
		if err != nil {
			t.Fatalf("Client %d failed to read message: %v", i, err)
		}
		if clientMsg != expectedMsg {
			t.Errorf("Client %d: Expected message %q, got %q", i, expectedMsg, clientMsg)
		}
	}

	server.Stop()
	serverWg.Wait()
}

func TestBroadcastServer_ClientDisconnect(t *testing.T) {
	port, err := getFreePort()
	if err != nil {
		t.Fatalf("Failed to get free port: %v", err)
	}

	server := NewBroadcastServer()

	var serverWg sync.WaitGroup
	serverWg.Add(1)
	go func() {
		defer serverWg.Done()
		server.Start(port)
	}()
	time.Sleep(100 * time.Millisecond)

	client1, err := net.Dial("tcp", "localhost:"+port)
	if err != nil {
		t.Fatalf("Failed to connect client 1: %v", err)
	}
	client2, err := net.Dial("tcp", "localhost:"+port)
	if err != nil {
		t.Fatalf("Failed to connect client 2: %v", err)
	}

	time.Sleep(100 * time.Millisecond) // Give server time to register clients

	// Client 1 disconnects
	client1.Close()
	time.Sleep(200 * time.Millisecond) // Give server time to process disconnect

	// Broadcast a message
	testMessage := "After disconnect"
	server.Broadcast(testMessage)

	// Only client 2 should receive the message
	reader2 := bufio.NewReader(client2)
	client2Msg, err := reader2.ReadString('\n')
	if err != nil {
		t.Fatalf("Client 2 failed to read message: %v", err)
	}
	expectedMsg := testMessage + "\n"
	if client2Msg != expectedMsg {
		t.Errorf("Client 2: Expected message %q, got %q", expectedMsg, client2Msg)
	}

	// Try to read from client 1 (should fail or block)
	// # Mock rationale: In a real scenario, ReadString would block or return EOF/closed connection error.
	// For deterministic testing, we assert the expected error for a closed connection.
	client1Reader := bufio.NewReader(client1)
	_, err = client1Reader.ReadString('\n')
	if err == nil || (!strings.Contains(err.Error(), "use of closed network connection") && err != io.EOF) {
		t.Errorf("Expected error for closed connection or EOF, got %v", err)
	}

	client2.Close()
	server.Stop()
	serverWg.Wait()
}

func TestBroadcastServer_NoClients(t *testing.T) {
	port, err := getFreePort()
	if err != nil {
		t.Fatalf("Failed to get free port: %v", err)
	}

	server := NewBroadcastServer()

	var serverWg sync.WaitGroup
	serverWg.Add(1)
	go func() {
		defer serverWg.Done()
		server.Start(port)
	}()
	time.Sleep(100 * time.Millisecond)

	// Broadcast a message with no clients connected
	testMessage := "No one is listening"
	server.Broadcast(testMessage)

	// No errors should occur, and the server should remain stable.
	// This test primarily checks for panics or deadlocks.
	time.Sleep(100 * time.Millisecond)

	server.Stop()
	serverWg.Wait()
}

func TestBroadcastServer_Stop(t *testing.T) {
	port, err := getFreePort()
	if err != nil {
		t.Fatalf("Failed to get free port: %v", err)
	}

	server := NewBroadcastServer()

	var serverWg sync.WaitGroup
	serverWg.Add(1)
	go func() {
		defer serverWg.Done()
		server.Start(port)
	}()
	time.Sleep(100 * time.Millisecond)

	// Connect a client
	clientConn, err := net.Dial("tcp", "localhost:"+port)
	if err != nil {
		t.Fatalf("Failed to connect client: %v", err)
	}
	// defer clientConn.Close() // Client will be closed by server.Stop()

	time.Sleep(100 * time.Millisecond) // Give server time to register client

	server.Stop()
	serverWg.Wait() // Wait for server to shut down

	// Verify client connection is closed
	// # Mock rationale: Attempting to read from a server-closed connection should result in EOF or a closed network error.
	reader := bufio.NewReader(clientConn)
	_, err = reader.ReadString('\n')
	if err == nil || (err != io.EOF && !strings.Contains(err.Error(), "use of closed network connection")) {
		t.Errorf("Expected EOF or closed connection error after server stop, got %v", err)
	}
	clientConn.Close() // Ensure client is closed even if test fails early
}

func TestBroadcastServer_BroadcastWhileStopping(t *testing.T) {
	port, err := getFreePort()
	if err != nil {
		t.Fatalf("Failed to get free port: %v", err)
	}

	server := NewBroadcastServer()

	var serverWg sync.WaitGroup
	serverWg.Add(1)
	go func() {
		defer serverWg.Done()
		server.Start(port)
	}()
	time.Sleep(100 * time.Millisecond)

	// Start shutdown
	server.Stop()

	// Attempt to broadcast a message immediately after stopping
	server.Broadcast("This whisper should be dropped")

	// Ensure no panic and server eventually shuts down
	serverWg.Wait()
}
