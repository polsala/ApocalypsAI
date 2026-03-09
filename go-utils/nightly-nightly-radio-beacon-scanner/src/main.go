package main

import (
    "bufio"
    "flag"
    "fmt"
    "io"
    "net"
    "os"
    "strings"
    "sync"
    "time"
)

type Dialer func(network, address string) (net.Conn, error)

// scanHost attempts to connect to host:port, sends a minimal HTTP request,
// reads up to 1KB of response, and checks whether the response contains the keyword.
func scanHost(dialer Dialer, host string, port string, keyword string, timeout time.Duration) (bool, error) {
    address := net.JoinHostPort(host, port)
    conn, err := dialer("tcp", address)
    if err != nil {
        return false, err
    }
    defer conn.Close()

    // Set a deadline for the whole operation.
    if err := conn.SetDeadline(time.Now().Add(timeout)); err != nil {
        return false, err
    }

    // Send a simple HTTP GET request.
    _, err = fmt.Fprintf(conn, "GET / HTTP/1.0\r\n\r\n")
    if err != nil {
        return false, err
    }

    // Read up to 1KB of response.
    buf := make([]byte, 1024)
    n, err := conn.Read(buf)
    if err != nil && err != io.EOF {
        return false, err
    }
    response := string(buf[:n])
    return strings.Contains(response, keyword), nil
}

func main() {
    hostsFile := flag.String("hosts", "", "Path to file with one host per line")
    port := flag.String("port", "80", "TCP port to connect to")
    keyword := flag.String("keyword", "", "Beacon string to search for in the response")
    timeoutStr := flag.String("timeout", "2s", "Connection timeout (e.g., 2s, 500ms)")
    flag.Parse()

    if *hostsFile == "" || *keyword == "" {
        fmt.Fprintln(os.Stderr, "-hosts and -keyword are required")
        flag.Usage()
        os.Exit(1)
    }

    timeout, err := time.ParseDuration(*timeoutStr)
    if err != nil {
        fmt.Fprintf(os.Stderr, "invalid timeout: %v\n", err)
        os.Exit(1)
    }

    file, err := os.Open(*hostsFile)
    if err != nil {
        fmt.Fprintf(os.Stderr, "cannot open hosts file: %v\n", err)
        os.Exit(1)
    }
    defer file.Close()

    var hosts []string
    scanner := bufio.NewScanner(file)
    for scanner.Scan() {
        line := strings.TrimSpace(scanner.Text())
        if line != "" {
            hosts = append(hosts, line)
        }
    }
    if err := scanner.Err(); err != nil {
        fmt.Fprintf(os.Stderr, "error reading hosts file: %v\n", err)
        os.Exit(1)
    }

    // Concurrency control: limit to 100 workers.
    const maxWorkers = 100
    sem := make(chan struct{}, maxWorkers)
    var wg sync.WaitGroup
    results := make(chan string, len(hosts))

    dialer := func(network, address string) (net.Conn, error) {
        return net.DialTimeout(network, address, timeout)
    }

    for _, host := range hosts {
        wg.Add(1)
        sem <- struct{}{}
        go func(h string) {
            defer wg.Done()
            defer func() { <-sem }()
            found, err := scanHost(dialer, h, *port, *keyword, timeout)
            if err != nil {
                results <- fmt.Sprintf("%s: ERROR (%v)", h, err)
                return
            }
            if found {
                results <- fmt.Sprintf("%s: FOUND", h)
            } else {
                results <- fmt.Sprintf("%s: NOT FOUND", h)
            }
        }(host)
    }

    wg.Wait()
    close(results)

    for line := range results {
        fmt.Println(line)
    }
}
