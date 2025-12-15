package main

import (
    "bufio"
    "fmt"
    "log"
    "math/rand"
    "net"
    "os"
    "strconv"
    "strings"
    "time"
)

var phrases = []string{
    "The skies crackle",
    "Ashes whisper",
    "Ravens caw",
    "The ground trembles",
    "Eternal night falls",
}

func getRandomPhrase() string {
    return phrases[rand.Intn(len(phrases))]
}

func handleConn(conn net.Conn) {
    defer conn.Close()
    scanner := bufio.NewScanner(conn)
    for scanner.Scan() {
        line := scanner.Text()
        phrase := getRandomPhrase()
        response := fmt.Sprintf("%s: %s\n", phrase, line)
        _, err := conn.Write([]byte(response))
        if err != nil {
            log.Printf("write error: %v", err)
            return
        }
    }
    if err := scanner.Err(); err != nil {
        log.Printf("read error: %v", err)
    }
}

func main() {
    rand.Seed(time.Now().UnixNano())
    port := "8080"
    if len(os.Args) > 1 {
        port = os.Args[1]
    }
    // Validate port is numeric
    if _, err := strconv.Atoi(port); err != nil {
        log.Fatalf("invalid port: %s", port)
    }
    addr := ":" + port
    ln, err := net.Listen("tcp", addr)
    if err != nil {
        log.Fatalf("listen error: %v", err)
    }
    defer ln.Close()
    log.Printf("Apocalyptic Echo Bot listening on %s", addr)
    for {
        conn, err := ln.Accept()
        if err != nil {
            log.Printf("accept error: %v", err)
            continue
        }
        go handleConn(conn)
    }
}
