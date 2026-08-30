package main

import (
    "bufio"
    "fmt"
    "net"
    "os/exec"
    "strconv"
    "testing"
    "time"
)

func startServer(t *testing.T, port int) *exec.Cmd {
    cmd := exec.Command("go", "run", "src/main.go", "-port", strconv.Itoa(port), "-testmode")
    // Suppress output for test cleanliness
    cmd.Stdout = nil
    cmd.Stderr = nil
    if err := cmd.Start(); err != nil {
        t.Fatalf("failed to start server: %v", err)
    }
    // Give the server a moment to start listening
    time.Sleep(200 * time.Millisecond)
    return cmd
}

func TestEchoResponse(t *testing.T) {
    port := 5001
    server := startServer(t, port)
    defer server.Process.Kill()

    conn, err := net.Dial("tcp", fmt.Sprintf("localhost:%d", port))
    if err != nil {
        t.Fatalf("dial error: %v", err)
    }
    defer conn.Close()

    msg := "Hello world"
    fmt.Fprintf(conn, "%s\n", msg)

    reader := bufio.NewReader(conn)
    resp, err := reader.ReadString('\n')
    if err != nil {
        t.Fatalf("read error: %v", err)
    }
    expected := msg + " [Apocalypse]\n"
    if resp != expected {
        t.Fatalf("expected %q, got %q", expected, resp)
    }
}
