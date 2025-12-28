package main

import (
    \"net/http\"
    \"net/http/httptest\"
    \"sync\"
    \"testing\"
    \"time\"
)

func TestCheckURL(t *testing.T) {
    // Setup test servers
    okServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.WriteHeader(http.StatusOK)
    }))
    defer okServer.Close()

    notFoundServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.WriteHeader(http.StatusNotFound)
    }))
    defer notFoundServer.Close()

    slowServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        time.Sleep(2 * time.Second)
        w.WriteHeader(http.StatusOK)
    }))
    defer slowServer.Close()

    client := &http.Client{Timeout: 1 * time.Second}

    tests := []struct {
        url        string
        wantStatus int
        wantErr    bool
    }{
        {okServer.URL, http.StatusOK, false},
        {notFoundServer.URL, http.StatusNotFound, false},
        {slowServer.URL, 0, true},
    }

    for _, tt := range tests {
        resCh := make(chan result, 1)
        var wg sync.WaitGroup
        wg.Add(1)
        go checkURL(tt.url, client, resCh, &wg)
        wg.Wait()
        close(resCh)
        r := <-resCh
        if tt.wantErr && r.err == nil {
            t.Errorf(\"expected error for %s, got none\", tt.url)
        }
        if !tt.wantErr && r.err != nil {
            t.Errorf(\"unexpected error for %s: %v\", tt.url, r.err)
        }
        if !tt.wantErr && r.status != tt.wantStatus {
            t.Errorf(\"expected status %d for %s, got %d\", tt.wantStatus, tt.url, r.status)
        }
    }
}
