package main

import (
    "errors"
    "testing"
    "time"
)

func TestCheckHosts_AllAlive(t *testing.T) {
    // Save original and restore after test.
    orig := pingFunc
    defer func() { pingFunc = orig }()
    // Mock pingFunc to always succeed.
    pingFunc = func(host string, timeout time.Duration) (bool, error) {
        return true, nil
    }

    hosts := []string{"a.com", "b.com"}
    results := checkHosts(hosts, 1*time.Second)
    if len(results) != 2 {
        t.Fatalf("expected 2 results, got %d", len(results))
    }
    for _, r := range results {
        if !r.Alive {
            t.Errorf("expected host %s to be alive", r.Host)
        }
    }
}

func TestCheckHosts_Mixed(t *testing.T) {
    orig := pingFunc
    defer func() { pingFunc = orig }()
    pingFunc = func(host string, timeout time.Duration) (bool, error) {
        if host == "good.com" {
            return true, nil
        }
        return false, errors.New("dial timeout")
    }

    hosts := []string{"good.com", "bad.com"}
    results := checkHosts(hosts, 1*time.Second)
    if len(results) != 2 {
        t.Fatalf("expected 2 results, got %d", len(results))
    }
    for _, r := range results {
        if r.Host == "good.com" && !r.Alive {
            t.Errorf("good.com should be alive")
        }
        if r.Host == "bad.com" && r.Alive {
            t.Errorf("bad.com should be dead")
        }
        if r.Host == "bad.com" && r.Error == "" {
            t.Errorf("bad.com should have an error message")
        }
    }
}
