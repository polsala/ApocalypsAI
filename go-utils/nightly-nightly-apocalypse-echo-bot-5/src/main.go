package main

import (
    "bufio"
    "flag"
    "fmt"
    "net"
    "os"
    "strings"
    "sync/atomic"
)

// Default apocalypse‑themed tags. Can be overridden in tests via SetTags.
var tags = []string{"[Doom]", "[Ashes]", "[Ruin]", "[Silence]"}
var tagIdx uint64

// SetTags allows tests to provide a deterministic tag list.
func SetTags(t []string) {
    tags = t
    atomic.StoreUint64(&tagIdx, 0)
}

func getTag() string {
    i := atomic.AddUint64(&tagIdx, 1) - 1
    return tags[i%uint64(len(tags))]
}

func handleConn(conn net.Conn) {
    defer conn.Close()
    scanner := bufio.NewScanner(conn)
    writer := bufio.NewWriter(conn)
    for scanner.Scan() {
        line := scanner.Text()
        prefixed := fmt.Sprintf("%s %s\n", getTag(), line)
        writer.WriteString(prefixed)
        writer.Flush()
    }
    // Ignore scanner.Err() for brevity.
}

func runServer(listenAddr string) error {
    ln, err := net.Listen("tcp", listenAddr)
    if err != nil {
        return err
    }
    defer ln.Close()
    fmt.Printf("Apocalypse Echo Bot listening on %s\n", listenAddr)
    for {
        conn, err := ln.Accept()
        if err != nil {
            // Listener closed, exit gracefully.
            if strings.Contains(err.Error(), "use of closed network connection") {
                return nil
            }
            fmt.Fprintf(os.Stderr, "accept error: %v\n", err)
            continue
        }
        go handleConn(conn)
    }
}

func runClient(target string) error {
    conn, err := net.Dial("tcp", target)
    if err != nil {
        return err
    }
    defer conn.Close()
    scanner := bufio.NewScanner(os.Stdin)
    serverScanner := bufio.NewScanner(conn)
    for scanner.Scan() {
        line := scanner.Text()
        fmt.Fprintf(conn, "%s\n", line)
        if serverScanner.Scan() {
            fmt.Println(serverScanner.Text())
        } else {
            return fmt.Errorf("server closed connection")
        }
    }
    return scanner.Err()
}

func main() {
    listenAddr := flag.String("listen", ":9090", "address for server mode (e.g., :8080)")
    clientTarget := flag.String("client", "", "address for client mode (e.g., localhost:8080)")
    flag.Parse()

    if *clientTarget != "" {
        if err := runClient(*clientTarget); err != nil {
            fmt.Fprintf(os.Stderr, "client error: %v\n", err)
            os.Exit(1)
        }
        return
    }

    if err := runServer(*listenAddr); err != nil {
        fmt.Fprintf(os.Stderr, "server error: %v\n", err)
        os.Exit(1)
    }
}
