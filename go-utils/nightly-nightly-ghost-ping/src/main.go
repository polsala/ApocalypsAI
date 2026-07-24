package main

import (
    "fmt"
    "os"
    "sync"
    "time"

    "github.com/polsala/ghost-ping/ping"
)

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: ghost-ping <host1> [host2] ...")
        os.Exit(1)
    }
    hosts := os.Args[1:]
    var wg sync.WaitGroup
    results := make(chan string, len(hosts))

    for _, h := range hosts {
        wg.Add(1)
        go func(host string) {
            defer wg.Done()
            dur, err := ping.Ping(host, 2*time.Second)
            if err != nil {
                results <- fmt.Sprintf("👻 %s: timeout or error (%v)", host, err)
                return
            }
            results <- fmt.Sprintf("👻 %s: %d ms", host, dur.Milliseconds())
        }(h)
    }
    wg.Wait()
    close(results)

    for r := range results {
        fmt.Println(r)
    }
}
