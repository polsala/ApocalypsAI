package main

import (
    "flag"
    "fmt"
    "io"
    "math/rand"
    "net"
    "os"
    "sync"
    "time"
)

type Config struct {
    listen  string
    target  string
    latency time.Duration
    jitter  time.Duration
    loss    float64 // 0.0 - 1.0
}

func main() {
    cfg := parseFlags()
    rand.Seed(time.Now().UnixNano())

    listener, err := net.Listen("tcp", cfg.listen)
    if err != nil {
        fmt.Fprintf(os.Stderr, "listen error: %v\n", err)
        os.Exit(1)
    }
    defer listener.Close()
    fmt.Printf("Listening on %s, forwarding to %s\n", cfg.listen, cfg.target)

    for {
        clientConn, err := listener.Accept()
        if err != nil {
            fmt.Fprintf(os.Stderr, "accept error: %v\n", err)
            continue
        }
        go handleConnection(clientConn, cfg)
    }
}

func parseFlags() Config {
    listen := flag.String("listen", "", "local address to listen on (e.g., :9000)")
    target := flag.String("target", "", "remote address to forward to (e.g., example.com:80)")
    latency := flag.Int("latency", 0, "base latency in milliseconds")
    jitter := flag.Int("jitter", 0, "max jitter in milliseconds")
    loss := flag.Float64("loss", 0, "packet loss percentage (0-100)")
    flag.Parse()

    if *listen == "" || *target == "" {
        fmt.Fprintln(os.Stderr, "listen and target are required")
        flag.Usage()
        os.Exit(1)
    }

    return Config{
        listen:  *listen,
        target:  *target,
        latency: time.Duration(*latency) * time.Millisecond,
        jitter:  time.Duration(*jitter) * time.Millisecond,
        loss:    *loss / 100.0,
    }
}

func handleConnection(client net.Conn, cfg Config) {
    defer client.Close()
    remote, err := net.Dial("tcp", cfg.target)
    if err != nil {
        fmt.Fprintf(os.Stderr, "dial error: %v\n", err)
        return
    }
    defer remote.Close()

    var wg sync.WaitGroup
    wg.Add(2)
    go func() {
        defer wg.Done()
        copyWithEffects(client, remote, cfg)
    }()
    go func() {
        defer wg.Done()
        copyWithEffects(remote, client, cfg)
    }()
    wg.Wait()
}

func copyWithEffects(src net.Conn, dst net.Conn, cfg Config) {
    buf := make([]byte, 32*1024)
    for {
        n, err := src.Read(buf)
        if n > 0 {
            // Simulate packet loss
            if rand.Float64() < cfg.loss {
                // drop this chunk
                continue
            }
            // Simulate latency + jitter
            delay := cfg.latency
            if cfg.jitter > 0 {
                jitterMs := rand.Int63n(int64(cfg.jitter*2+1)) - int64(cfg.jitter)
                delay += time.Duration(jitterMs) * time.Millisecond
            }
            if delay > 0 {
                time.Sleep(delay)
            }
            _, werr := dst.Write(buf[:n])
            if werr != nil {
                return
            }
        }
        if err != nil {
            if err != io.EOF {
                // ignore other errors
            }
            return
        }
    }
}
