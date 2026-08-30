package main

import (
    "bufio"
    "flag"
    "fmt"
    "io"
    "log"
    "net"
    "os"
    "sync/atomic"
)

var quotes = []string{
    "The wasteland whispers.",
    "Hope is a fragile ember.",
    "Even ruins have stories.",
    "Silence sings louder than bombs.",
}

// counter provides a deterministic round‑robin selection of quotes.
var counter uint64

func main() {
    if len(os.Args) < 2 {
        fmt.Fprintln(os.Stderr, "expected 'server' or 'client' subcommand")
        os.Exit(1)
    }

    switch os.Args[1] {
    case "server":
        serverCmd := flag.NewFlagSet("server", flag.ExitOnError)
        port := serverCmd.Int("port", 8080, "port to listen on")
        serverCmd.Parse(os.Args[2:])
        runServer(*port)
    case "client":
        clientCmd := flag.NewFlagSet("client", flag.ExitOnError)
        addr := clientCmd.String("addr", "localhost:8080", "address of the quote server")
        clientCmd.Parse(os.Args[2:])
        runClient(*addr)
    default:
        fmt.Fprintln(os.Stderr, "unknown subcommand")
        os.Exit(1)
    }
}

func runServer(port int) {
    ln, err := net.Listen("tcp", fmt.Sprintf(":%d", port))
    if err != nil {
        log.Fatalf("failed to listen on port %d: %v", port, err)
    }
    defer ln.Close()
    log.Printf("quote server listening on %s", ln.Addr())
    for {
        conn, err := ln.Accept()
        if err != nil {
            log.Printf("accept error: %v", err)
            continue
        }
        go handleConn(conn)
    }
}

func handleConn(conn net.Conn) {
    defer conn.Close()
    idx := atomic.AddUint64(&counter, 1) - 1
    quote := quotes[idx%uint64(len(quotes))]
    fmt.Fprintln(conn, quote)
}

func runClient(address string) {
    conn, err := net.Dial("tcp", address)
    if err != nil {
        log.Fatalf("failed to connect to %s: %v", address, err)
    }
    defer conn.Close()
    reader := bufio.NewReader(conn)
    for {
        line, err := reader.ReadString('\n')
        if err != nil {
            if err == io.EOF {
                break
            }
            log.Fatalf("read error: %v", err)
        }
        fmt.Print(line)
    }
}
