package main

import (
    "bufio"
    "flag"
    "fmt"
    "log"
    "net"
    "os"
    "strconv"
    "strings"
    "sync"
    "time"
)

// processMessage implements the core ping‑pong logic.
// If the incoming message starts with "ping:" it returns "pong:" + payload.
// Otherwise it returns an empty string indicating no reply.
func processMessage(msg string) string {
    if strings.HasPrefix(msg, "ping:") {
        payload := strings.TrimPrefix(msg, "ping:")
        return "pong:" + payload
    }
    return ""
}

func runServer(port int) error {
    addr := net.UDPAddr{Port: port, IP: net.ParseIP("0.0.0.0")}
    conn, err := net.ListenUDP("udp", &addr)
    if err != nil {
        return err
    }
    defer conn.Close()
    log.Printf("UDP ping‑pong server listening on %s", conn.LocalAddr())

    buf := make([]byte, 1024)
    for {
        n, remoteAddr, err := conn.ReadFromUDP(buf)
        if err != nil {
            log.Printf("read error: %v", err)
            continue
        }
        incoming := strings.TrimSpace(string(buf[:n]))
        reply := processMessage(incoming)
        if reply == "" {
            // ignore non‑ping messages
            continue
        }
        _, err = conn.WriteToUDP([]byte(reply), remoteAddr)
        if err != nil {
            log.Printf("write error: %v", err)
        }
    }
}

func runClient(host string, port, count int) error {
    serverAddr := net.UDPAddr{IP: net.ParseIP(host), Port: port}
    conn, err := net.DialUDP("udp", nil, &serverAddr)
    if err != nil {
        return err
    }
    defer conn.Close()

    var wg sync.WaitGroup
    wg.Add(1)
    go func() {
        defer wg.Done()
        // Listener for responses
        respBuf := make([]byte, 1024)
        for i := 0; i < count; i++ {
            conn.SetReadDeadline(time.Now().Add(2 * time.Second))
            n, _, err := conn.ReadFromUDP(respBuf)
            if err != nil {
                fmt.Fprintf(os.Stderr, "read timeout or error: %v\n", err)
                return
            }
            fmt.Printf("Received: %s\n", strings.TrimSpace(string(respBuf[:n])))
        }
    }()

    // Send ping messages
    for i := 0; i < count; i++ {
        msg := fmt.Sprintf("ping:%d", i)
        _, err := conn.Write([]byte(msg))
        if err != nil {
            return err
        }
        time.Sleep(100 * time.Millisecond) // slight pause to avoid packet loss on localhost
    }
    wg.Wait()
    return nil
}

func main() {
    mode := flag.String("mode", "server", "Mode to run: server or client")
    host := flag.String("host", "127.0.0.1", "Server host (client mode)")
    port := flag.Int("port", 9000, "Port number")
    count := flag.Int("count", 5, "Number of ping messages (client mode)")
    flag.Parse()

    switch *mode {
    case "server":
        if err := runServer(*port); err != nil {
            log.Fatalf("Server error: %v", err)
        }
    case "client":
        if err := runClient(*host, *port, *count); err != nil {
            log.Fatalf("Client error: %v", err)
        }
    default:
        fmt.Fprintf(os.Stderr, "Invalid mode: %s\n", *mode)
        os.Exit(1)
    }
}
