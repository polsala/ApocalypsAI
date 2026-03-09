package main

import (
    "errors"
    "io"
    "net"
    "strings"
    "testing"
    "time"
)

// mockConn implements net.Conn for testing purposes.
type mockConn struct {
    response string
    readPos  int
    closed   bool
}

func (m *mockConn) Read(b []byte) (int, error) {
    if m.readPos >= len(m.response) {
        return 0, io.EOF
    }
    n := copy(b, m.response[m.readPos:])
    m.readPos += n
    return n, nil
}

func (m *mockConn) Write(b []byte) (int, error) { return len(b), nil }
func (m *mockConn) Close() error               { m.closed = true; return nil }
func (m *mockConn) LocalAddr() net.Addr        { return nil }
func (m *mockConn) RemoteAddr() net.Addr       { return nil }
func (m *mockConn) SetDeadline(t time.Time) error      { return nil }
func (m *mockConn) SetReadDeadline(t time.Time) error  { return nil }
func (m *mockConn) SetWriteDeadline(t time.Time) error { return nil }

// mockDialer returns a mockConn whose response is predetermined based on the address.
func mockDialer(responses map[string]string) Dialer {
    return func(network, address string) (net.Conn, error) {
        if resp, ok := responses[address]; ok {
            return &mockConn{response: resp}, nil
        }
        return nil, errors.New("connection refused")
    }
}

func TestScanHostFound(t *testing.T) {
    responses := map[string]string{
        "host1:8080": "Welcome SURVIVE here!",
    }
    dial := mockDialer(responses)
    found, err := scanHost(dial, "host1", "8080", "SURVIVE", 1*time.Second)
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
    if !found {
        t.Fatalf("expected keyword to be found")
    }
}

func TestScanHostNotFound(t *testing.T) {
    responses := map[string]string{
        "host2:8080": "No beacon here.",
    }
    dial := mockDialer(responses)
    found, err := scanHost(dial, "host2", "8080", "SURVIVE", 1*time.Second)
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
    if found {
        t.Fatalf("expected keyword NOT to be found")
    }
}

func TestScanHostError(t *testing.T) {
    responses := map[string]string{}
    dial := mockDialer(responses)
    _, err := scanHost(dial, "unknown", "8080", "SURVIVE", 1*time.Second)
    if err == nil {
        t.Fatalf("expected an error for unknown host")
    }
    if !strings.Contains(err.Error(), "connection refused") {
        t.Fatalf("unexpected error message: %v", err)
    }
}
