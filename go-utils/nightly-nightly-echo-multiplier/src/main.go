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
    "time"
)

var emojis = []string{
    "😀","🚀","🌟","🔥","💧","🍀","🎉","🧩","🦄","🤖",
}

func main() {
    addr := flag.String("addr", ":8080", "listen address")
    flag.Parse()

    // Seed rand with current time for production randomness
    rand.Seed(time.Now().UnixNano())

    ln, err := net.Listen("tcp", *addr)
    if err != nil {
        log.Fatalf("Failed to listen on %s: %v", *addr, err)
    }
    defer ln.Close()
    log.Printf("Echo server listening on %s", *addr)

    for {
        conn, err := ln.Accept()
        if err != nil {
            log.Printf("Accept error: %v", err)
            continue
        }
        go handleConn(conn)
    }
}

// handleConn reads lines from conn and writes back the line plus a random emoji.
func handleConn(conn net.Conn) {
    defer conn.Close()
    scanner := bufio.NewScanner(conn)
    writer := bufio.NewWriter(conn)

    for scanner.Scan() {
        line := scanner.Text()
        emoji := emojis[rand.Intn(len(emojis))]
        response := fmt.Sprintf("%s %s\n", line, emoji)
        if _, err := writer.WriteString(response); err != nil {
            fmt.Fprintf(os.Stderr, "Write error: %v\n", err)
            return
        }
        writer.Flush()
    }
    if err := scanner.Err(); err != nil && !strings.Contains(err.Error(), "closed") {
        fmt.Fprintf(os.Stderr, "Read error: %v\n", err)
    }
}
