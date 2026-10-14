package main

import (
    "context"
    "flag"
    "fmt"
    "log"
    "net"
    "time"
)

func runServer(ctx context.Context, port int) error {
    addr := net.UDPAddr{IP: net.ParseIP("0.0.0.0"), Port: port}
    conn, err := net.ListenUDP("udp", &addr)
    if err != nil {
        return fmt.Errorf("listen udp: %w", err)
    }
    defer conn.Close()
    log.Printf("UDP server listening on %s", conn.LocalAddr())
    buf := make([]byte, 4096)
    for {
        select {
        case <-ctx.Done():
            return nil
        default:
        }
        n, remote, err := conn.ReadFromUDP(buf)
        if err != nil {
            log.Printf("read error: %v", err)
            continue
        }
        // Echo back concurrently
        data := make([]byte, n)
        copy(data, buf[:n])
        go func(r *net.UDPAddr, d []byte) {
            _, err := conn.WriteToUDP(d, r)
            if err != nil {
                log.Printf("write error: %v", err)
            }
        }(remote, data)
    }
}

// ping sends a single UDP packet to addr with msg and waits for the echo.
// It returns the echoed message, the round‑trip duration, and any error.
func ping(addr string, msg string) (string, time.Duration, error) {
    remote, err := net.ResolveUDPAddr("udp", addr)
    if err != nil {
        return "", 0, fmt.Errorf("resolve addr: %w", err)
    }
    conn, err := net.DialUDP("udp", nil, remote)
    if err != nil {
        return "", 0, fmt.Errorf("dial udp: %w", err)
    }
    defer conn.Close()
    start := time.Now()
    _, err = conn.Write([]byte(msg))
    if err != nil {
        return "", 0, fmt.Errorf("write: %w", err)
    }
    buf := make([]byte, 4096)
    conn.SetReadDeadline(time.Now().Add(5 * time.Second))
    n, _, err := conn.ReadFromUDP(buf)
    if err != nil {
        return "", 0, fmt.Errorf("read: %w", err)
    }
    elapsed := time.Since(start)
    return string(buf[:n]), elapsed, nil
}

func main() {
    mode := flag.String("mode", "", "mode: server or client (required)")
    port := flag.Int("port", 9000, "UDP port for server")
    addr := flag.String("addr", "", "server address for client (host:port)")
    msg := flag.String("msg", "ping", "message to send (client only)")
    flag.Parse()

    if *mode == "" {
        log.Fatal("-mode flag is required")
    }
    switch *mode {
    case "server":
        ctx, cancel := context.WithCancel(context.Background())
        defer cancel()
        if err := runServer(ctx, *port); err != nil {
            log.Fatalf("server error: %v", err)
        }
    case "client":
        if *addr == "" {
            log.Fatal("-addr flag is required in client mode")
        }
        resp, dur, err := ping(*addr, *msg)
        if err != nil {
            log.Fatalf("client error: %v", err)
        }
        fmt.Printf("Received echo: %s (RTT: %v)\n", resp, dur)
    default:
        log.Fatalf("unknown mode: %s", *mode)
    }
}
