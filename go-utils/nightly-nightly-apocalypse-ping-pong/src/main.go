package main

import (
    "bufio"
    "flag"
    "fmt"
    "net"
    "os"
    "runtime"
    "strings"
    "sync"
    "time"
)

type Result struct {
    Host    string
    Latency time.Duration
    Err     error
}

func pingHost(address string, timeout time.Duration) Result {
    start := time.Now()
    conn, err := net.DialTimeout("tcp", address, timeout)
    if err != nil {
        return Result{Host: address, Latency: -1, Err: err}
    }
    conn.Close()
    return Result{Host: address, Latency: time.Since(start), Err: nil}
}

func rating(latency time.Duration) string {
    if latency < 0 {
        return "❌ Unreachable"
    }
    ms := latency.Milliseconds()
    switch {
    case ms < 50:
        return "🐇 Rabbit speed"
    case ms <= 150:
        return "🐢 Turtle pace"
    default:
        return "🦥 Sloth crawl"
    }
}

func worker(addresses <-chan string, results chan<- Result, wg *sync.WaitGroup, timeout time.Duration) {
    defer wg.Done()
    for addr := range addresses {
        res := pingHost(addr, timeout)
        results <- res
    }
}

func main() {
    filePtr := flag.String("f", "", "Path to file containing hosts (one per line)")
    timeoutPtr := flag.Int("t", 2000, "Timeout per host in milliseconds")
    flag.Parse()

    var hosts []string
    if *filePtr != "" {
        f, err := os.Open(*filePtr)
        if err != nil {
            fmt.Fprintf(os.Stderr, "Error opening file: %v\n", err)
            os.Exit(1)
        }
        scanner := bufio.NewScanner(f)
        for scanner.Scan() {
            line := strings.TrimSpace(scanner.Text())
            if line != "" {
                hosts = append(hosts, line)
            }
        }
        f.Close()
        if err := scanner.Err(); err != nil {
            fmt.Fprintf(os.Stderr, "Error reading file: %v\n", err)
            os.Exit(1)
        }
    }
    hosts = append(hosts, flag.Args()...)
    if len(hosts) == 0 {
        fmt.Fprintln(os.Stderr, "No hosts provided. Use arguments or -f file.")
        os.Exit(1)
    }

    // Ensure each host includes a port; default to 80 if missing
    for i, h := range hosts {
        if !strings.Contains(h, ":") {
            hosts[i] = fmt.Sprintf("%s:80", h)
        }
    }

    numWorkers := runtime.NumCPU()
    addressCh := make(chan string, len(hosts))
    resultCh := make(chan Result, len(hosts))
    var wg sync.WaitGroup
    timeout := time.Duration(*timeoutPtr) * time.Millisecond

    for i := 0; i < numWorkers; i++ {
        wg.Add(1)
        go worker(addressCh, resultCh, &wg, timeout)
    }

    for _, h := range hosts {
        addressCh <- h
    }
    close(addressCh)
    wg.Wait()
    close(resultCh)

    for res := range resultCh {
        fmt.Printf("%s - %v ms - %s\n", res.Host, res.Latency.Milliseconds(), rating(res.Latency))
    }
}
