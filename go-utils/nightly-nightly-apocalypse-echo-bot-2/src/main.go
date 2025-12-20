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

var phrases = []string{
    "The Skies Crack",
    "Ashes Whisper",
    "Ravens Caw",
    "Molten Dawn",
    "Silent Fallout",
    "Eternal Ember",
    "Winds of Ruin",
    "Shattered Horizon",
}

func main() {
    port := flag.Int("port", 4000, "Port to listen on")
    flag.Parse()
    addr := fmt.Sprintf(":%d", *port)

    // deterministic random for tests
    rand.Seed(42)

    ln, err := net.Listen("tcp", addr)
    if err != nil {
        log.Fatalf("Failed to listen on %s: %v", addr, err)
    }
    defer ln.Close()
    log.Printf("Apocalypse Echo Server listening on %s", addr)

    for {
        conn, err := ln.Accept()
        if err != nil {
            log.Printf("Accept error: %v", err)
            continue
        }
        go handleConn(conn)
    }
}

func handleConn(c net.Conn) {
    defer c.Close()
    scanner := bufio.NewScanner(c)
    writer := bufio.NewWriter(c)
    for scanner.Scan() {
        line := scanner.Text()
        phrase := phrases[rand.Intn(len(phrases))]
        response := fmt.Sprintf("[%s] %s\n", phrase, line)
        writer.WriteString(response)
        writer.Flush()
    }
    if err := scanner.Err(); err != nil && !strings.Contains(err.Error(), "closed") {
        log.Printf("Read error: %v", err)
    }
}
