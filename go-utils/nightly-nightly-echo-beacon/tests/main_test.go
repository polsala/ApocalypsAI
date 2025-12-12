package main

import (
    "errors"
    "net"
    "testing"
    "time"
)

// MockNetwork simulates a UDP connection for deterministic tests.
// # Mock rationale: avoid real sockets and provide controlled read/write behavior.
type MockNetwork struct {
    written []byte
    readMsg []byte
    closed  bool
}

func (m *MockNetwork) WriteTo(b []byte, addr *net.UDPAddr) (int, error) {
    if m.closed {
        return 0, errors.New("closed")
    }
    m.written = append([]byte{}, b...)
    return len(b), nil
}

func (m *MockNetwork) ReadFrom(b []byte) (int, *net.UDPAddr, error) {
    if m.closed {
        return 0, nil, errors.New("closed")
    }
    copy(b, m.readMsg)
    return len(m.readMsg), &net.UDPAddr{}, nil
}

func (m *MockNetwork) Close() error {
    m.closed = true
    return nil
}

// Test that Broadcast writes the correct message.
func TestBroadcastWritesMessage(t *testing.T) {
    mock := &MockNetwork{}
    go func() {
        // Stop after first write
        time.Sleep(1100 * time.Millisecond)
        mock.Close()
    }()
    err := Broadcast("testmsg", 1234, mock)
    if err != nil && err.Error() != "closed" {
        t.Fatalf("unexpected error: %v", err)
    }
    if string(mock.written) != "testmsg" {
        t.Fatalf("expected 'testmsg', got %s", string(mock.written))
    }
}

// Test that Listen receives a message and forwards it.
func TestListenReceivesMessage(t *testing.T) {
    mock := &MockNetwork{readMsg: []byte("hello")}
    out := make(chan string, 1)
    go func() {
        err := Listen(1234, mock, out)
        if err != nil && err.Error() != "closed" {
            t.Fatalf("listen error: %v", err)
        }
    }()
    // Give goroutine time to read
    time.Sleep(100 * time.Millisecond)
    mock.Close()
    select {
    case msg := <-out:
        if msg != "hello" {
            t.Fatalf("expected 'hello', got %s", msg)
        }
    default:
        t.Fatalf("no message received")
    }
}
