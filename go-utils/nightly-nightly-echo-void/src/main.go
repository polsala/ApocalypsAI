package main

import (
    "bufio"
    "flag"
    "fmt"
    "log"
    "net"
    "strconv"
    "strings"
    "sync"
    "time"
)

// startServer launches a UDP echo server on the given port.
// It runs until the provided WaitGroup is done.
func startServer(port string, wg *sync.WaitGroup) error {
    defer wg.Done()
    addr, err := net.ResolveUDPAddr("udp", ":"+port)
    if err != nil {
        return fmt.Errorf("resolve udp addr: %w", err)
    }
    conn, err := net.ListenUDP("udp", addr)
    if err != nil {
        return fmt.Errorf("listen udp: %w", err)
    }
    defer conn.Close()
    log.Printf("[server] listening on %s", conn.LocalAddr())
    buf := make([]byte, 4096)
    for {
        n, clientAddr, err := conn.ReadFromUDP(buf)
        if err != nil {
            return fmt.Errorf("read udp: %w", err)
        }
        payload := string(buf[:n])
        timestamp := time.Now().UnixNano()
        response := fmt.Sprintf("%d:%s", timestamp, payload)
        _, err = conn.WriteToUDP([]byte(response), clientAddr)
        if err != nil {
            return fmt.Errorf("write udp: %w", err)
        }
    }
}

// pingServer sends a single UDP packet to the server and returns the echoed payload.
func pingServer(address string, message string) (string, time.Duration, error) {
    serverAddr, err := net.ResolveUDPAddr("udp", address)
    if err != nil {
        return "", 0, fmt.Errorf("resolve udp addr: %w", err)
    }
    conn, err := net.DialUDP("udp", nil, serverAddr)
    if err != nil {
        return "", 0, fmt.Errorf("dial udp: %w", err)
    }
    defer conn.Close()

    start := time.Now()
    _, err = conn.Write([]byte(message))
    if err != nil {
        return "", 0, fmt.Errorf("write udp: %w", err)
    }
    conn.SetReadDeadline(time.Now().Add(2 * time.Second))
    respBuf := make([]byte, 4096)
    n, _, err := conn.ReadFromUDP(respBuf)
    if err != nil {
        return "", 0, fmt.Errorf("read udp: %w", err)
    }
    elapsed := time.Since(start)
    resp := string(respBuf[:n])
    // Expected format: "<timestamp>:<original>"
    parts := strings.SplitN(resp, ":", 2)
    if len(parts) != 2 {
        return "", elapsed, fmt.Errorf("malformed response: %s", resp)
    }
    // We ignore the timestamp here; caller can parse if needed.
    return parts[1], elapsed, nil
}

func runServer(port string) {
    var wg sync.WaitGroup
    wg.Add(1)
    go func() {
        if err := startServer(port, &wg); err != nil {
            log.Fatalf("server error: %v", err)
        }
    }()
    wg.Wait()
}

func runClient(address string, count int, message string) {
    for i := 0; i < count; i++ {
        payload, rtt, err := pingServer(address, message)
        if err != nil {
            log.Printf("ping %d failed: %v", i+1, err)
            continue
        }
        log.Printf("ping %d: echoed "%s" in %s", i+1, payload, rtt)
        // Small pause to avoid flooding
        time.Sleep(200 * time.Millisecond)
    }
}

func main() {
    mode := flag.String("mode", "", "operation mode: server or client (required)")
    port := flag.String("port", "9000", "UDP port for server mode")
    address := flag.String("address", "localhost:9000", "server address for client mode")
    count := flag.Int("count", 1, "number of messages to send (client mode)")
    message := flag.String("message", "ping", "payload to send (client mode)")
    flag.Parse()

    if *mode != "server" && *mode != "client" {
        log.Fatalf("invalid mode: %s (must be 'server' or 'client')", *mode)
    }

    if *mode == "server" {
        runServer(*port)
    } else {
        runClient(*address, *count, *message)
    }
}
