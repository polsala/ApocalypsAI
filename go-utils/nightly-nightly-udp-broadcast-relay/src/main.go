package main

import (
    "flag"
    "fmt"
    "log"
    "net"
    "strings"
    "sync"
)

func main() {
    mode := flag.String("mode", "relay", "Mode: relay or send")
    listenAddr := flag.String("listen", ":9000", "UDP address to listen on (relay mode)")
    targets := flag.String("targets", "", "Comma‑separated list of UDP addresses to forward to (relay mode)")
    sendAddr := flag.String("addr", "", "UDP address to send to (send mode)")
    msg := flag.String("msg", "", "Message to send (send mode)")
    flag.Parse()

    switch *mode {
    case "relay":
        if *targets == "" {
            log.Fatal("targets required in relay mode")
        }
        runRelay(*listenAddr, strings.Split(*targets, ","))
    case "send":
        if *sendAddr == "" || *msg == "" {
            log.Fatal("addr and msg required in send mode")
        }
        err := sendMessage(*sendAddr, []byte(*msg))
        if err != nil {
            log.Fatalf("send error: %v", err)
        }
        fmt.Println("sent")
    default:
        log.Fatalf("unknown mode %s", *mode)
    }
}

func runRelay(listen string, targets []string) {
    addr, err := net.ResolveUDPAddr("udp", listen)
    if err != nil {
        log.Fatalf("resolve listen addr: %v", err)
    }
    conn, err := net.ListenUDP("udp", addr)
    if err != nil {
        log.Fatalf("listen udp: %v", err)
    }
    defer conn.Close()
    log.Printf("relay listening on %s, forwarding to %v", listen, targets)

    var wg sync.WaitGroup
    buf := make([]byte, 65535)
    for {
        n, src, err := conn.ReadFromUDP(buf)
        if err != nil {
            log.Printf("read error: %v", err)
            continue
        }
        data := make([]byte, n)
        copy(data, buf[:n])
        log.Printf("received %d bytes from %s", n, src)

        for _, t := range targets {
            wg.Add(1)
            go func(target string) {
                defer wg.Done()
                err := forwardMessage(target, data)
                if err != nil {
                    log.Printf("forward to %s failed: %v", target, err)
                } else {
                    log.Printf("forwarded to %s", target)
                }
            }(t)
        }
    }
}

func forwardMessage(target string, data []byte) error {
    raddr, err := net.ResolveUDPAddr("udp", target)
    if err != nil {
        return fmt.Errorf("resolve target: %w", err)
    }
    conn, err := net.DialUDP("udp", nil, raddr)
    if err != nil {
        return fmt.Errorf("dial udp: %w", err)
    }
    defer conn.Close()
    _, err = conn.Write(data)
    return err
}

func sendMessage(addr string, data []byte) error {
    raddr, err := net.ResolveUDPAddr("udp", addr)
    if err != nil {
        return fmt.Errorf("resolve addr: %w", err)
    }
    conn, err := net.DialUDP("udp", nil, raddr)
    if err != nil {
        return fmt.Errorf("dial udp: %w", err)
    }
    defer conn.Close()
    _, err = conn.Write(data)
    return err
}
