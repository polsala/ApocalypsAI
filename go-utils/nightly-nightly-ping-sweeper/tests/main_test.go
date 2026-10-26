package main

import (
    "reflect"
    "testing"
)

func TestSweep_WithMock(t *testing.T) {
    // Save original and restore after test
    orig := checkHost
    defer func() { checkHost = orig }()

    // Mock implementation: return true for "good.com" and "alsogood.com", false otherwise
    checkHost = func(host string) (bool, error) {
        if host == "good.com" || host == "alsogood.com" {
            return true, nil
        }
        return false, nil
    }

    hosts := []string{"good.com", "bad.com", "alsogood.com"}
    reachable := Sweep(hosts, 2)
    expected := []string{"good.com", "alsogood.com"}
    if !reflect.DeepEqual(reachable, expected) {
        t.Fatalf("expected %v, got %v", expected, reachable)
    }
}
