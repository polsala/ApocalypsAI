package main

import (
    "bytes"
    "encoding/json"
    "io/ioutil"
    "net/http"
    "net/http/httptest"
    "testing"
)

func TestEchoHandler(t *testing.T) {
    ts := httptest.NewServer(http.HandlerFunc(echoHandler))
    defer ts.Close()

    // Test GET
    resp, err := http.Get(ts.URL)
    if err != nil {
        t.Fatalf("GET request failed: %v", err)
    }
    defer resp.Body.Close()
    if resp.StatusCode != http.StatusOK {
        t.Fatalf("Expected status 200, got %d", resp.StatusCode)
    }
    bodyBytes, _ := ioutil.ReadAll(resp.Body)
    var echoResp EchoResponse
    if err := json.Unmarshal(bodyBytes, &echoResp); err != nil {
        t.Fatalf("Failed to unmarshal response: %v", err)
    }
    if echoResp.Method != "GET" || echoResp.URL != "/" {
        t.Errorf("Unexpected echo response: %+v", echoResp)
    }

    // Test POST
    payload := []byte("hello world")
    resp, err = http.Post(ts.URL, "text/plain", bytes.NewReader(payload))
    if err != nil {
        t.Fatalf("POST request failed: %v", err)
    }
    defer resp.Body.Close()
    bodyBytes, _ = ioutil.ReadAll(resp.Body)
    if err := json.Unmarshal(bodyBytes, &echoResp); err != nil {
        t.Fatalf("Failed to unmarshal POST response: %v", err)
    }
    if echoResp.Method != "POST" || echoResp.Body != string(payload) {
        t.Errorf("Unexpected POST echo response: %+v", echoResp)
    }
}
