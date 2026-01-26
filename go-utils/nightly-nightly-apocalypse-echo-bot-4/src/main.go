package main

import (
    "bufio"
    "fmt"
    "math/rand"
    "net"
    "os"
    "strings"
    "time"
)

var defaultPhrases = []string{
    "Doomsday",
    "The Last Sunrise",
    "Ashes to Ashes",
    "Final Countdown",
    "Eternal Night",
    "Ragnarok",
    "The Great Silence",
    "Apocalypse Now",
}

func getRandomPhrase(phrases []string) string {
    if len(phrases) == 0 {
        return ""
    }
    return phrases[rand.Intn(len(phrases))]
}

func handleConnection(conn net.Conn, phrases []string) {
    defer conn.Close()
    scanner := bufio.NewScanner(conn)
    writer := bufio.NewWriter(conn)
    for scanner.Scan() {
        line := scanner.Text()
        // Preserve empty lines
        if strings.TrimSpace(line) == "" {
            writer.WriteString("\n")
            writer.Flush()
            continue
        }
        response := fmt.Sprintf("%s: %s\n", getRandomPhrase(phrases), line)
        writer.WriteString(response)
        writer.Flush()
    }
    // Ignore scanner.Err() for brevity; connection will simply close on error.
}

func main() {
    // Seed random generator
    rand.Seed(time.Now().UnixNano())

    address := os.Getenv("ADDRESS")
    if address == "" {
        address = "localhost:4000"
    }

    listener, err := net.Listen("tcp", address)
    if err != nil {
        fmt.Fprintf(os.Stderr, "Failed to listen on %s: %v\n", address, err)
        os.Exit(1)
    }
    defer listener.Close()
    fmt.Printf("Apocalyptic Echo Bot listening on %s\n", address)

    for {
        conn, err := listener.Accept()
        if err != nil {
            fmt.Fprintf(os.Stderr, "Accept error: %v\n", err)
            continue
        }
        go handleConnection(conn, defaultPhrases)
    }
}
