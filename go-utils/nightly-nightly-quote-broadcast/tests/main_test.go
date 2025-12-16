package main

import (
    "io/ioutil"
    "net"
    "os"
    "strings"
    "testing"
    "time"
)

func TestLoadQuotesFromFile(t *testing.T) {
    // Mock rationale: create a temporary file with known quotes.
    content := "First quote\nSecond quote\n"
    tmp, err := ioutil.TempFile("", "quotes-*.txt")
    if err != nil {
        t.Fatalf("temp file creation failed: %v", err)
    }
    defer os.Remove(tmp.Name())
    if _, err := tmp.WriteString(content); err != nil {
        t.Fatalf("write failed: %v", err)
    }
    tmp.Close()

    quotes, err := loadQuotes(tmp.Name())
    if err != nil {
        t.Fatalf("loadQuotes returned error: %v", err)
    }
    if len(quotes) != 2 {
        t.Fatalf("expected 2 quotes, got %d", len(quotes))
    }
    if quotes[0] != "First quote" || quotes[1] != "Second quote" {
        t.Fatalf("quotes content mismatch: %v", quotes)
    }
}

func TestBroadcastAndReceive(t *testing.T) {
    // Mock rationale: set up a UDP listener on a random port and send a known message.
    listenAddr, err := net.ResolveUDPAddr("udp", "127.0.0.1:0")
    if err != nil {
        t.Fatalf("resolve failed: %v", err)
    }
    listenConn, err := net.ListenUDP("udp", listenAddr)
    if err != nil {
        t.Fatalf("listen failed: %v", err)
    }
    defer listenConn.Close()
    actualPort := listenConn.LocalAddr().(*net.UDPAddr).Port

    sendAddr, err := net.ResolveUDPAddr("udp", "127.0.0.1:"+strconv.Itoa(actualPort))
    if err != nil {
        t.Fatalf("resolve send addr failed: %v", err)
    }
    sendConn, err := net.DialUDP("udp", nil, sendAddr)
    if err != nil {
        t.Fatalf("dial failed: %v", err)
    }
    defer sendConn.Close()

    testMsg := "Test Quote"
    if err := broadcastQuote(sendConn, sendAddr, testMsg); err != nil {
        t.Fatalf("broadcastQuote error: %v", err)
    }

    buf := make([]byte, 1024)
    listenConn.SetReadDeadline(time.Now().Add(2 * time.Second))
    n, _, err := listenConn.ReadFromUDP(buf)
    if err != nil {
        t.Fatalf("read failed: %v", err)
    }
    received := strings.TrimSpace(string(buf[:n]))
    if received != testMsg {
        t.Fatalf("expected %q, got %q", testMsg, received)
    }
}
