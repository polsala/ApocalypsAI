package main

import (
    "bufio"
    "flag"
    "fmt"
    "math/rand"
    "net"
    "os"
    "strings"
    "sync"
    "time"
)

var defaultQuotes = []string{
    "The only limit to our realization of tomorrow is our doubts of today.",
    "Life is what happens when you're busy making other plans.",
    "The purpose of our lives is to be happy.",
    "In the middle of difficulty lies opportunity.",
    "Do not watch the clock. Do what it does. Keep going.",
}

func loadQuotes(path string) ([]string, error) {
    if path == "" {
        return defaultQuotes, nil
    }
    file, err := os.Open(path)
    if err != nil {
        return nil, err
    }
    defer file.Close()
    var quotes []string
    scanner := bufio.NewScanner(file)
    for scanner.Scan() {
        line := strings.TrimSpace(scanner.Text())
        if line != "" {
            quotes = append(quotes, line)
        }
    }
    if err := scanner.Err(); err != nil {
        return nil, err
    }
    if len(quotes) == 0 {
        return defaultQuotes, nil
    }
    return quotes, nil
}

func pickRandomQuote(quotes []string) string {
    if len(quotes) == 0 {
        return ""
    }
    idx := rand.Intn(len(quotes))
    return quotes[idx]
}

// broadcastQuote sends a single quote over the provided UDP connection.
func broadcastQuote(conn *net.UDPConn, addr *net.UDPAddr, quote string) error {
    _, err := conn.WriteToUDP([]byte(quote), addr)
    return err
}

func broadcastLoop(conn *net.UDPConn, addr *net.UDPAddr, quotes []string, interval time.Duration, stop <-chan struct{}, wg *sync.WaitGroup) {
    defer wg.Done()
    ticker := time.NewTicker(interval)
    defer ticker.Stop()
    for {
        select {
        case <-stop:
            return
        case <-ticker.C:
            q := pickRandomQuote(quotes)
            if err := broadcastQuote(conn, addr, q); err != nil {
                fmt.Fprintf(os.Stderr, "broadcast error: %v\n", err)
                continue
            }
            fmt.Printf("[%s] Sent: \"%s\"\n", time.Now().UTC().Format(time.RFC3339), q)
        }
    }
}

func listenLoop(conn *net.UDPConn, stop <-chan struct{}, wg *sync.WaitGroup) {
    defer wg.Done()
    buf := make([]byte, 4096)
    for {
        conn.SetReadDeadline(time.Now().Add(500 * time.Millisecond))
        n, _, err := conn.ReadFromUDP(buf)
        if err != nil {
            if ne, ok := err.(net.Error); ok && ne.Timeout() {
                select {
                case <-stop:
                    return
                default:
                    continue
                }
            }
            fmt.Fprintf(os.Stderr, "listen error: %v\n", err)
            continue
        }
        msg := strings.TrimSpace(string(buf[:n]))
        fmt.Printf("[%s] Received: \"%s\"\n", time.Now().UTC().Format(time.RFC3339), msg)
    }
}

func main() {
    port := flag.Int("port", 9999, "UDP port to use for broadcasting and listening")
    interval := flag.Int("interval", 10, "Seconds between broadcasts")
    quotesFile := flag.String("quotes-file", "", "Path to a file containing quotes (one per line)")
    flag.Parse()

    rand.Seed(time.Now().UnixNano())

    quotes, err := loadQuotes(*quotesFile)
    if err != nil {
        fmt.Fprintf(os.Stderr, "failed to load quotes: %v\n", err)
        os.Exit(1)
    }

    addr, err := net.ResolveUDPAddr("udp", fmt.Sprintf("127.0.0.1:%d", *port))
    if err != nil {
        fmt.Fprintf(os.Stderr, "failed to resolve address: %v\n", err)
        os.Exit(1)
    }

    // Listen on the same address for incoming quotes.
    listenConn, err := net.ListenUDP("udp", addr)
    if err != nil {
        fmt.Fprintf(os.Stderr, "failed to listen on UDP: %v\n", err)
        os.Exit(1)
    }
    defer listenConn.Close()

    // For sending we can reuse the same connection.
    sendConn, err := net.DialUDP("udp", nil, addr)
    if err != nil {
        fmt.Fprintf(os.Stderr, "failed to dial UDP: %v\n", err)
        os.Exit(1)
    }
    defer sendConn.Close()

    stop := make(chan struct{})
    var wg sync.WaitGroup
    wg.Add(2)
    go listenLoop(listenConn, stop, &wg)
    go broadcastLoop(sendConn, addr, quotes, time.Duration(*interval)*time.Second, stop, &wg)

    // Run until interrupted.
    sig := make(chan os.Signal, 1)
    // Note: we avoid importing "os/signal" to keep deps minimal; use a simple sleep for demo.
    fmt.Println("Quote broadcaster running. Press Ctrl+C to stop.")
    select {}
    // In real usage we would capture SIGINT/SIGTERM and then close(stop).
    // close(stop)
    // wg.Wait()
}
