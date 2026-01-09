package main

import (
    "net/http"
    "net/http/httptest"
    "testing"
    "time"
)

func TestCheckURLs(t *testing.T) {
    // 200 OK server
    okSrv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.WriteHeader(http.StatusOK)
    }))
    defer okSrv.Close()

    // 404 server
    notFoundSrv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.WriteHeader(http.StatusNotFound)
    }))
    defer notFoundSrv.Close()

    // Delayed server to trigger timeout
    slowSrv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        time.Sleep(2 * time.Second)
        w.WriteHeader(http.StatusOK)
    }))
    defer slowSrv.Close()

    urls := []string{okSrv.URL, notFoundSrv.URL, slowSrv.URL}
    timeout := 1 * time.Second
    concurrency := 2

    results := CheckURLs(urls, timeout, concurrency)

    if len(results) != 3 {
        t.Fatalf("expected 3 results, got %d", len(results))
    }

    resMap := make(map[string]Result)
    for _, r := range results {
        resMap[r.URL] = r
    }

    // Check 200 OK
    if r, ok := resMap[okSrv.URL]; ok {
        if r.Err != nil {
            t.Errorf("expected no error for %s, got %v", okSrv.URL, r.Err)
        }
        if r.Status != http.StatusOK {
            t.Errorf("expected status 200 for %s, got %d", okSrv.URL, r.Status)
        }
    } else {
        t.Errorf("missing result for %s", okSrv.URL)
    }

    // Check 404
    if r, ok := resMap[notFoundSrv.URL]; ok {
        if r.Err != nil {
            t.Errorf("expected no error for %s, got %v", notFoundSrv.URL, r.Err)
        }
        if r.Status != http.StatusNotFound {
            t.Errorf("expected status 404 for %s, got %d", notFoundSrv.URL, r.Status)
        }
    } else {
        t.Errorf("missing result for %s", notFoundSrv.URL)
    }

    // Check timeout
    if r, ok := resMap[slowSrv.URL]; ok {
        if r.Err == nil {
            t.Errorf("expected timeout error for %s, got nil", slowSrv.URL)
        }
    } else {
        t.Errorf("missing result for %s", slowSrv.URL)
    }
}
