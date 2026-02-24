package main

import (
    "errors"
    "fmt"
    "net"
    "os"
    "sync"
    "time"
)

var dialer = net.DialTimeout

func pingHost(host string) (bool, error) {
    conn, err := dialer("tcp", net.JoinHostPort(host, "80"), 2*time.Second)
    if err != nil {
        return false, err
    }
    if conn != nil {
        conn.Close()
    }
    return true, nil
}

func rating(alive bool) string {
    if alive {
        return "Safe"
    }
    return "Dangerous"
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: pingpong <host1> <host2> ...")
        os.Exit(1)
    }
    hosts := os.Args[1:]

    var wg sync.WaitGroup
    results := make(chan struct {
        host  string
        alive bool
        err   error
    }, len(hosts))

    for _, h := range hosts {
        wg.Add(1)
        go func(host string) {
            defer wg.Done()
            alive, err := pingHost(host)
            results <- struct {
                host  string
                alive bool
                err   error
            }{host: host, alive: alive, err: err}
        }(h)
    }

    wg.Wait()
    close(results)

    for r := range results {
        status := "unreachable"
        if r.alive {
            status = "reachable"
        }
        fmt.Printf("%s: %s (%s)\n", r.host, status, rating(r.alive))
    }
}
