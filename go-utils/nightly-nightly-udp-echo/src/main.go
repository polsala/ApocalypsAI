package main

import (
    "flag"
    "fmt"
    "log"
    "net"
    "time"
)

func runServer(addr string) error {
    udpAddr, err := net.ResolveUDPAddr("udp", addr)
    if err != nil {
        return err
    }
    conn, err := net.ListenUDP("udp", udpAddr)
    if err != nil {
        return err
    }
    defer conn.Close()
    buf := make([]byte, 65535)
    for {
        n, remote, err := conn.ReadFromUDP(buf)
        if err != nil {
            return err
        }
        // Echo back the same data
        _, err = conn.WriteToUDP(buf[:n], remote)
        if err != nil {
            return err
        }
    }
}

func runClient(addr, msg string, count int) error {
    udpAddr, err := net.ResolveUDPAddr("udp", addr)
    if err != nil {
        return err
    }
    conn, err := net.DialUDP("udp", nil, udpAddr)
    if err != nil {
        return err
    }
    defer conn.Close()
    for i := 0; i < count; i++ {
        start := time.Now()
        _, err = conn.Write([]byte(msg))
        if err != nil {
            return err
        }
        buf := make([]byte, len(msg))
        conn.SetReadDeadline(time.Now().Add(2 * time.Second))
        n, _, err := conn.ReadFromUDP(buf)
        if err != nil {
            return err
        }
        rtt := time.Since(start)
        fmt.Printf("Reply %d: %s (RTT %v)\n", i+1, string(buf[:n]), rtt)
        time.Sleep(200 * time.Millisecond)
    }
    return nil
}

func main() {
    mode := flag.String("mode", "server", "Mode to run: server or client")
    addr := flag.String("addr", "0.0.0.0:9000", "UDP address to listen on or connect to")
    msg := flag.String("msg", "ping", "Message to send (client mode)")
    count := flag.Int("count", 1, "Number of messages to send (client mode)")
    flag.Parse()

    switch *mode {
    case "server":
        log.Printf("Starting UDP echo server on %s\n", *addr)
        if err := runServer(*addr); err != nil {
            log.Fatalf("Server error: %v", err)
        }
    case "client":
        log.Printf("Sending %d messages to %s\n", *count, *addr)
        if err := runClient(*addr, *msg, *count); err != nil {
            log.Fatalf("Client error: %v", err)
        }
    default:
        log.Fatalf("Unknown mode: %s", *mode)
    }
}
