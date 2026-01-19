package tests

import (
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

// Mock rationale: We simulate a TCP echo server to test our proxy logic without external dependencies.
func TestTCPProxy(t *testing.T) {
	// Start mock echo server
	echoAddr := startEchoServer(t)

	// Start proxy pointing to echo server
	proxyAddr := startProxy(t, echoAddr)

	// Connect to proxy and send test message
	conn, err := net.Dial("tcp", proxyAddr)
	if err != nil {
		t.Fatalf("Failed to connect to proxy: %v", err)
	}
	defer conn.Close()

	msg := "Hello, Wasteland!"
	_, err = conn.Write([]byte(msg))
	if err != nil {
		t.Fatalf("Failed to write to proxy: %v", err)
	}

	// Allow time for message to echo back
	time.Sleep(100 * time.Millisecond)

	// Read response
	buf := make([]byte, len(msg))
	_, err = conn.Read(buf)
	if err != nil && err != io.EOF {
		t.Fatalf("Failed to read from proxy: %v", err)
	}

	if string(buf) != msg {
		t.Errorf("Expected %q, got %q", msg, string(buf))
	}
}

func startEchoServer(t *testing.T) string {
	listener, err := net.Listen("tcp", "127.0.0.1:0")
	if err != nil {
		t.Fatal(err)
	}

	go func() {
		defer listener.Close()
		for {
			conn, err := listener.Accept()
			if err != nil {
				return
			}
			go func(c net.Conn) {
				io.Copy(c, c)
				c.Close()
			}(conn)
		}
	}()

	return listener.Addr().String()
}

func startProxy(t *testing.T, targetAddr string) string {
	listener, err := net.Listen("tcp", "127.0.0.1:0")
	if err != nil {
		t.Fatal(err)
	}

	var wg sync.WaitGroup
	go func() {
		defer listener.Close()
		for {
			conn, err := listener.Accept()
			if err != nil {
				return
			}
			wg.Add(1)
			go func(c net.Conn) {
				defer wg.Done()
				handleMockConnection(c, targetAddr)
			}(conn)
		}
	}()

	t.Cleanup(func() {
		listener.Close()
		wg.Wait()
	})

	return listener.Addr().String()
}

func handleMockConnection(clientConn net.Conn, targetAddr string) {
	serverConn, err := net.Dial("tcp", targetAddr)
	if err != nil {
		log.Printf("Failed to connect to target %s: %v", targetAddr, err)
		clientConn.Close()
		return
	}

	var wg sync.WaitGroup
	wg.Add(2)

	copyConn := func(dst, src net.Conn) {
		defer wg.Done()
		io.Copy(dst, src)
		dst.Close()
		src.Close()
	}

	go copyConn(serverConn, clientConn)
	go copyConn(clientConn, serverConn)

	wg.Wait()
}
