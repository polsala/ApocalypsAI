package main

import (
	"bytes"
	"fmt"
	"io"
	"net"
	"strings"
	"sync"
	"testing"
	"time"
)

// Mock rationale: We need to simulate network connections and data transfer without actually binding to ports or sending real network traffic. This ensures tests are fast, deterministic, and isolated from the network environment.
type MockConn struct {
	readBuffer  bytes.Buffer
	writeBuffer bytes.Buffer
	closed      bool
	mu          sync.Mutex
	remoteAddr  net.Addr // Store the remote address
}

func NewMockConn(ip string, port int) *MockConn {
	return &MockConn{
		remoteAddr: &net.TCPAddr{IP: net.ParseIP(ip), Port: port},
	}
}

func (m *MockConn) Read(b []byte) (n int, err error) {
	m.mu.Lock()
	defer m.mu.Unlock()
	if m.closed {
		return 0, io.EOF
	}
	return m.readBuffer.Read(b)
}

func (m *MockConn) Write(b []byte) (n int, err error) {
	m.mu.Lock()
	defer m.mu.Unlock()
	if m.closed {
		return 0, io.ErrClosedPipe
	}
	return m.writeBuffer.Write(b)
}

func (m *MockConn) Close() error {
	m.mu.Lock()
	defer m.mu.Unlock()
	m.closed = true
	return nil
}

func (m *MockConn) LocalAddr() net.Addr { return &net.TCPAddr{IP: net.ParseIP("127.0.0.1"), Port: 12345} }
func (m *MockConn) RemoteAddr() net.Addr { return m.remoteAddr }
func (m *MockConn) SetDeadline(t time.Time) error { return nil }
func (m *MockConn) SetReadDeadline(t time.Time) error { return nil }
func (m *MockConn) SetWriteDeadline(t time.Time) error { return nil }

// Helper to get written content
func (m *MockConn) GetWritten() string {
	m.mu.Lock()
	defer m.mu.Unlock()
	return m.writeBuffer.String()
}

// Helper to simulate incoming data
func (m *MockConn) SimulateIncoming(data string) {
	m.mu.Lock()
	defer m.mu.Unlock()
	m.readBuffer.WriteString(data)
}

// Mock rationale: We need to simulate a network listener accepting connections without actually binding to a port. This allows us to control when connections are "accepted" and what mock connections are returned.
type MockListener struct {
	acceptCh chan net.Conn
	closeCh  chan struct{}
	closed   bool
	mu       sync.Mutex
}

func NewMockListener() *MockListener {
	return &MockListener{
		acceptCh: make(chan net.Conn),
		closeCh:  make(chan struct{}),
	}
}

func (m *MockListener) Accept() (net.Conn, error) {
	select {
	case conn := <-m.acceptCh:
		return conn, nil
	case <-m.closeCh:
		return nil, io.EOF // Simulate listener closed
	}
}

func (m *MockListener) Close() error {
	m.mu.Lock()
	defer m.mu.Unlock()
	if !m.closed {
		close(m.closeCh)
		m.closed = true
	}
	return nil
}

func (m *MockListener) Addr() net.Addr { return &net.TCPAddr{IP: net.ParseIP("127.0.0.1"), Port: 0} } // Port 0 for mock

// Helper to simulate an incoming connection
func (m *MockListener) SimulateAccept(conn net.Conn) {
	m.acceptCh <- conn
}

func TestServer_SignalAmplification(t *testing.T) {
	ml := NewMockListener()
	server := NewServer(ml)
	go server.Start()
	defer server.Stop()

	client1Conn := NewMockConn("127.0.0.1", 10001)
	client2Conn := NewMockConn("127.0.0.1", 10002)

	ml.SimulateAccept(client1Conn)
	ml.SimulateAccept(client2Conn)

	// Give server time to register clients
	time.Sleep(100 * time.Millisecond)

	// Client 1 sends a signal
	client1Conn.SimulateIncoming(SignalKeyword + "\n")

	// Wait for broadcast to happen
	time.Sleep(200 * time.Millisecond)

	// Check if both clients received an amplified message
	output1 := client1Conn.GetWritten()
	output2 := client2Conn.GetWritten()

	if !strings.Contains(output1, "✨ AMPLIFIED SIGNAL DETECTED! ✨") {
		t.Errorf("Client 1 did not receive amplified signal. Output:\n%s", output1)
	}
	if !strings.Contains(output2, "✨ AMPLIFIED SIGNAL DETECTED! ✨") {
		t.Errorf("Client 2 did not receive amplified signal. Output:\n%s", output2)
	}

	if !strings.Contains(output1, "(from 127.0.0.1:10001)") {
		t.Errorf("Client 1's output missing sender info. Output:\n%s", output1)
	}
	if !strings.Contains(output2, "(from 127.0.0.1:10001)") {
		t.Errorf("Client 2's output missing sender info. Output:\n%s", output2)
	}

	// Ensure the non-sender also received the message
	if output1 == "" || output2 == "" {
		t.Errorf("One or both clients received no output. Client 1: '%s', Client 2: '%s'", output1, output2)
	}
}

func TestServer_NonSignalMessage(t *testing.T) {
	ml := NewMockListener()
	server := NewServer(ml)
	go server.Start()
	defer server.Stop()

	clientConn := NewMockConn("127.0.0.1", 10003)
	ml.SimulateAccept(clientConn)

	time.Sleep(100 * time.Millisecond)

	nonSignal := "Hello, void!\n"
	clientConn.SimulateIncoming(nonSignal)

	time.Sleep(100 * time.Millisecond)

	output := clientConn.GetWritten()
	if !strings.Contains(output, "Starlight Amplifier received: Hello, void!") {
		t.Errorf("Server did not echo non-signal message. Output:\n%s", output)
	}
	if strings.Contains(output, "✨ AMPLIFIED SIGNAL DETECTED! ✨") {
		t.Errorf("Server incorrectly amplified a non-signal message. Output:\n%s", output)
	}
}

func TestServer_ClientDisconnect(t *testing.T) {
	ml := NewMockListener()
	server := NewServer(ml)
	go server.Start()
	defer server.Stop()

	clientConn := NewMockConn("127.0.0.1", 10004)
	ml.SimulateAccept(clientConn)

	time.Sleep(100 * time.Millisecond)

	// Simulate client sending a message then closing
	clientConn.SimulateIncoming("Test message\n")
	clientConn.Close() // Simulate client closing its connection

	time.Sleep(200 * time.Millisecond) // Give server time to process disconnect

	server.mu.Lock()
	numClients := len(server.clients)
	server.mu.Unlock()

	if numClients != 0 {
		t.Errorf("Expected 0 clients after disconnect, got %d", numClients)
	}
}

func TestServer_MultipleClientsAndSignals(t *testing.T) {
	ml := NewMockListener()
	server := NewServer(ml)
	go server.Start()
	defer server.Stop()

	clientA := NewMockConn("127.0.0.1", 20001)
	clientB := NewMockConn("127.0.0.1", 20002)
	clientC := NewMockConn("127.0.0.1", 20003)

	ml.SimulateAccept(clientA)
	ml.SimulateAccept(clientB)
	ml.SimulateAccept(clientC)

	time.Sleep(100 * time.Millisecond) // Allow clients to connect

	clientA.SimulateIncoming(SignalKeyword + "\n")
	time.Sleep(100 * time.Millisecond)
	clientB.SimulateIncoming("Just chatting\n")
	time.Sleep(100 * time.Millisecond)
	clientC.SimulateIncoming("ANOTHER " + SignalKeyword + " HERE\n")
	time.Sleep(200 * time.Millisecond) // Wait for all broadcasts

	// Check client A's output
	outputA := clientA.GetWritten()
	if !strings.Contains(outputA, "✨ AMPLIFIED SIGNAL DETECTED! ✨") {
		t.Errorf("Client A did not receive amplified signal. Output:\n%s", outputA)
	}
	if !strings.Contains(outputA, "Starlight Amplifier received: Just chatting") {
		t.Errorf("Client A did not receive echo. Output:\n%s", outputA)
	}
	if strings.Count(outputA, "✨ AMPLIFIED SIGNAL DETECTED! ✨") != 2 {
		t.Errorf("Client A received incorrect number of amplified signals. Expected 2, got %d. Output:\n%s", strings.Count(outputA, "✨ AMPLIFIED SIGNAL DETECTED! ✨"), outputA)
	}

	// Check client B's output
	outputB := clientB.GetWritten()
	if !strings.Contains(outputB, "✨ AMPLIFIED SIGNAL DETECTED! ✨") {
		t.Errorf("Client B did not receive amplified signal. Output:\n%s", outputB)
	}
	if strings.Count(outputB, "✨ AMPLIFIED SIGNAL DETECTED! ✨") != 2 {
		t.Errorf("Client B received incorrect number of amplified signals. Expected 2, got %d. Output:\n%s", strings.Count(outputB, "✨ AMPLIFIED SIGNAL DETECTED! ✨"), outputB)
	}
	if !strings.Contains(outputB, "Starlight Amplifier received: Just chatting") {
		t.Errorf("Client B did not receive echo. Output:\n%s", outputB)
	}

	// Check client C's output
	outputC := clientC.GetWritten()
	if !strings.Contains(outputC, "✨ AMPLIFIED SIGNAL DETECTED! ✨") {
		t.Errorf("Client C did not receive amplified signal. Output:\n%s", outputC)
	}
	if strings.Count(outputC, "✨ AMPLIFIED SIGNAL DETECTED! ✨") != 2 {
		t.Errorf("Client C received incorrect number of amplified signals. Expected 2, got %d. Output:\n%s", strings.Count(outputC, "✨ AMPLIFIED SIGNAL DETECTED! ✨"), outputC)
	}
}

func TestServer_Stop(t *testing.T) {
	ml := NewMockListener()
	server := NewServer(ml)
	go server.Start()

	clientConn := NewMockConn("127.0.0.1", 10005)
	ml.SimulateAccept(clientConn)
	time.Sleep(100 * time.Millisecond) // Allow client to connect

	server.Stop()
	time.Sleep(100 * time.Millisecond) // Give time for goroutines to exit

	server.mu.Lock()
	numClients := len(server.clients)
	server.mu.Unlock()

	if numClients != 0 {
		t.Errorf("Expected 0 clients after server stop, got %d", numClients)
	}

	// Verify listener is closed (Accept should return error)
	_, err := ml.Accept()
	if err != io.EOF {
		t.Errorf("Expected listener to be closed (io.EOF), got %v", err)
	}

	// Verify broadcast channel is closed (sending should panic or block if not closed)
	select {
	case _, ok := <-server.broadcastCh:
		if ok {
			t.Error("Broadcast channel is still open after server stop")
		}
	case <-time.After(50 * time.Millisecond):
		t.Error("Broadcast channel did not close in time")
	}
}
