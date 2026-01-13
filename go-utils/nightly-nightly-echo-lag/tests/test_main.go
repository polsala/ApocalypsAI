package main

import (
    "net/http"
    "sync"
    "testing"
)

type mockRoundTripper struct {
    responses map[string]*http.Response
}

func (m *mockRoundTripper) RoundTrip(req *http.Request) (*http.Response, error) {
    if resp, ok := m.responses[req.URL.String()]; ok {
        return resp, nil
    }
    return &http.Response{
        StatusCode: 404,
        Body:       http.NoBody,
        Header:     make(http.Header),
    }, nil
}

func TestWhimsicalMessage(t *testing.T) {
    tests := []struct {
        status int
        want   string
    }{
        {200, "All good!"},
        {404, "Lost in the void!"},
        {500, "Server is crying!"},
        {302, "Mysterious response."},
    }
    for _, tt := range tests {
        got := whimsicalMessage(tt.status)
        if got != tt.want {
            t.Errorf("whimsicalMessage(%d) = %q; want %q", tt.status, got, tt.want)
        }
    }
}

func TestFetchURLSuccess(t *testing.T) {
    mock := &mockRoundTripper{
        responses: map[string]*http.Response{
            "https://example.com": {
                StatusCode: 200,
                Body:       http.NoBody,
                Header:     make(http.Header),
            },
        },
    }
    client := &http.Client{Transport: mock}
    ch := make(chan Result, 1)
    var wg sync.WaitGroup
    wg.Add(1)
    go fetchURL(client, "https://example.com", &wg, ch)
    wg.Wait()
    close(ch)
    res := <-ch
    if res.StatusCode != 200 {
        t.Fatalf("expected status 200, got %d", res.StatusCode)
    }
    if res.Message != "All good!" {
        t.Fatalf("unexpected message: %s", res.Message)
    }
}

func TestFetchURLNotFound(t *testing.T) {
    mock := &mockRoundTripper{
        responses: map[string]*http.Response{
            "https://missing.com": {
                StatusCode: 404,
                Body:       http.NoBody,
                Header:     make(http.Header),
            },
        },
    }
    client := &http.Client{Transport: mock}
    ch := make(chan Result, 1)
    var wg sync.WaitGroup
    wg.Add(1)
    go fetchURL(client, "https://missing.com", &wg, ch)
    wg.Wait()
    close(ch)
    res := <-ch
    if res.StatusCode != 404 {
        t.Fatalf("expected status 404, got %d", res.StatusCode)
    }
    if res.Message != "Lost in the void!" {
        t.Fatalf("unexpected message: %s", res.Message)
    }
}
