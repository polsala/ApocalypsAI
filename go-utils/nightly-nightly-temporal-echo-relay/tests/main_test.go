package main

import (
	"bufio"
	"bytes"
	"fmt"
	"io"
	"log"
	"net"
	"os"
	"strings"
	"sync"
	"testing"
	"time"
)

// # Mock rationale:
// We use `net.Pipe()` to create an in-memory, synchronous, full-duplex network connection.
// This allows us to test the `handleConnection` and `startClient` logic without binding to actual ports
// or relying on the operating system's network stack, making tests deterministic and offline.
// We also capture log output to assert on messages printed by the server/client.

func TestHandleConnection_NoDistortion(t *testing.T) {
	serverConn, clientConn := net.Pipe()
	defer serverConn.Close()
	defer clientConn.Close()

	config := ServerConfig{Port: 0, Delay: 0, LossProb: 0.0}

	var wg sync.WaitGroup
	wg.Add(1)
	go func() {
		defer wg.Done()
		handleConnection(serverConn, config)
	}()

	clientWriter := bufio.NewWriter(clientConn)
	clientReader := bufio.NewReader(clientConn)

	message := "Test Message 1"
	_, err := clientWriter.WriteString(message + "\n")
	if err != nil {
		t.Fatalf("Client write error: %v", err)
	}
	clientWriter.Flush()

	received, err := clientReader.ReadString('\n')
	if err != nil {
		t.Fatalf("Client read error: %v", err)
	}

	expected := fmt.Sprintf("Echo: %s\n", message)
	if received != expected {
		t.Errorf("Expected \"%s\", got \"%s\"", expected, received)
	}

	// Close client connection to signal server to stop handling
	clientConn.Close()
	wg.Wait() // Wait for handleConnection to finish
}

func TestHandleConnection_WithDelay(t *testing.T) {
	serverConn, clientConn := net.Pipe()
	defer serverConn.Close()
	defer clientConn.Close()

	delay := 100 * time.Millisecond
	config := ServerConfig{Port: 0, Delay: delay, LossProb: 0.0}

	var wg sync.WaitGroup
	wg.Add(1)
	go func() {
		defer wg.Done()
		handleConnection(serverConn, config)
	}()

	clientWriter := bufio.NewWriter(clientConn)
	clientReader := bufio.NewReader(clientConn)

	message := "Delayed Message"
	start := time.Now()
	_, err := clientWriter.WriteString(message + "\n")
	if err != nil {
		t.Fatalf("Client write error: %v", err)
	}
	clientWriter.Flush()

	received, err := clientReader.ReadString('\n')
	if err != nil {
		t.Fatalf("Client read error: %v", err)
	}
	actualDelay := time.Since(start)

	expected := fmt.Sprintf("Echo: %s\n", message)
	if received != expected {
		t.Errorf("Expected \"%s\", got \"%s\"", expected, received)
	}

	// Allow for some test execution overhead, but ensure it's at least the delay
	if actualDelay < delay {
		t.Errorf("Expected delay of at least %s, got %s", delay, actualDelay)
	}

	clientConn.Close()
	wg.Wait()
}

func TestHandleConnection_WithLoss(t *testing.T) {
	serverConn, clientConn := net.Pipe()
	defer serverConn.Close()
	defer clientConn.Close()

	// Set a high loss probability to ensure a drop in a single test run
	config := ServerConfig{Port: 0, Delay: 0, LossProb: 0.99}

	var wg sync.WaitGroup
	wg.Add(1)
	go func() {
		defer wg.Done()
		handleConnection(serverConn, config)
	}()

	clientWriter := bufio.NewWriter(clientConn)
	clientReader := bufio.NewReader(clientConn)

	message := "Lost Message"
	_, err := clientWriter.WriteString(message + "\n")
	if err != nil {
		t.Fatalf("Client write error: %v", err)
	}
	clientWriter.Flush()

	// Expect a read timeout or EOF because the message should be dropped
	clientConn.SetReadDeadline(time.Now().Add(50 * time.Millisecond)) // Short timeout
	_, err = clientReader.ReadString('\n')

	if err == nil || !strings.Contains(err.Error(), "timeout") && err != io.EOF {
		t.Errorf("Expected read timeout or EOF due to message loss, but got: %v", err)
	}

	clientConn.Close()
	wg.Wait()
}

func TestStartClient_Success(t *testing.T) {
	// Capture log output to verify client messages
	var buf bytes.Buffer
	log.SetOutput(&buf)
	defer func() { log.SetOutput(os.Stderr) }() // Restore default output

	// Mock the server side using a listener that immediately echoes
	listener, err := net.Listen("tcp", "localhost:0") // Listen on a random available port
	if err != nil {
		t.Fatalf("Failed to start mock listener: %v", err)
	}
	defer listener.Close()

	var serverWg sync.WaitGroup
	serverWg.Add(1)
	go func() {
		defer serverWg.Done()
		conn, err := listener.Accept()
		if err != nil {
			// This error can happen if listener is closed before accept
			if !strings.Contains(err.Error(), "use of closed network connection") {
				t.Errorf("Mock server accept error: %v", err)
			}
			return
		}
		defer conn.Close()

		reader := bufio.NewReader(conn)
		writer := bufio.NewWriter(conn)

		for {
			message, err := reader.ReadString('\n')
			if err != nil {
				return // Client disconnected
			}
			// Echo immediately without delay or loss
			_, _ = writer.WriteString(fmt.Sprintf("Echo: %s", message))
			_ = writer.Flush()
		}
	}()

	clientConfig := ClientConfig{
		Addr:        listener.Addr().String(),
		Messages:    2,
		Interval:    10 * time.Millisecond,
	}

	startClient(clientConfig)

	logOutput := buf.String()
	// Check if client sent and received messages
	if !strings.Contains(logOutput, "Client sent: \"Hello from client #1\"") ||
		!strings.Contains(logOutput, "Client received: \"Echo: Hello from client #1\"") ||
		!strings.Contains(logOutput, "Client sent: \"Hello from client #2\"") ||
		!strings.Contains(logOutput, "Client received: \"Echo: Hello from client #2\"") {
		t.Errorf("Client did not send/receive expected messages. Log output:\n%s", logOutput)
	}

	listener.Close()
	serverWg.Wait()
}

func TestStartClient_Timeout(t *testing.T) {
	// Capture log output to verify client messages
	var buf bytes.Buffer
	log.SetOutput(&buf)
	defer func() { log.SetOutput(os.Stderr) }() // Restore default output

	// Mock the server side using a listener that accepts but never responds
	listener, err := net.Listen("tcp", "localhost:0") // Listen on a random available port
	if err != nil {
		t.Fatalf("Failed to start mock listener: %v", err)
	}
	defer listener.Close()

	var serverWg sync.WaitGroup
	serverWg.Add(1)
	go func() {
		defer serverWg.Done()
		conn, err := listener.Accept()
		if err != nil {
			// This error can happen if listener is closed before accept
			if !strings.Contains(err.Error(), "use of closed network connection") {
				t.Errorf("Mock server accept error: %v", err)
			}
			return
		}
		defer conn.Close()
		// Do nothing, simulate server not responding
		select{<-(chan int)(nil)} // Block forever
	}()

	clientConfig := ClientConfig{
		Addr:        listener.Addr().String(),
		Messages:    1,
		Interval:    10 * time.Millisecond, // Small interval for quick test
	}

	startClient(clientConfig)

	logOutput := buf.String()
	// Check if client reported timeout
	if !strings.Contains(logOutput, "Message #1 timed out. Likely dropped or delayed too long.") {
		t.Errorf("Client did not report timeout. Log output:\n%s", logOutput)
	}

	listener.Close()
	serverWg.Wait()
}
