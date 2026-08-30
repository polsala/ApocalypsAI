package main

import (
    "flag"
    "fmt"
    "net"
    "strings"
    "sync"
    "time"
)

type dialFunc func(network, address string) (net.Conn, error)

func scanPort(host string, port string, dialer dialFunc) bool {
    address := net.JoinHostPort(host, port)
    conn, err := dialer("tcp", address)
    if err != nil {
        return false
    }
    conn.Close()
    return true
}

func defaultDialer(network, address string) (net.Conn, error) {
    d := net.Dialer{Timeout: 500 * time.Millisecond}
    return d.Dial(network, address)
}

func main() {
    host := flag.String("host", "localhost", "Target host")
    ports := flag.String("ports", "", "Comma-separated list of ports")
    flag.Parse()
    if *ports == "" {
        fmt.Println("No ports specified")
        return
    }
    portList := strings.Split(*ports, ",")
    var wg sync.WaitGroup
    results := make(chan string, len(portList))
    for _, p := range portList {
        wg.Add(1)
        go func(port string) {
            defer wg.Done()
            if scanPort(*host, port, defaultDialer) {
                results <- fmt.Sprintf("✅ Port %s is open on %s", port, *host)
            } else {
                results <- fmt.Sprintf("❌ Port %s is closed on %s", port, *host)
            }
        }(strings.TrimSpace(p))
    }
    wg.Wait()
    close(results)
    for r := range results {
        fmt.Println(r)
    }
}
