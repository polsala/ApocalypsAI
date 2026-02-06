package main

import (
    "flag"
    "fmt"
    "net"
    "sort"
    "sync"
    "time"
)

func scanPorts(host string, start, end, concurrency int) []int {
    var wg sync.WaitGroup
    sem := make(chan struct{}, concurrency)
    var mu sync.Mutex
    openPorts := []int{}

    for port := start; port <= end; port++ {
        wg.Add(1)
        go func(p int) {
            defer wg.Done()
            sem <- struct{}{}
            defer func() { <-sem }()

            address := fmt.Sprintf("%s:%d", host, p)
            conn, err := net.DialTimeout("tcp", address, 200*time.Millisecond)
            if err == nil {
                conn.Close()
                mu.Lock()
                openPorts = append(openPorts, p)
                mu.Unlock()
            }
        }(port)
    }

    wg.Wait()
    sort.Ints(openPorts)
    return openPorts
}

func main() {
    host := flag.String("host", "localhost", "target host")
    start := flag.Int("start", 1, "starting port")
    end := flag.Int("end", 65535, "ending port")
    concurrency := flag.Int("c", 100, "concurrency level")
    flag.Parse()

    ports := scanPorts(*host, *start, *end, *concurrency)
    for _, p := range ports {
        fmt.Printf("🌀 Port %d is open! The portal hums.\n", p)
    }
}
