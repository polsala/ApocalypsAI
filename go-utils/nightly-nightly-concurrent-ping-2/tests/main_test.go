package main

import (
    "fmt"
    "reflect"
    "testing"
)

// MockExecutor implements PingExecutor with predefined responses.
type MockExecutor struct {
    responses map[string]string
    errors    map[string]bool
}

func (m MockExecutor) Ping(host string) (string, error) {
    if m.errors[host] {
        return "", fmt.Errorf("mock error")
    }
    return m.responses[host], nil
}

func TestRun(t *testing.T) {
    hosts := []string{"alpha", "beta"}
    mock := MockExecutor{
        responses: map[string]string{
            "alpha": "5ms",
        },
        errors: map[string]bool{
            "beta": true,
        },
    }
    got := run(hosts, mock)
    want := map[string]string{
        "alpha": "5ms",
        "beta":  "error",
    }
    if !reflect.DeepEqual(got, want) {
        t.Fatalf("run() = %v, want %v", got, want)
    }
}

