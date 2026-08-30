package main

import (
    "bufio"
    "fmt"
    "log"
    "math/rand"
    "net"
    "os"
    "strconv"
    "strings"
    "time"
)

var phrases = []string{
    "The skies darken:",
    "Radiation levels rise:",
    "The ground trembles:",
    "Ash falls:",
    "Silence before the storm:",
}

// getPrefix returns a random apocalypse‑themed phrase.
func getPrefix() string {
    return phrases[rand.Intn(len(phrases))]
}

// handleConn processes a single client connection.
func handleConn(conn net.Conn) {
    defer conn.Close()
    scanner := bufio.NewScanner(conn)
    writer := bufio.NewWriter(conn)
    for scanner.Scan() {
        line := scanner.Text()
        prefixed := fmt.Sprintf("%s %s\n", getPrefix(), line)
        writer.WriteString(prefixed)
        writer.Flush()
    }
    if err := scanner.Err(); err != nil {
        log.Printf("connection error: %v", err)
    }
}

func main() {
    // Deterministic random seed for reproducible tests.
    rand.Seed(42)

    port := "8080"
    if len(os.Args) > 1 {
        port = os.Args[1]
    }
    // Validate that the port is numeric.
    if _, err := strconv.Atoi(port); err != nil {
        log.Fatalf("invalid port: %s", port)
    }
    addr := ":" + port
    ln, err := net.Listen("tcp", addr)
    if err != nil {
        log.Fatalf("failed to listen on %s: %v", addr, err)
    }
    defer ln.Close()
    log.Printf("apocalypse echo server listening on %s", addr)
    for {
        conn, err := ln.Accept()
        if err != nil {
            log.Printf("accept error: %v", err)
            continue
        }
        go handleConn(conn)
    }
}
