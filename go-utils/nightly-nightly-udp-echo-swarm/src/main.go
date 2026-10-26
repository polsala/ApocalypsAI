package main

import (
    "errors"
    "flag"
    "fmt"
    "net"
    "strings"
    "sync"
    "time"
)

type Result struct {
    Host string
    RTT  time.Duration
    Err  error
}

// PingHost sends a UDP message to the given address and waits for the echo.
// It returns the round‑trip time or an error if the operation fails.
func PingHost(address string, message string, timeout time.Duration) Result {
    start := time.Now()
    addr, err := net.ResolveUDPAddr("udp", address)
    if err != nil {
        return Result{Host: address, Err: err}
    }
    conn, err := net.DialUDP("udp", nil, addr)
    if err != nil {
        return Result{Host: address, Err: err}
    }
    defer conn.Close()
    conn.SetDeadline(time.Now().Add(timeout))
    _, err = conn.Write([]byte(message))
    if err != nil {
        return Result{Host: address, Err: err}
    }
    buf := make([]byte, 1024)
    n, _, err := conn.ReadFromUDP(buf)
    if err != nil {
        return Result{Host: address, Err: err}
    }
    rtt := time.Since(start)
    if string(buf[:n]) != message {
        return Result{Host: address, Err: errors.New("mismatched echo response")}
    }
    return Result{Host: address, RTT: rtt, Err: nil}
}

func main() {
    hostsFlag := flag.String("hosts", "", "comma‑separated list of host:port")
    msgFlag := flag.String("msg", "ping", "message to send")
    timeoutFlag := flag.Duration("timeout", 2*time.Second, "per‑host timeout")
    flag.Parse()

    if *hostsFlag == "" {
        fmt.Println("error: -hosts flag is required")
        return
    }
    hosts := strings.Split(*hostsFlag, ",")
    var wg sync.WaitGroup
    resultsCh := make(chan Result, len(hosts))

    for _, h := range hosts {
        h = strings.TrimSpace(h)
        wg.Add(1)
        go func(host string) {
            defer wg.Done()
            res := PingHost(host, *msgFlag, *timeoutFlag)
            resultsCh <- res
        }(h)
    }
    wg.Wait()
    close(resultsCh)

    for res := range resultsCh {
        if res.Err != nil {
            fmt.Printf("%s -> error: %v\n", res.Host, res.Err)
        } else {
            fmt.Printf("%s -> %v\n", res.Host, res.RTT)
        }
    }
}
