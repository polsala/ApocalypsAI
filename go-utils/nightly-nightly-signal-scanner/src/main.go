package main

import (
    "bufio"
    "flag"
    "fmt"
    "net"
    "os"
    "strings"
    "sync"
    "time"
)

var (
    timeoutSec    = flag.Int("t", 2, "connection timeout in seconds")
    maxConcurrent = flag.Int("c", 10, "maximum concurrent checks")
)

// dialFunc is a variable so tests can replace it with a mock.
var dialFunc = net.DialTimeout

func checkPort(address string, timeout time.Duration) error {
    conn, err := dialFunc("tcp", address, timeout)
    if err != nil {
        return err
    }
    conn.Close()
    return nil
}

// runScanner checks each address concurrently and returns friendly messages.
func runScanner(addresses []string, timeout time.Duration, maxConc int) []string {
    sem := make(chan struct{}, maxConc)
    var wg sync.WaitGroup
    results := make([]string, len(addresses))
    for i, addr := range addresses {
        wg.Add(1)
        go func(i int, addr string) {
            defer wg.Done()
            sem <- struct{}{}
            defer func() { <-sem }()
            if err := checkPort(addr, timeout); err == nil {
                results[i] = fmt.Sprintf("Signal received from %s", addr)
            } else {
                results[i] = fmt.Sprintf("No signal from %s", addr)
            }
        }(i, strings.TrimSpace(addr))
    }
    wg.Wait()
    return results
}

func main() {
    flag.Parse()
    timeout := time.Duration(*timeoutSec) * time.Second
    scanner := bufio.NewScanner(os.Stdin)
    var inputs []string
    for scanner.Scan() {
        line := strings.TrimSpace(scanner.Text())
        if line != "" {
            inputs = append(inputs, line)
        }
    }
    if err := scanner.Err(); err != nil {
        fmt.Fprintln(os.Stderr, "error reading stdin:", err)
        os.Exit(1)
    }
    outputs := runScanner(inputs, timeout, *maxConcurrent)
    for _, out := range outputs {
        fmt.Println(out)
    }
}
