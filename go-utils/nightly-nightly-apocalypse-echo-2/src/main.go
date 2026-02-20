package main

import (
    "bufio"
    "fmt"
    "log"
    "net"
)

// prefix added to each echoed line
const prefix = "[Doom] "

// RunServer starts a TCP echo server on the given address.
// If address is ":0", the system picks an available port.
// It returns the actual listening address, a shutdown function, and any error.
func RunServer(addr string) (string, func() error, error) {
    ln, err := net.Listen("tcp", addr)
    if err != nil {
        return "", nil, err
    }

    // shutdown closes the listener
    shutdown := func() error {
        return ln.Close()
    }

    go func() {
        for {
            conn, err := ln.Accept()
            if err != nil {
                // listener closed
                return
            }
            go handleConn(conn)
        }
    }()

    return ln.Addr().String(), shutdown, nil
}

func handleConn(conn net.Conn) {
    defer conn.Close()
    scanner := bufio.NewScanner(conn)
    writer := bufio.NewWriter(conn)
    for scanner.Scan() {
        line := scanner.Text()
        response := prefix + line + "\n"
        writer.WriteString(response)
        writer.Flush()
    }
    // ignore scanner.Err()
}

func main() {
    addr, _, err := RunServer(":0")
    if err != nil {
        log.Fatalf("Failed to start server: %v", err)
    }
    fmt.Printf("Listening on %s\n", addr)

    // block forever
    select {}
}
