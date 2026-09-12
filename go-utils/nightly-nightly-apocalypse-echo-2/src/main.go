package main

import (
    "bufio"
    "flag"
    "fmt"
    "math/rand"
    "net"
    "os"
    "strings"
    "time"
)

var phrases = []string{
    "The skies burn:",
    "Dust storms whisper:",
    "Ravens caw:",
    "Ashes fall:",
    "The ground cracks:",
}

// formatMessage prefixes msg with a random apocalypse phrase using the provided rand.Rand.
func formatMessage(msg string, r *rand.Rand) string {
    if len(phrases) == 0 {
        return msg
    }
    prefix := phrases[r.Intn(len(phrases))]
    return fmt.Sprintf("%s %s", prefix, msg)
}

// handleConnection processes a single client connection.
func handleConnection(conn net.Conn, r *rand.Rand) {
    defer conn.Close()
    scanner := bufio.NewScanner(conn)
    writer := bufio.NewWriter(conn)
    for scanner.Scan() {
        line := scanner.Text()
        // Trim any carriage return to keep output tidy.
        line = strings.TrimRight(line, "\r")
        out := formatMessage(line, r)
        fmt.Fprintln(writer, out)
        writer.Flush()
    }
    // Ignoring scanner.Err() for brevity; in production log it.
}

func main() {
    port := flag.Int("port", 8080, "Port to listen on")
    flag.Parse()

    addr := fmt.Sprintf(":%d", *port)
    listener, err := net.Listen("tcp", addr)
    if err != nil {
        fmt.Fprintf(os.Stderr, "Failed to listen on %s: %v\n", addr, err)
        os.Exit(1)
    }
    defer listener.Close()
    fmt.Printf("Apocalyptic Echo Server listening on %s\n", addr)

    // Seed the random generator once; each connection shares it.
    r := rand.New(rand.NewSource(time.Now().UnixNano()))

    for {
        conn, err := listener.Accept()
        if err != nil {
            fmt.Fprintf(os.Stderr, "Accept error: %v\n", err)
            continue
        }
        go handleConnection(conn, r)
    }
}
