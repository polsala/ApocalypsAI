package main

import (
    "flag"
    "fmt"
    "log"
    "net"
    "os"
    "sync"
)

// Relay starts a UDP relay from listenAddr to broadcastAddr.
// It runs until the provided context is cancelled or an error occurs.
func Relay(listenAddr, broadcastAddr string) error {
    laddr, err := net.ResolveUDPAddr("udp", listenAddr)
    if err != nil {
        return fmt.Errorf("resolve listen address: %w", err)
    }
    baddr, err := net.ResolveUDPAddr("udp", broadcastAddr)
    if err != nil {
        return fmt.Errorf("resolve broadcast address: %w", err)
    }

    // Socket for receiving
    connIn, err := net.ListenUDP("udp", laddr)
    if err != nil {
        return fmt.Errorf("listen udp: %w", err)
    }
    defer connIn.Close()

    // Socket for sending
    connOut, err := net.DialUDP("udp", nil, baddr)
    if err != nil {
        return fmt.Errorf("dial udp: %w", err)
    }
    defer connOut.Close()

    var wg sync.WaitGroup
    buf := make([]byte, 65535)

    for {
        n, src, err := connIn.ReadFromUDP(buf)
        if err != nil {
            // If the socket is closed, exit gracefully
            if opErr, ok := err.(*net.OpError); ok && !opErr.Temporary() {
                break
            }
            log.Printf("read error: %v", err)
            continue
        }

        // Copy data for goroutine
        data := make([]byte, n)
        copy(data, buf[:n])

        wg.Add(1)
        go func(src *net.UDPAddr, payload []byte) {
            defer wg.Done()
            // Forward to broadcast address
            _, err := connOut.Write(payload)
            if err != nil {
                log.Printf("forward error from %v: %v", src, err)
            }
        }(src, data)
    }

    wg.Wait()
    return nil
}

func main() {
    listen := flag.String("listen", ":9000", "UDP address to listen on")
    broadcast := flag.String("broadcast", "239.0.0.1:9000", "UDP address to forward packets to")
    flag.Parse()

    if err := Relay(*listen, *broadcast); err != nil {
        fmt.Fprintln(os.Stderr, err)
        os.Exit(1)
    }
}
