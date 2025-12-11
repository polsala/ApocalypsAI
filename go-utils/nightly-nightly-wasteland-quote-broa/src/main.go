package main

import (
    "bufio"
    "flag"
    "fmt"
    "log"
    "math/rand"
    "net"
    "os"
    "strings"
    "sync"
    "time"
)

// quotes holds a handful of whimsical post‑apocalyptic sayings.
var quotes = []string{
    "Keep your eyes on the horizon, but your feet on the rubble.",
    "When in doubt, barter for canned beans.",
    "Radiation is just the universe's way of saying 'stay inside'.",
    "Never trust a scavenger with a smile.",
    "A good shelter is worth more than a golden compass.",
    "If the sky glows green, it's probably time to hide.",
    "Water is life – but coffee is sanity.",
    "Remember: the louder the alarm, the better the story.",
    "A well‑timed joke can defuse a mutant.",
    "Never leave your flashlight on when the batteries are low.",
}

// getRandomQuote returns a quote selected from the slice using the provided RNG.
func getRandomQuote(rng *rand.Rand) string {
    if len(quotes) == 0 {
        return "...silence..."
    }
    idx := rng.Intn(len(quotes))
    return quotes[idx]
}

// runServer starts a UDP server on the given port. It uses the supplied RNG for deterministic output in tests.
func runServer(port string, rng *rand.Rand) error {
    addr, err := net.ResolveUDPAddr("udp", ":"+port)
    if err != nil {
        return fmt.Errorf("resolve udp addr: %w", err)
    }
    conn, err := net.ListenUDP("udp", addr)
    if err != nil {
        return fmt.Errorf("listen udp: %w", err)
    }
    defer conn.Close()
    log.Printf("Quote server listening on UDP %s", port)

    var wg sync.WaitGroup
    buf := make([]byte, 1024)
    for {
        n, clientAddr, err := conn.ReadFromUDP(buf)
        if err != nil {
            // If the connection is closed, exit gracefully.
            if strings.Contains(err.Error(), "use of closed network connection") {
                break
            }
            log.Printf("read error: %v", err)
            continue
        }
        // Echo handling in a goroutine to allow concurrency.
        wg.Add(1)
        go func(data []byte, addr *net.UDPAddr) {
            defer wg.Done()
            _ = data[:n] // request payload is ignored; any packet triggers a quote.
            quote := getRandomQuote(rng)
            _, err := conn.WriteToUDP([]byte(quote), addr)
            if err != nil {
                log.Printf("write error: %v", err)
            }
        }(buf[:n], clientAddr)
    }
    wg.Wait()
    return nil
}

// runClient sends a single empty UDP packet to the server and prints the received quote.
func runClient(address string) error {
    serverAddr, err := net.ResolveUDPAddr("udp", address)
    if err != nil {
        return fmt.Errorf("resolve server address: %w", err)
    }
    conn, err := net.DialUDP("udp", nil, serverAddr)
    if err != nil {
        return fmt.Errorf("dial udp: %w", err)
    }
    defer conn.Close()

    // Send an empty packet as a request.
    _, err = conn.Write([]byte{})
    if err != nil {
        return fmt.Errorf("write request: %w", err)
    }

    // Set a read deadline to avoid hanging forever.
    conn.SetReadDeadline(time.Now().Add(2 * time.Second))
    resp := make([]byte, 1024)
    n, _, err := conn.ReadFromUDP(resp)
    if err != nil {
        return fmt.Errorf("read response: %w", err)
    }
    fmt.Println(string(resp[:n]))
    return nil
}

func main() {
    mode := flag.String("mode", "server", "Mode to run: 'server' or 'client'")
    port := flag.String("port", "9000", "Port for server mode (UDP)")
    address := flag.String("address", "localhost:9000", "Server address for client mode (host:port)")
    seed := flag.Int64("seed", time.Now().UnixNano(), "Seed for random number generator (useful for testing)")
    flag.Parse()

    rng := rand.New(rand.NewSource(*seed))

    switch *mode {
    case "server":
        if err := runServer(*port, rng); err != nil {
            log.Fatalf("Server error: %v", err)
        }
    case "client":
        if err := runClient(*address); err != nil {
            log.Fatalf("Client error: %v", err)
        }
    default:
        fmt.Fprintln(os.Stderr, "Invalid mode. Use -mode=server or -mode=client")
        os.Exit(1)
    }
}
