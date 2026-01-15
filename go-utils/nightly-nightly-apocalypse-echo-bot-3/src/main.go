package main

import (
    "bufio"
    "flag"
    "fmt"
    "log"
    "net"
    "os"
)

// startServer launches a TCP server that echoes each received line
// with the apocalypse‑themed prefix.
func startServer(port string) error {
    ln, err := net.Listen("tcp", ":"+port)
    if err != nil {
        return err
    }
    defer ln.Close()
    for {
        conn, err := ln.Accept()
        if err != nil {
            return err
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
        response := fmt.Sprintf("⚡️[Apocalypse] %s\n", line)
        writer.WriteString(response)
        writer.Flush()
    }
}

// runClient connects to the server, sends a single message, and returns the response.
func runClient(port, msg string) (string, error) {
    conn, err := net.Dial("tcp", "127.0.0.1:"+port)
    if err != nil {
        return "", err
    }
    defer conn.Close()
    fmt.Fprintf(conn, "%s\n", msg)
    resp, err := bufio.NewReader(conn).ReadString('\n')
    if err != nil {
        return "", err
    }
    return resp, nil
}

func main() {
    mode := flag.String("mode", "server", "mode: server or client")
    port := flag.String("port", "8080", "port to listen on or connect to")
    msg := flag.String("msg", "", "message to send (client mode)")
    flag.Parse()

    if *mode == "server" {
        log.Printf("Starting apocalypse echo server on port %s", *port)
        if err := startServer(*port); err != nil {
            log.Fatalf("Server error: %v", err)
        }
    } else if *mode == "client" {
        if *msg == "" {
            fmt.Fprintln(os.Stderr, "msg is required in client mode")
            os.Exit(1)
        }
        resp, err := runClient(*port, *msg)
        if err != nil {
            log.Fatalf("Client error: %v", err)
        }
        fmt.Print(resp)
    } else {
        fmt.Fprintln(os.Stderr, "invalid mode")
        os.Exit(1)
    }
}
