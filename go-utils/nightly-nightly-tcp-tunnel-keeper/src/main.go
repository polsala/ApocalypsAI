package main

import (
    "flag"
    "fmt"
    "io"
    "log"
    "net"
    "strconv"
    "strings"
    "time"
)

type Config struct {
    LocalPort  int
    RemoteAddr string
    Delay      time.Duration
}

// parseArgs parses command‑line flags into a Config.
// Returns an error if required flags are missing or malformed.
func parseArgs() (*Config, error) {
    var (
        local = flag.Int("l", 0, "local listening port")
        remote = flag.String("r", "", "remote address host:port")
        delayMs = flag.Int("d", 0, "artificial latency in milliseconds")
    )
    flag.Parse()
    if *local <= 0 {
        return nil, fmt.Errorf("invalid local port: %d", *local)
    }
    if *remote == "" || !strings.Contains(*remote, ":") {
        return nil, fmt.Errorf("invalid remote address: %s", *remote)
    }
    // Validate remote port numeric
    parts := strings.Split(*remote, ":")
    if _, err := strconv.Atoi(parts[1]); err != nil {
        return nil, fmt.Errorf("invalid remote port: %s", parts[1])
    }
    cfg := &Config{
        LocalPort:  *local,
        RemoteAddr: *remote,
        Delay:      time.Duration(*delayMs) * time.Millisecond,
    }
    return cfg, nil
}

// delayedConn wraps a net.Conn and adds a fixed delay to each Read and Write.
type delayedConn struct {
    net.Conn
    delay time.Duration
}

func (d *delayedConn) Read(b []byte) (int, error) {
    if d.delay > 0 {
        time.Sleep(d.delay)
    }
    return d.Conn.Read(b)
}

func (d *delayedConn) Write(b []byte) (int, error) {
    if d.delay > 0 {
        time.Sleep(d.delay)
    }
    return d.Conn.Write(b)
}

// handleConnection forwards data between src and dst, applying optional latency.
func handleConnection(src net.Conn, cfg *Config) {
    defer src.Close()
    dst, err := net.Dial("tcp", cfg.RemoteAddr)
    if err != nil {
        log.Printf("failed to connect to remote %s: %v", cfg.RemoteAddr, err)
        return
    }
    defer dst.Close()
    log.Printf("new tunnel %s <-> %s", src.RemoteAddr(), cfg.RemoteAddr)

    // Wrap connections if latency is requested.
    if cfg.Delay > 0 {
        src = &delayedConn{Conn: src, delay: cfg.Delay}
        dst = &delayedConn{Conn: dst, delay: cfg.Delay}
    }

    // Bidirectional copy.
    go io.Copy(dst, src)
    io.Copy(src, dst)
}

func main() {
    cfg, err := parseArgs()
    if err != nil {
        log.Fatalf("argument error: %v", err)
    }
    listenAddr := fmt.Sprintf(":%d", cfg.LocalPort)
    listener, err := net.Listen("tcp", listenAddr)
    if err != nil {
        log.Fatalf("failed to listen on %s: %v", listenAddr, err)
    }
    defer listener.Close()
    log.Printf("listening on %s, forwarding to %s, delay=%v", listenAddr, cfg.RemoteAddr, cfg.Delay)

    for {
        conn, err := listener.Accept()
        if err != nil {
            log.Printf("accept error: %v", err)
            continue
        }
        go handleConnection(conn, cfg)
    }
}
