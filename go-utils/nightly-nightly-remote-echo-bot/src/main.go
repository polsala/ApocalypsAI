package main

import (
    "bufio"
    "flag"
    "fmt"
    "log"
    "math/rand"
    "net"
    "strings"
    "time"
)

var (
    port     = flag.Int("port", 4000, "TCP port to listen on")
    testMode = flag.Bool("testmode", false, "Deterministic suffix for tests")
    suffixes = []string{
        "[The world crumbles]",
        "[Rubble rains]",
        "[Skies darken]",
        "[Silence reigns]",
    }
)

func getSuffix() string {
    if *testMode {
        return "[Apocalypse]"
    }
    rand.Seed(time.Now().UnixNano())
    return suffixes[rand.Intn(len(suffixes))]
}

func handleConn(conn net.Conn) {
    defer conn.Close()
    scanner := bufio.NewScanner(conn)
    writer := bufio.NewWriter(conn)
    for scanner.Scan() {
        line := scanner.Text()
        response := fmt.Sprintf("%s %s\n", line, getSuffix())
        writer.WriteString(response)
        writer.Flush()
    }
    if err := scanner.Err(); err != nil {
        log.Printf("connection error: %v", err)
    }
}

func main() {
    flag.Parse()
    addr := fmt.Sprintf(":%d", *port)
    ln, err := net.Listen("tcp", addr)
    if err != nil {
        log.Fatalf("failed to listen on %s: %v", addr, err)
    }
    log.Printf("Listening on %s", addr)
    for {
        conn, err := ln.Accept()
        if err != nil {
            log.Printf("accept error: %v", err)
            continue
        }
        go handleConn(conn)
    }
}
