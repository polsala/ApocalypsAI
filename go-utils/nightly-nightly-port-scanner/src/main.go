package main

import (
    "flag"
    "fmt"
    "net"
    "strconv"
    "sync"
    "time"
)

func scanPort(host string, port int, timeout time.Duration) bool {
    address := fmt.Sprintf("%s:%d", host, port)
    conn, err := net.DialTimeout("tcp", address, timeout)
    if err != nil {
        return false
    }
    conn.Close()
    return true
}

func main() {
    host := flag.String("host", "localhost", "Target host")
    start := flag.Int("start", 1, "Start port")
    end := flag.Int("end", 1024, "End port")
    timeoutMs := flag.Int("timeout", 200, "Timeout per port in milliseconds")
    flag.Parse()

    if *start > *end {
        fmt.Println("Invalid range: start > end")
        return
    }

    var wg sync.WaitGroup
    var mu sync.Mutex
    openPorts := []int{}
    timeout := time.Duration(*timeoutMs) * time.Millisecond
    sem := make(chan struct{}, 100) // limit concurrency

    for port := *start; port <= *end; port++ {
        wg.Add(1)
        sem <- struct{}{}
        go func(p int) {
            defer wg.Done()
            if scanPort(*host, p, timeout) {
                mu.Lock()
                openPorts = append(openPorts, p)
                mu.Unlock()
            }
            <-sem
        }(port)
    }
    wg.Wait()

    if len(openPorts) == 0 {
        fmt.Println("No open ports found.")
        return
    }
    fmt.Println("Open ports:")
    for _, p := range openPorts {
        fmt.Printf("- %d
", p)
    }
}

