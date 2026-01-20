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

var (
    mode = flag.String("mode", "server", "Mode to run: server or client")
    port = flag.Int("port", 8080, "Port to listen on or connect to")
    msg  = flag.String("msg", "", "Message to send (client mode)")
)

var prefixes = []string{"WASTELAND", "RUINS", "SANDSTORM", "MUTANT", "RADIOACTIVE"}

// randomPrefix returns a random prefix from the list.
func randomPrefix() string {
    return prefixes[rand.Intn(len(prefixes))]
}

// handleConn processes a single client connection.
func handleConn(conn net.Conn, wg *sync.WaitGroup) {
    defer wg.Done()
    defer conn.Close()
    scanner := bufio.NewScanner(conn)
    writer := bufio.NewWriter(conn)
    for scanner.Scan() {
        line := scanner.Text()
        prefixed := fmt.Sprintf("%s: %s\n", randomPrefix(), line)
        writer.WriteString(prefixed)
        writer.Flush()
    }
    if err := scanner.Err(); err != nil {
        log.Printf("error reading from client: %v", err)
    }
}

// startServer runs the echo server on the provided listener.
func startServer(l net.Listener) error {
    var wg sync.WaitGroup
    for {
        conn, err := l.Accept()
        if err != nil {
            // Listener closed, exit gracefully.
            if strings.Contains(err.Error(), "use of closed network connection") {
                break
            }
            return err
        }
        wg.Add(1)
        go handleConn(conn, &wg)
    }
    wg.Wait()
    return nil
}

// clientSend connects to the server, sends a single line, and returns the response.
func clientSend(address, message string) (string, error) {
    conn, err := net.Dial("tcp", address)
    if err != nil {
        return "", err
    }
    defer conn.Close()
    fmt.Fprintf(conn, "%s\n", message)
    resp, err := bufio.NewReader(conn).ReadString('\n')
    if err != nil {
        return "", err
    }
    return strings.TrimSpace(resp), nil
}

func main() {
    flag.Parse()
    rand.Seed(time.Now().UnixNano())
    address := fmt.Sprintf("127.0.0.1:%d", *port)
    switch *mode {
    case "server":
        l, err := net.Listen("tcp", address)
        if err != nil {
            log.Fatalf("failed to listen on %s: %v", address, err)
        }
        log.Printf("apocalypse-echo server listening on %s", address)
        if err := startServer(l); err != nil {
            log.Fatalf("server error: %v", err)
        }
    case "client":
        if *msg == "" {
            fmt.Fprintln(os.Stderr, "-msg is required in client mode")
            os.Exit(1)
        }
        resp, err := clientSend(address, *msg)
        if err != nil {
            log.Fatalf("client error: %v", err)
        }
        fmt.Println(resp)
    default:
        fmt.Fprintf(os.Stderr, "unknown mode: %s\n", *mode)
        os.Exit(1)
    }
}
