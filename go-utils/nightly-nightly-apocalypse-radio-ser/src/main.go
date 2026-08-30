package main

import (
    "bufio"
    "flag"
    "fmt"
    "log"
    "math/rand"
    "net"
    "strings"
    "time"
)

// quotes holds a collection of whimsical post‑apocalyptic messages.
var quotes = []string{
    "The sun rose over the rusted towers, but the coffee machine stayed dead.",
    "Remember when Wi‑Fi was a thing? Yeah, me neither.",
    "Radiation levels are low… for now.",
    "The last meme died in the desert, but its echo lives on.",
    "If you hear static, it's just the universe buffering.",
    "Don't trust the bunker’s thermostat – it has its own agenda.",
    "Survivors: now offering free hugs for a limited time only.",
    "The only thing that’s certain is uncertainty.",
    "Keep calm and ration on.",
    "Your battery is low, but your spirit is not.",
}

// getRandomQuote returns a random quote from the quotes slice.
func getRandomQuote() string {
    if len(quotes) == 0 {
        return "..."
    }
    idx := rand.Intn(len(quotes))
    return quotes[idx]
}

// handleClient streams quotes to a single client until the connection closes.
func handleClient(conn net.Conn, interval time.Duration) {
    defer conn.Close()
    writer := bufio.NewWriter(conn)
    ticker := time.NewTicker(interval)
    defer ticker.Stop()
    for {
        select {
        case <-ticker.C:
            quote := getRandomQuote()
            // Ensure each quote ends with a newline for client readability.
            if !strings.HasSuffix(quote, "\n") {
                quote += "\n"
            }
            _, err := writer.WriteString(quote)
            if err != nil {
                log.Printf("client write error: %v", err)
                return
            }
            err = writer.Flush()
            if err != nil {
                log.Printf("client flush error: %v", err)
                return
            }
        }
    }
}

func main() {
    // Command‑line flags for address and broadcast interval.
    addr := flag.String("addr", "0.0.0.0:8080", "TCP listen address")
    intervalStr := flag.String("interval", "5s", "Broadcast interval (e.g., 2s, 500ms)")
    flag.Parse()

    interval, err := time.ParseDuration(*intervalStr)
    if err != nil {
        log.Fatalf("invalid interval: %v", err)
    }

    // Seed the random number generator.
    rand.Seed(time.Now().UnixNano())

    listener, err := net.Listen("tcp", *addr)
    if err != nil {
        log.Fatalf("failed to listen on %s: %v", *addr, err)
    }
    defer listener.Close()
    log.Printf("Apocalypse Radio Server listening on %s (interval %s)", *addr, interval)

    for {
        conn, err := listener.Accept()
        if err != nil {
            log.Printf("accept error: %v", err)
            continue
        }
        log.Printf("client connected from %s", conn.RemoteAddr())
        go handleClient(conn, interval)
    }
}
