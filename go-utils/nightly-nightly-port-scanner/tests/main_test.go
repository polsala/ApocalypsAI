package main

import (
    "net"
    "os/exec"
    "strconv"
    "strings"
    "testing"
)

func startTestServer(t *testing.T) (int, func()) {
    ln, err := net.Listen("tcp", "127.0.0.1:0")
    if err != nil {
        t.Fatalf("Failed to start test server: %v", err)
    }
    addr := ln.Addr().String()
    parts := strings.Split(addr, ":")
    p, _ := strconv.Atoi(parts[len(parts)-1])
    go func() {
        for {
            conn, err := ln.Accept()
            if err != nil {
                return
            }
            conn.Close()
        }
    }()
    return p, func() { ln.Close() }
}

func TestPortScannerFindsOpenPort(t *testing.T) {
    port, closeSrv := startTestServer(t)
    defer closeSrv()

    // Build the binary
    cmdBuild := exec.Command("go", "build", "-o", "scanner", ".")
    if out, err := cmdBuild.CombinedOutput(); err != nil {
        t.Fatalf("Build failed: %v, output: %s", err, string(out))
    }
    defer exec.Command("rm", "-f", "scanner").Run()

    // Run scanner targeting the open port
    cmdRun := exec.Command("./scanner", "-host", "127.0.0.1", "-start", strconv.Itoa(port), "-end", strconv.Itoa(port), "-timeout", "500")
    out, err := cmdRun.CombinedOutput()
    if err != nil {
        t.Fatalf("Scanner execution failed: %v, output: %s", err, string(out))
    }
    output := string(out)
    if !strings.Contains(output, strconv.Itoa(port)) {
        t.Fatalf("Expected output to contain open port %d, got: %s", port, output)
    }
}

func TestPortScannerNoOpenPorts(t *testing.T) {
    // Choose a high port range unlikely to be open
    startPort := 65000
    endPort := 65002

    cmdBuild := exec.Command("go", "build", "-o", "scanner", ".")
    if out, err := cmdBuild.CombinedOutput(); err != nil {
        t.Fatalf("Build failed: %v, output: %s", err, string(out))
    }
    defer exec.Command("rm", "-f", "scanner").Run()

    cmdRun := exec.Command("./scanner", "-host", "127.0.0.1", "-start", strconv.Itoa(startPort), "-end", strconv.Itoa(endPort), "-timeout", "200")
    out, err := cmdRun.CombinedOutput()
    if err != nil {
        t.Fatalf("Scanner execution failed: %v, output: %s", err, string(out))
    }
    output := string(out)
    if !strings.Contains(output, "No open ports found.") {
        t.Fatalf("Expected no open ports message, got: %s", output)
    }
}

