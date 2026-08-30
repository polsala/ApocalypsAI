package main

import (
    "bufio"
    "bytes"
    "encoding/json"
    "io"
    "net/http"
    "net/http/httptest"
    "strings"
    "testing"
)

func TestBroadcastAndStream(t *testing.T) {
    // Set up server with the same handlers as main.
    b := newBroadcaster()
    mux := http.NewServeMux()
    mux.HandleFunc("/broadcast", func(w http.ResponseWriter, r *http.Request) {
        var bm broadcastMessage
        if err := json.NewDecoder(r.Body).Decode(&bm); err != nil {
            http.Error(w, "bad request", http.StatusBadRequest)
            return
        }
        staticMsg := addStatic(bm.Msg)
        b.broadcast(staticMsg)
        w.WriteHeader(http.StatusNoContent)
    })
    mux.HandleFunc("/stream", func(w http.ResponseWriter, r *http.Request) {
        flusher, ok := w.(http.Flusher)
        if !ok {
            http.Error(w, "streaming unsupported", http.StatusInternalServerError)
            return
        }
        w.Header().Set("Content-Type", "text/event-stream")
        w.Header().Set("Cache-Control", "no-cache")
        w.Header().Set("Connection", "keep-alive")
        msgCh := make(chan string, 10)
        b.addListener(msgCh)
        defer b.removeListener(msgCh)
        notify := r.Context().Done()
        for {
            select {
            case <-notify:
                return
            case msg := <-msgCh:
                io.WriteString(w, "data: "+msg+"\n\n")
                flusher.Flush()
                return // For test we only need the first message.
            }
        }
    })

    server := httptest.NewServer(mux)
    defer server.Close()

    // Send a broadcast.
    payload := `{"msg":"TestMessage"}`
    resp, err := http.Post(server.URL+"/broadcast", "application/json", strings.NewReader(payload))
    if err != nil {
        t.Fatalf("POST request failed: %v", err)
    }
    if resp.StatusCode != http.StatusNoContent {
        t.Fatalf("expected 204 No Content, got %d", resp.StatusCode)
    }
    resp.Body.Close()

    // Connect to the stream and read the first event.
    streamResp, err := http.Get(server.URL + "/stream")
    if err != nil {
        t.Fatalf("GET stream failed: %v", err)
    }
    defer streamResp.Body.Close()

    reader := bufio.NewReader(streamResp.Body)
    line, err := reader.ReadString('\n')
    if err != nil {
        t.Fatalf("reading SSE line failed: %v", err)
    }
    if !strings.HasPrefix(line, "data: ") {
        t.Fatalf("expected SSE data line, got %q", line)
    }
    received := strings.TrimSpace(strings.TrimPrefix(line, "data: "))

    // Compute expected static transformation using the same deterministic function.
    expected := addStatic("TestMessage")
    if received != expected {
        t.Fatalf("static message mismatch. expected %q, got %q", expected, received)
    }
}
