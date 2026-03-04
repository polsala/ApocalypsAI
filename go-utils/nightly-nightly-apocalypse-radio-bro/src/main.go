package main

import (
    "bufio"
    "flag"
    "fmt"
    "math/rand"
    "net"
    "os"
    "time"
)

// Pre‑defined broadcast messages.  Feel free to add more for extra flavor.
var messages = []string{
    "... static ...",
    "This is the last broadcast from the wasteland.",
    "Do you hear the wind? It carries whispers of the old world.",
    "Radio silence... or is it?",
    "Survivors, gather at the beacon.",
    "The sun sets, but the signal lives.",
}

// broadcast writes a short series of messages to the provided connection.
// It uses the supplied *rand.Rand for deterministic behaviour in tests.
func broadcast(conn net.Conn, rng *rand.Rand) {
    defer conn.Close()
    writer := bufio.NewWriter(conn)
    for i := 0; i < 10; i++ {
        msg := messages[rng.Intn(len(messages))]
        fmt.Fprintln(writer, msg)
        writer.Flush()
        // Small pause to emulate a real‑time radio transmission.
        time.Sleep(100 * time.Millisecond)
    }
}

func main() {
    port := flag.String("port", "8080", "Port to listen on")
    flag.Parse()

    listener, err := net.Listen("tcp", ":"+*port)
    if err != nil {
        fmt.Fprintln(os.Stderr, "Failed to listen:", err)
        os.Exit(1)
    }
    fmt.Println("Apocalypse Radio broadcasting on port", *port)

    // Seed the random generator with current time for production use.
    rng := rand.New(rand.NewSource(time.Now().UnixNano()))

    for {
        conn, err := listener.Accept()
        if err != nil {
            fmt.Fprintln(os.Stderr, "Accept error:", err)
            continue
        }
        go broadcast(conn, rng)
    }
}
