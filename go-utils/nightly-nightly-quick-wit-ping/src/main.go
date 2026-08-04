package main

import (
    "bufio"
    "fmt"
    "net"
    "os"
    "strings"
    "sync"
    "time"
)

// animalMetaphor maps latency to a whimsical animal rating.
func animalMetaphor(d time.Duration) (string, string) {
    switch {
    case d < 50*time.Millisecond:
        return "🐆", "Cheetah (fast)"
    case d < 150*time.Millisecond:
        return "🐇", "Rabbit (moderate)"
    default:
        return "🐢", "Turtle (slow)"
    }
}

// pingHost measures latency to the given host using the supplied dialer.
// The dialer is injected to allow deterministic testing.
func pingHost(host string, dialer func(network, address string, timeout time.Duration) (net.Conn, error)) (time.Duration, error) {
    start := time.Now()
    // Try common ports: 80 (http) then 443 (https) if the first fails.
    ports := []string{"80", "443"}
    var err error
    for _, p := range ports {
        _, err = dialer("tcp", net.JoinHostPort(host, p), 2*time.Second)
        if err == nil {
            break
        }
    }
    if err != nil {
        return 0, err
    }
    return time.Since(start), nil
}

func defaultDialer(network, address string, timeout time.Duration) (net.Conn, error) {
    return net.DialTimeout(network, address, timeout)
}

func main() {
    hosts := []string{}
    if len(os.Args) > 1 {
        hosts = os.Args[1:]
    } else {
        scanner := bufio.NewScanner(os.Stdin)
        for scanner.Scan() {
            line := strings.TrimSpace(scanner.Text())
            if line != "" {
                hosts = append(hosts, line)
            }
        }
        if err := scanner.Err(); err != nil {
            fmt.Fprintf(os.Stderr, "error reading stdin: %v\n", err)
            os.Exit(1)
        }
    }

    if len(hosts) == 0 {
        fmt.Fprintln(os.Stderr, "no hosts provided")
        os.Exit(1)
    }

    // Limit concurrency to 10 goroutines.
    sem := make(chan struct{}, 10)
    var wg sync.WaitGroup
    mu := &sync.Mutex{}

    for _, h := range hosts {
        wg.Add(1)
        go func(host string) {
            defer wg.Done()
            sem <- struct{}{}
            defer func() { <-sem }()

            latency, err := pingHost(host, defaultDialer)
            mu.Lock()
            defer mu.Unlock()
            if err != nil {
                fmt.Printf("%s: error – %v\n", host, err)
                return
            }
            emoji, desc := animalMetaphor(latency)
            fmt.Printf("%s: %dms – %s %s\n", host, latency.Milliseconds(), emoji, desc)
        }(h)
    }
    wg.Wait()
}
