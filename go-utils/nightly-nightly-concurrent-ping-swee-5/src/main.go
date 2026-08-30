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

// dialFunc abstracts the network dialing operation for easier testing.
type dialFunc func(network, address string, timeout time.Duration) error

// dial is the production implementation using net.DialTimeout.
var dial dialFunc = net.DialTimeout

// checkHost attempts to open a TCP connection to host:80 within the given timeout.
// It returns true if the connection succeeds, false otherwise.
func checkHost(host string, timeout time.Duration) bool {
    // Ensure the host does not contain a scheme or path.
    host = strings.TrimSpace(host)
    if host == "" {
        return false
    }
    address := net.JoinHostPort(host, "80")
    err := dial("tcp", address, timeout)
    return err == nil
}

func main() {
    // Command‑line flags.
    maxConcurrency := flag.Int("c", 10, "maximum concurrent checks")
    timeoutMs := flag.Int("t", 500, "timeout per connection in milliseconds")
    flag.Parse()

    timeout := time.Duration(*timeoutMs) * time.Millisecond

    // Gather hosts from arguments or stdin.
    var hosts []string
    if flag.NArg() > 0 {
        hosts = flag.Args()
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

    // Concurrency control.
    sem := make(chan struct{}, *maxConcurrency)
    var wg sync.WaitGroup
    results := make(chan string, len(hosts))

    for _, host := range hosts {
        wg.Add(1)
        go func(h string) {
            defer wg.Done()
            sem <- struct{}{} // acquire
            reachable := checkHost(h, timeout)
            <-sem // release
            if reachable {
                results <- h
            }
        }(host)
    }

    wg.Wait()
    close(results)

    // Print reachable hosts.
    fmt.Println("Reachable hosts:")
    for h := range results {
        fmt.Println("- ", h)
    }
}
