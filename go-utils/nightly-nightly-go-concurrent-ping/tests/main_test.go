package main

import (
    "fmt"
    "io/ioutil"
    "net/http"
    "net/http/httptest"
    "os"
    "sort"
    "strings"
    "testing"
    "time"
)

func TestPingURLs(t *testing.T) {
    // Server returning 200
    srv200 := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.WriteHeader(http.StatusOK)
    }))
    defer srv200.Close()

    // Server returning 404
    srv404 := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.WriteHeader(http.StatusNotFound)
    }))
    defer srv404.Close()

    // Server that times out (sleep longer than client timeout)
    srvTimeout := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        time.Sleep(6 * time.Second)
    }))
    defer srvTimeout.Close()

    urls := []string{srv200.URL, srv404.URL, srvTimeout.URL}
    tmpFile, err := ioutil.TempFile("", "urls-*.txt")
    if err != nil {
        t.Fatalf("failed to create temp file: %v", err)
    }
    defer os.Remove(tmpFile.Name())

    for _, u := range urls {
        if _, err := tmpFile.WriteString(u + "\n"); err != nil {
            t.Fatalf("failed to write to temp file: %v", err)
        }
    }
    tmpFile.Close()

    results, err := PingURLs(tmpFile.Name(), 2)
    if err != nil {
        t.Fatalf("PingURLs returned error: %v", err)
    }

    // Expected successful results (order after sorting)
    expected := []string{
        fmt.Sprintf("%s -> 200", srv200.URL),
        fmt.Sprintf("%s -> 404", srv404.URL),
    }

    // Verify timeout server produced an error entry
    foundTimeout := false
    for _, r := range results {
        if strings.Contains(r, srvTimeout.URL) && strings.Contains(r, "error") {
            foundTimeout = true
            break
        }
    }
    if !foundTimeout {
        t.Errorf("expected timeout error for %s, got results: %v", srvTimeout.URL, results)
    }

    // Verify the successful results are present
    sort.Strings(expected)
    sort.Strings(results)
    for _, exp := range expected {
        if !contains(results, exp) {
            t.Errorf("expected result %q not found in %v", exp, results)
        }
    }
}

// helper to check slice contains a string
func contains(slice []string, item string) bool {
    for _, s := range slice {
        if s == item {
            return true
        }
    }
    return false
}
