package main

import (
    "bufio"
    "fmt"
    "log"
    "net"
    "net/http"
    "sync/atomic"
)

var totalConnections uint64

func handleTCP(conn net.Conn) {
    atomic.AddUint64(&totalConnections, 1)
    defer conn.Close()
    scanner := bufio.NewScanner(conn)
    for scanner.Scan() {
        line := scanner.Text()
        fmt.Fprintln(conn, line) // echo back the received line
    }
    if err := scanner.Err(); err != nil {
        log.Printf("TCP scanner error: %v", err)
    }
}

func startTCP(address string) {
    ln, err := net.Listen("tcp", address)
    if err != nil {
        log.Fatalf("TCP listen error: %v", err)
    }
    go func() {
        for {
            conn, err := ln.Accept()
            if err != nil {
                log.Printf("TCP accept error: %v", err)
                continue
            }
            go handleTCP(conn)
        }
    }()
}

func statsHandler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "total_connections %d\n", atomic.LoadUint64(&totalConnections))
}

func startHTTP(address string) {
    http.HandleFunc("/stats", statsHandler)
    go func() {
        if err := http.ListenAndServe(address, nil); err != nil {
            log.Fatalf("HTTP server error: %v", err)
        }
    }()
}

func main() {
    // Default ports – change here if you need different ones before building.
    tcpAddr := ":9000"
    httpAddr := ":9001"
    startTCP(tcpAddr)
    startHTTP(httpAddr)
    // Block forever; the servers run in background goroutines.
    select {}
}
