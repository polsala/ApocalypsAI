package main

import (
    "flag"
    "fmt"
    "net"
    "sync"
)

type dialFunc func(network, address string) (net.Conn, error)

var dial dialFunc = net.Dial

func scanPort(host string, port int, d dialFunc) bool {
    address := fmt.Sprintf("%s:%d", host, port)
    conn, err := d("tcp", address)
    if err != nil {
        return false
    }
    conn.Close()
    return true
}

func scanPorts(host string, start, end, workers int, d dialFunc) []int {
    ports := make(chan int, end-start+1)
    results := make(chan int)
    var wg sync.WaitGroup

    // start workers
    for i := 0; i < workers; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for p := range ports {
                if scanPort(host, p, d) {
                    results <- p
                }
            }
        }()
    }

    // feed ports to workers
    go func() {
        for p := start; p <= end; p++ {
            ports <- p
        }
        close(ports)
    }()

    // close results channel when workers finish
    go func() {
        wg.Wait()
        close(results)
    }()

    openPorts := []int{}
    for p := range results {
        openPorts = append(openPorts, p)
    }
    return openPorts
}

func main() {
    host := flag.String("host", "localhost", "target host")
    start := flag.Int("start", 1, "starting port")
    end := flag.Int("end", 1024, "ending port")
    workers := flag.Int("workers", 100, "number of concurrent workers")
    flag.Parse()

    open := scanPorts(*host, *start, *end, *workers, dial)
    for _, p := range open {
        fmt.Printf("🔓 Port %d is open! The gate swings wide.\n", p)
    }
    // report closed ports
    for p := *start; p <= *end; p++ {
        found := false
        for _, op := range open {
            if op == p {
                found = true
                break
            }
        }
        if !found {
            fmt.Printf("❌ Port %d is closed. The gate remains shut.\n", p)
        }
    }
}
