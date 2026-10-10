package main

import (
    "errors"
    "testing"
    "time"
)

// mockDial simulates network behavior for testing.
func mockDial(successHosts map[string]bool) dialFunc {
    return func(network, address string, timeout time.Duration) error {
        // Extract host part (address is host:port).
        hostPort := address
        // Split on ':' to get host.
        var host string
        if idx := strings.LastIndex(hostPort, ":"); idx != -1 {
            host = hostPort[:idx]
        } else {
            host = hostPort
        }
        if ok, exists := successHosts[host]; exists && ok {
            return nil // simulate successful connection
        }
        return errors.New("dial error") // simulate failure
    }
}

func TestCheckHost_Mocked(t *testing.T) {
    // Define which hosts should succeed.
    successMap := map[string]bool{"good.com": true, "bad.com": false}
    // Replace the global dial with our mock.
    originalDial := dial
    dial = mockDial(successMap)
    defer func() { dial = originalDial }()

    if !checkHost("good.com", 100*time.Millisecond) {
        t.Errorf("expected good.com to be reachable")
    }
    if checkHost("bad.com", 100*time.Millisecond) {
        t.Errorf("expected bad.com to be unreachable")
    }
    if checkHost("unknown.com", 100*time.Millisecond) {
        t.Errorf("expected unknown.com to be unreachable (default mock failure)")
    }
}
