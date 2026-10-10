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

// MockAddr implements net.Addr for testing
type MockAddr string

func (m MockAddr) Network() string { return "tcp" }
func (m MockAddr) String() string  { return string(m) }

// MockConn implements net.Conn for testing
type MockConn struct {
	readBuffer  bytes.Buffer
	writeBuffer bytes.Buffer
	closed      bool
	readCh      chan []byte // Channel to simulate incoming data
	closeCh     chan struct{} // Channel to signal close
	remoteAddr  net.Addr
	localAddr   net.Addr
	mu          sync.Mutex // Protects readBuffer and writeBuffer
}

func NewMockConn(remote, local string) *MockConn {
	return &MockConn{
		readCh:      make(chan []byte, 10), // Buffered channel
		closeCh:     make(chan struct{}),
		remoteAddr:  MockAddr(remote),
		localAddr:   MockAddr(local),
	}
}

func (m *MockConn) Read(b []byte) (n int, err error) {
	m.mu.Lock()
	defer m.mu.Unlock()

	if m.readBuffer.Len() > 0 {
		n, err = m.readBuffer.Read(b)
		return
	}

	select {
	case data := <-m.readCh:
		m.readBuffer.Write(data)
		n, err = m.readBuffer.Read(b)
		return
	case <-m.closeCh:
		return 0, io.EOF
	case <-time.After(50 * time.Millisecond): // Timeout for Read to prevent blocking tests indefinitely
		return 0, io.ErrNoProgress // Simulate no data available yet
	}
}

func (m *MockConn) Write(b []byte) (n int, err error) {
	m.mu.Lock()
	defer m.mu.Unlock()
	return m.writeBuffer.Write(b)
}

func (m *MockConn) Close() error {
	m.mu.Lock()
	defer m.mu.Unlock()
	if !m.closed {
		m.closed = true
		close(m.closeCh)
	}
	return nil
}

func (m *MockConn) LocalAddr() net.Addr                { return m.localAddr }
func (m *MockConn) RemoteAddr() net.Addr               { return m.remoteAddr }
func (m *MockConn) SetDeadline(t time.Time) error      { return nil }
func (m *MockConn) SetReadDeadline(t time.Time) error  { return nil }
func (m *MockConn) SetWriteDeadline(t time.Time) error { return nil }

// InjectReadData allows tests to push data into the mock connection's read buffer
func (m *MockConn) InjectReadData(data []byte) {
	m.readCh <- data
}

// GetWrittenData retrieves data written to the mock connection
func (m *MockConn) GetWrittenData() string {
	m.mu.Lock()
	defer m.mu.Unlock()
	return m.writeBuffer.String()
}

// MockListener implements net.Listener for testing
type MockListener struct {
	acceptCh chan net.Conn // Channel to queue mock connections
	closeCh  chan struct{}
	addr     net.Addr
	closed   bool
}

func NewMockListener(addr string) *MockListener {
	return &MockListener{
		acceptCh: make(chan net.Conn, 10),
		closeCh:  make(chan struct{}),
		addr:     MockAddr(addr),
	}
}

func (m *MockListener) Accept() (net.Conn, error) {
	select {
	case conn := <-m.acceptCh:
		return conn, nil
	case <-m.closeCh:
		return nil, io.EOF
	}
}

func (m *MockListener) Close() error {
	if !m.closed {
		m.closed = true
		close(m.closeCh)
		close(m.acceptCh) // Close the accept channel
	}
	return nil
}

func (m *MockListener) Addr() net.Addr { return m.addr }

// InjectConn allows tests to push mock connections into the listener
func (m *MockListener) InjectConn(conn net.Conn) {
	m.acceptCh <- conn
}

// # Mock rationale:
// Network operations are inherently non-deterministic and require external resources.
// Mocking net.Conn and net.Listener allows testing the server's internal logic
// (client management, message processing, broadcasting, delays) without actual network I/O,
// ensuring deterministic and fast tests.

func TestEchoServer_StartAndStop(t *testing.T) {
	listener := NewMockListener("127.0.0.1:8080")
	server := &EchoServer{
		listener:    listener,
		messages:    make(chan string, 10),
		minDelay:    1 * time.Millisecond, // Use minimal delays for tests
		maxDelay:    1 * time.Millisecond,
		distortMsgs: false,
		shutdown:    make(chan struct{}),
	}

	server.Start()

	// Give some time for goroutines to start
	time.Sleep(50 * time.Millisecond)

	server.Stop()

	// Verify listener is closed
	_, err := listener.Accept()
	if err != io.EOF {
		t.Errorf("Expected listener to be closed, got %v", err)
	}
}

func TestEchoServer_SingleClientEcho(t *testing.T) {
	listener := NewMockListener("127.0.0.1:8080")
	server := &EchoServer{
		listener:    listener,
		messages:    make(chan string, 10),
		minDelay:    1 * time.Millisecond,
		maxDelay:    1 * time.Millisecond,
		distortMsgs: false,
		shutdown:    make(chan struct{}),
	}
	server.Start()
	defer server.Stop()

	clientConn := NewMockConn("127.0.0.1:12345", "127.0.0.1:8080")
	listener.InjectConn(clientConn)

	// Give server time to accept client
	time.Sleep(50 * time.Millisecond)

	testMessage := "Hello, Temporal Echo!\n"
	clientConn.InjectReadData([]byte(testMessage))

	// Wait for message to be processed and echoed
	time.Sleep(100 * time.Millisecond)

	expectedEcho := fmt.Sprintf("[%s] %s\n", clientConn.RemoteAddr().String(), strings.TrimSpace(testMessage))

	actualWritten := clientConn.GetWrittenData()
	if !strings.Contains(actualWritten, expectedEcho) {
		t.Errorf("Expected client to receive '%s', got '%s'", expectedEcho, actualWritten)
	}
}

func TestEchoServer_MultipleClientsBroadcast(t *testing.T) {
	listener := NewMockListener("127.0.0.1:8080")
	server := &EchoServer{
		listener:    listener,
		messages:    make(chan string, 10),
		minDelay:    1 * time.Millisecond,
		maxDelay:    1 * time.Millisecond,
		distortMsgs: false,
		shutdown:    make(chan struct{}),
	}
	server.Start()
	defer server.Stop()

	client1Conn := NewMockConn("127.0.0.1:12345", "127.0.0.1:8080")
	client2Conn := NewMockConn("127.0.0.1:12346", "127.0.0.1:8080")

	listener.InjectConn(client1Conn)
	listener.InjectConn(client2Conn)

	// Give server time to accept clients
	time.Sleep(50 * time.Millisecond)

	testMessage := "Broadcast this!\n"
	client1Conn.InjectReadData([]byte(testMessage))

	// Wait for message to be processed and echoed
	time.Sleep(100 * time.Millisecond)

	expectedEcho := fmt.Sprintf("[%s] %s\n", client1Conn.RemoteAddr().String(), strings.TrimSpace(testMessage))

	// Verify client 1 received the message
	actualWritten1 := client1Conn.GetWrittenData()
	if !strings.Contains(actualWritten1, expectedEcho) {
		t.Errorf("Client 1: Expected to receive '%s', got '%s'", expectedEcho, actualWritten1)
	}

	// Verify client 2 received the message
	actualWritten2 := client2Conn.GetWrittenData()
	if !strings.Contains(actualWritten2, expectedEcho) {
		t.Errorf("Client 2: Expected to receive '%s', got '%s'", expectedEcho, actualWritten2)
	}
}

func TestEchoServer_Distortion(t *testing.T) {
	listener := NewMockListener("127.0.0.1:8080")
	server := &EchoServer{
		listener:    listener,
		messages:    make(chan string, 10),
		minDelay:    1 * time.Millisecond,
		maxDelay:    1 * time.Millisecond,
		distortMsgs: true, // Enable distortion
		shutdown:    make(chan struct{}),
	}
	server.Start()
	defer server.Stop()

	clientConn := NewMockConn("127.0.0.1:12345", "127.0.0.1:8080")
	listener.InjectConn(clientConn)

	// Give server time to accept client
	time.Sleep(50 * time.Millisecond)

	originalMessage := "Distort Me!\n"
	clientConn.InjectReadData([]byte(originalMessage))

	// Wait for message to be processed and echoed
	time.Sleep(100 * time.Millisecond)

	// The distortion function reverses the string
	distortedMessage := distortMessage(strings.TrimSpace(originalMessage))
	expectedEcho := fmt.Sprintf("[%s] %s\n", clientConn.RemoteAddr().String(), distortedMessage)

	actualWritten := clientConn.GetWrittenData()
	if !strings.Contains(actualWritten, expectedEcho) {
		t.Errorf("Expected client to receive distorted message '%s', got '%s'", expectedEcho, actualWritten)
	}
}

func TestEchoServer_ClientDisconnect(t *testing.T) {
	listener := NewMockListener("127.0.0.1:8080")
	server := &EchoServer{
		listener:    listener,
		messages:    make(chan string, 10),
		minDelay:    1 * time.Millisecond,
		maxDelay:    1 * time.Millisecond,
		distortMsgs: false,
		shutdown:    make(chan struct{}),
	}
	server.Start()
	defer server.Stop()

	clientConn := NewMockConn("127.0.0.1:12345", "127.0.0.1:8080")
	listener.InjectConn(clientConn)

	// Give server time to accept client
	time.Sleep(50 * time.Millisecond)

	// Verify client is connected
	if _, ok := server.clients.Load(clientConn.RemoteAddr().String()); !ok {
		t.Fatal("Client not registered after connection")
	}

	// Simulate client disconnection
	clientConn.Close()

	// Give server time to process disconnection
	time.Sleep(100 * time.Millisecond)

	// Verify client is removed from map
	if _, ok := server.clients.Load(clientConn.RemoteAddr().String()); ok {
		t.Errorf("Client %s was not removed from server.clients after disconnection", clientConn.RemoteAddr().String())
	}
}
