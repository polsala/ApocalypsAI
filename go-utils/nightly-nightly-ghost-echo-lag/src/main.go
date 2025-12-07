package main

import (
    "flag"
    "fmt"
    "net"
    "time"
)

func measureRTT(host string, port int) (time.Duration, error) {
    addr := fmt.Sprintf("%s:%d", host, port)
    start := time.Now()
    conn, err := net.DialTimeout("tcp", addr, 2*time.Second)
    if err != nil {
        return 0, err
    }
    defer conn.Close()
    rtt := time.Since(start)
    return rtt, nil
}

func main() {
    host := flag.String("host", "localhost", "host to ping")
    port := flag.Int("port", 80, "port to connect")
    flag.Parse()

    rtt, err := measureRTT(*host, *port)
    if err != nil {
        fmt.Printf("Ghostly echo: failed to connect to %s:%d: %v\n", *host, *port, err)
        return
    }
    fmt.Printf("Ghostly echo: RTT = %d ms\n", rtt.Milliseconds())
}
