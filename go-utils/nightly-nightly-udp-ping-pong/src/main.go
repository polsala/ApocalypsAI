package main

import (
    "bufio"
    "errors"
    "flag"
    "fmt"
    "net"
    "os"
    "strconv"
    "strings"
    "sync"
    "time"
)

// formatPingMessage creates a ping payload with a sequence number.
func formatPingMessage(seq int) string {
    return fmt.Sprintf("Ping:%d", seq)
}

// parsePongMessage extracts the sequence number from a pong response.
func parsePongMessage(msg string) (int, error) {
    if !strings.HasPrefix(msg, "Pong:") {
        return 0, errors.New("invalid pong prefix")
    }
    parts := strings.SplitN(msg, ":", 2)
    if len(parts) != 2 {
        return 0, errors.New("malformed pong message")
    }
    return strconv.Atoi(parts[1])
}

func runServer(listenAddr string) error {
    addr, err := net.ResolveUDPAddr("udp", listenAddr)
    if err != nil {
        return err
    }
    conn, err := net.ListenUDP("udp", addr)
    if err != nil {
        return err
    }
    defer conn.Close()
    fmt.Printf("[server] listening on %s\n", listenAddr)
    var wg sync.WaitGroup
    buf := make([]byte, 1024)
    for {
        n, clientAddr, err := conn.ReadFromUDP(buf)
        if err != nil {
            fmt.Fprintf(os.Stderr, "read error: %v\n", err)
            continue
        }
        data := make([]byte, n)
        copy(data, buf[:n])
        wg.Add(1)
        go func(payload []byte, addr *net.UDPAddr) {
            defer wg.Done()
            // Echo back with "Pong:" prefix
            response := []byte("Pong:" + string(payload))
            _, err := conn.WriteToUDP(response, addr)
            if err != nil {
                fmt.Fprintf(os.Stderr, "write error: %v\n", err)
            }
        }(data, clientAddr)
    }
    // wg.Wait() // unreachable, kept for completeness
}

func runClient(target string, count int, interval time.Duration) error {
    serverAddr, err := net.ResolveUDPAddr("udp", target)
    if err != nil {
        return err
    }
    localAddr, err := net.ResolveUDPAddr("udp", "0.0.0.0:0")
    if err != nil {
        return err
    }
    conn, err := net.DialUDP("udp", localAddr, serverAddr)
    if err != nil {
        return err
    }
    defer conn.Close()

    var latencies []time.Duration
    reader := bufio.NewReader(conn)
    for i := 1; i <= count; i++ {
        msg := formatPingMessage(i)
        start := time.Now()
        _, err := conn.Write([]byte(msg))
        if err != nil {
            return err
        }
        // Set a read deadline to avoid hanging forever
        conn.SetReadDeadline(time.Now().Add(2 * time.Second))
        respBuf := make([]byte, 1024)
        n, _, err := conn.ReadFromUDP(respBuf)
        if err != nil {
            fmt.Printf("Ping %d timed out\n", i)
            continue
        }
        elapsed := time.Since(start)
        latencies = append(latencies, elapsed)
        resp := string(respBuf[:n])
        seq, err := parsePongMessage(resp)
        if err != nil {
            fmt.Printf("Invalid pong: %v\n", err)
            continue
        }
        fmt.Printf("Ping %d -> Pong %d : %v\n", i, seq, elapsed)
        if i < count {
            time.Sleep(interval)
        }
    }
    if len(latencies) == 0 {
        fmt.Println("No successful pings.")
        return nil
    }
    // Compute stats
    var sum, min, max time.Duration
    min = latencies[0]
    max = latencies[0]
    for _, l := range latencies {
        sum += l
        if l < min {
            min = l
        }
        if l > max {
            max = l
        }
    }
    avg := time.Duration(int64(sum) / int64(len(latencies)))
    fmt.Printf("\n--- Summary ---\n")
    fmt.Printf("Sent: %d, Received: %d\n", count, len(latencies))
    fmt.Printf("Min: %v, Max: %v, Avg: %v\n", min, max, avg)
    return nil
}

func main() {
    mode := flag.String("mode", "client", "Mode to run: server or client")
    listen := flag.String("listen", ":9000", "[server] address to listen on")
    target := flag.String("target", "localhost:9000", "[client] server address")
    count := flag.Int("count", 5, "[client] number of pings to send")
    interval := flag.Duration("interval", time.Second, "[client] pause between pings")
    flag.Parse()

    switch *mode {
    case "server":
        if err := runServer(*listen); err != nil {
            fmt.Fprintf(os.Stderr, "Server error: %v\n", err)
            os.Exit(1)
        }
    case "client":
        if err := runClient(*target, *count, *interval); err != nil {
            fmt.Fprintf(os.Stderr, "Client error: %v\n", err)
            os.Exit(1)
        }
    default:
        fmt.Fprintf(os.Stderr, "Invalid mode: %s (must be 'server' or 'client')\n", *mode)
        os.Exit(1)
    }
}
