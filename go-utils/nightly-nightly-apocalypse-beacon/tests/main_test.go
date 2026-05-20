package main

import (
    "errors"
    "testing"
    "time"
)

type mockPingProvider struct {
    responses map[string]struct {
        dur time.Duration
        err error
    }
}

func (m *mockPingProvider) Ping(host string) (time.Duration, error) {
    if r, ok := m.responses[host]; ok {
        return r.dur, r.err
    }
    return 0, errors.New("unknown host")
}

func TestPingAll(t *testing.T) {
    mock := &mockPingProvider{responses: map[string]struct {
        dur time.Duration
        err error
    }{
        "good:80":  {dur: 50 * time.Millisecond, err: nil},
        "bad:1234": {dur: 0, err: errors.New("timeout")},
    }}
    hosts := []string{"good:80", "bad:1234"}
    results := pingAll(hosts, mock)

    if got, want := results["good:80"], "✅ good:80 responded in 50ms"; got != want {
        t.Fatalf("unexpected result for good host: got %q, want %q", got, want)
    }
    if got, want := results["bad:1234"], "☠️ bad:1234 is unreachable (timeout)"; got != want {
        t.Fatalf("unexpected result for bad host: got %q, want %q", got, want)
    }
}
