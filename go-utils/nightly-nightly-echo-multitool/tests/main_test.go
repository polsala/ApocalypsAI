package main

import (
    "bufio"
    "fmt"
    "io/ioutil"
    "net"
    "net/http"
    "strings"
    "testing"
    "time"
)

func TestEchoAndStats(t *testing.T) {
    // Acquire free ports for TCP and HTTP by listening on :0 and then closing.
    tcpLn, err := net.Listen("tcp", "127.0.0.1:0")
    if err != nil {
        t.Fatalf("failed to acquire TCP port: %v", err)
    }
    tcpAddr := tcpLn.Addr().String()
    tcpLn.Close()

    httpLn, err := net.Listen("tcp", "127.0.0.1:0")
    if err != nil {
        t.Fatalf("failed to acquire HTTP port: %v", err)
    }
    httpAddr := httpLn.Addr().String()
    httpLn.Close()

    // Start the services on the chosen ports.
    startTCP(tcpAddr)
    startHTTP(httpAddr)

    // Give the goroutines a moment to start listening.
    time.Sleep(100 * time.Millisecond)

    // ---- TCP echo verification ----
    conn, err := net.Dial("tcp", tcpAddr)
    if err != nil {
        t.Fatalf("TCP dial failed: %v", err)
    }
    defer conn.Close()

    testMsg := "hello world"
    fmt.Fprintf(conn, "%s\n", testMsg)
    resp, err := bufio.NewReader(conn).ReadString('\n')
    if err != nil {
        t.Fatalf("reading echo response failed: %v", err)
    }
    resp = strings.TrimSpace(resp)
    if resp != testMsg {
        t.Fatalf("expected echo %q, got %q", testMsg, resp)
    }

    // ---- HTTP stats verification ----
    httpURL := fmt.Sprintf("http://%s/stats", httpAddr)
    httpResp, err := http.Get(httpURL)
    if err != nil {
        t.Fatalf("HTTP GET to /stats failed: %v", err)
    }
    defer httpResp.Body.Close()
    body, err := ioutil.ReadAll(httpResp.Body)
    if err != nil {
        t.Fatalf("reading HTTP body failed: %v", err)
    }
    if !strings.Contains(string(body), "total_connections 1") {
        t.Fatalf("expected stats to contain count 1, got %s", string(body))
    }
}
