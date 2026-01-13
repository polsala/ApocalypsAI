package main

import (
    "bufio"
    "flag"
    "fmt"
    "net"
    "os"
    "strings"
    "time"
)

const (
    defaultPort = "9999"
    broadcastIP = "255.255.255.255"
)

// encodeMessage prepares a text payload for transmission.
func encodeMessage(text string) []byte {
    return []byte(strings.TrimSpace(text))
}

// decodeMessage converts a received payload back to a string.
func decodeMessage(data []byte) string {
    return string(data)
}

// listen runs a UDP listener that forwards incoming messages to the out channel.
func listen(addr string, out chan<- string, stop <-chan struct{}) {
    pc, err := net.ListenPacket("udp4", addr)
    if err != nil {
        fmt.Fprintf(os.Stderr, "listen error: %v
", err)
        close(out)
        return
    }
    defer pc.Close()
    buf := make([]byte, 4096)
    for {
        select {
        case <-stop:
            close(out)
            return
        default:
            pc.SetReadDeadline(time.Now().Add(500 * time.Millisecond))
            n, _, err := pc.ReadFrom(buf)
            if err != nil {
                if ne, ok := err.(net.Error); ok && ne.Timeout() {
                    continue
                }
                fmt.Fprintf(os.Stderr, "read error: %v
", err)
                continue
            }
            msg := decodeMessage(buf[:n])
            out <- msg
        }
    }
}

// broadcast sends messages received on the in channel to the broadcast address.
func broadcast(addr string, in <-chan string, stop <-chan struct{}) {
    udpAddr, err := net.ResolveUDPAddr("udp4", addr)
    if err != nil {
        fmt.Fprintf(os.Stderr, "resolve error: %v
", err)
        return
    }
    conn, err := net.DialUDP("udp4", nil, udpAddr)
    if err != nil {
        fmt.Fprintf(os.Stderr, "dial error: %v
", err)
        return
    }
    defer conn.Close()
    for {
        select {
        case <-stop:
            return
        case msg := <-in:
            data := encodeMessage(msg)
            _, err := conn.Write(data)
            if err != nil {
                fmt.Fprintf(os.Stderr, "write error: %v
", err)
            }
        }
    }
}

func main() {
    port := flag.String("port", defaultPort, "UDP port to use")
    flag.Parse()
    listenAddr := ":" + *port
    broadcastAddr := fmt.Sprintf("%s:%s", broadcastIP, *port)

    recvChan := make(chan string)
    sendChan := make(chan string)
    stop := make(chan struct{})
    go listen(listenAddr, recvChan, stop)
    go broadcast(broadcastAddr, sendChan, stop)

    scanner := bufio.NewScanner(os.Stdin)
    fmt.Println("Clipboard Telepathy started. Type text and press Enter to broadcast. Incoming messages will appear prefixed.")
    for {
        select {
        case msg := <-recvChan:
            fmt.Printf("[remote] %s
", msg)
        default:
            if scanner.Scan() {
                line := scanner.Text()
                sendChan <- line
            } else {
                close(stop)
                return
            }
        }
    }
}

