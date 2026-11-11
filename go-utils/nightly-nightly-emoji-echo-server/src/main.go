package main

import (
    "bufio"
    "fmt"
    "math/rand"
    "net"
    "os"
    "strconv"
    "strings"
    "time"
)

var emojis = []string{"😀", "😂", "😎", "🤖", "👾"}

// getRand returns a *rand.Rand seeded deterministically for tests or with time.Now for production.
func getRand() *rand.Rand {
    if seedStr := os.Getenv("SEED"); seedStr != "" {
        if seed, err := strconv.ParseInt(seedStr, 10, 64); err == nil {
            return rand.New(rand.NewSource(seed))
        }
    }
    return rand.New(rand.NewSource(time.Now().UnixNano()))
}

func randomEmoji(r *rand.Rand) string {
    return emojis[r.Intn(len(emojis))]
}

func handleConn(conn net.Conn, r *rand.Rand) {
    defer conn.Close()
    scanner := bufio.NewScanner(conn)
    writer := bufio.NewWriter(conn)
    for scanner.Scan() {
        line := scanner.Text()
        echoed := fmt.Sprintf("%s %s\n", line, randomEmoji(r))
        writer.WriteString(echoed)
        writer.Flush()
    }
    // ignore scanner.Err() for brevity
}

// startServer runs the accept loop on the provided listener.
func startServer(l net.Listener) error {
    r := getRand()
    for {
        conn, err := l.Accept()
        if err != nil {
            return err
        }
        go handleConn(conn, r)
    }
}

func main() {
    port := "8080"
    if p := os.Getenv("PORT"); p != "" {
        port = p
    }
    addr := ":" + port
    listener, err := net.Listen("tcp", addr)
    if err != nil {
        fmt.Fprintf(os.Stderr, "Failed to listen on %s: %v\n", addr, err)
        os.Exit(1)
    }
    fmt.Printf("Emoji Echo Server listening on %s\n", listener.Addr().String())
    if err := startServer(listener); err != nil && !strings.Contains(err.Error(), "use of closed network connection") {
        fmt.Fprintf(os.Stderr, "Server error: %v\n", err)
    }
}
