package main

import (
    "flag"
    "fmt"
    "log"
    "net"
    "os"
    "time"
)

type Network interface {
    WriteTo(b []byte, addr *net.UDPAddr) (int, error)
    ReadFrom(b []byte) (int, *net.UDPAddr, error)
    Close() error
}

type RealNetwork struct {
    conn *net.UDPConn
}

func NewRealNetwork(addr *net.UDPAddr) (*RealNetwork, error) {
    c, err := net.ListenUDP("udp", addr)
    if err != nil {
        return nil, err
    }
    return &RealNetwork{conn: c}, nil
}

func (r *RealNetwork) WriteTo(b []byte, addr *net.UDPAddr) (int, error) {
    return r.conn.WriteToUDP(b, addr)
}

func (r *RealNetwork) ReadFrom(b []byte) (int, *net.UDPAddr, error) {
    return r.conn.ReadFromUDP(b)
}

func (r *RealNetwork) Close() error {
    return r.conn.Close()
}

// Broadcast sends msg every second to the broadcast address on the given port.
func Broadcast(msg string, port int, netif Network) error {
    defer netif.Close()
    broadcastAddr := &net.UDPAddr{IP: net.IPv4bcast, Port: port}
    ticker := time.NewTicker(1 * time.Second)
    defer ticker.Stop()
    for {
        select {
        case <-ticker.C:
            _, err := netif.WriteTo([]byte(msg), broadcastAddr)
            if err != nil {
                return err
            }
        }
    }
}

// Listen receives messages on the given port and sends them to out channel.
func Listen(port int, netif Network, out chan<- string) error {
    defer netif.Close()
    buf := make([]byte, 1024)
    for {
        n, _, err := netif.ReadFrom(buf)
        if err != nil {
            return err
        }
        out <- string(buf[:n])
    }
}

func main() {
    mode := flag.String("mode", "broadcast", "Mode: broadcast or listen")
    msg := flag.String("msg", "echo", "Message to broadcast (broadcast mode)")
    port := flag.Int("port", 9999, "UDP port")
    flag.Parse()

    addr := &net.UDPAddr{IP: net.IPv4zero, Port: *port}
    realNet, err := NewRealNetwork(addr)
    if err != nil {
        log.Fatalf("Failed to open UDP socket: %v", err)
    }

    switch *mode {
    case "broadcast":
        fmt.Printf("Broadcasting \"%s\" on port %d\n", *msg, *port)
        if err := Broadcast(*msg, *port, realNet); err != nil {
            log.Fatalf("Broadcast error: %v", err)
        }
    case "listen":
        out := make(chan string)
        go func() {
            for m := range out {
                fmt.Printf("Received: %s\n", m)
            }
        }()
        fmt.Printf("Listening on port %d\n", *port)
        if err := Listen(*port, realNet, out); err != nil {
            log.Fatalf("Listen error: %v", err)
        }
    default:
        fmt.Fprintf(os.Stderr, "Invalid mode: %s\n", *mode)
        os.Exit(1)
    }
}
