package main

import (
    "bufio"
    "encoding/json"
    "fmt"
    "log"
    "math/rand"
    "net/http"
    "strings"
    "sync"
    "time"
)

type broadcastMessage struct {
    Msg string `json:"msg"`
}

// staticChars are the characters used to simulate radio static.
var staticChars = []rune{'~', '*', '#'}

// randSrc is seeded for deterministic behaviour (useful for tests).
var randSrc = rand.New(rand.NewSource(42))

// addStatic injects static noise into the input string.
func addStatic(s string) string {
    var sb strings.Builder
    for _, r := range s {
        // 30% chance to replace with static.
        if randSrc.Intn(100) < 30 {
            sb.WriteRune(staticChars[randSrc.Intn(len(staticChars))])
        } else {
            sb.WriteRune(r)
        }
    }
    return sb.String()
}

type broadcaster struct {
    listeners map[chan string]struct{}
    mu        sync.Mutex
}

func newBroadcaster() *broadcaster {
    return &broadcaster{listeners: make(map[chan string]struct{})}
}

func (b *broadcaster) addListener(ch chan string) {
    b.mu.Lock()
    defer b.mu.Unlock()
    b.listeners[ch] = struct{}{}
}

func (b *broadcaster) removeListener(ch chan string) {
    b.mu.Lock()
    defer b.mu.Unlock()
    delete(b.listeners, ch)
    close(ch)
}

func (b *broadcaster) broadcast(msg string) {
    b.mu.Lock()
    defer b.mu.Unlock()
    for ch := range b.listeners {
        // Non‑blocking send; drop if listener is slow.
        select {
        case ch <- msg:
        default:
        }
    }
}

func main() {
    b := newBroadcaster()

    http.HandleFunc("/broadcast", func(w http.ResponseWriter, r *http.Request) {
        if r.Method != http.MethodPost {
            http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
            return
        }
        var bm broadcastMessage
        if err := json.NewDecoder(r.Body).Decode(&bm); err != nil {
            http.Error(w, "bad request", http.StatusBadRequest)
            return
        }
        staticMsg := addStatic(bm.Msg)
        b.broadcast(staticMsg)
        w.WriteHeader(http.StatusNoContent)
    })

    http.HandleFunc("/stream", func(w http.ResponseWriter, r *http.Request) {
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

        // Keep connection alive until client disconnects.
        notify := r.Context().Done()
        for {
            select {
            case <-notify:
                return
            case msg := <-msgCh:
                fmt.Fprintf(w, "data: %s\n\n", msg)
                flusher.Flush()
            }
        }
    })

    srv := &http.Server{Addr: ":8080", Handler: nil}
    go func() {
        log.Printf("Radio static simulator listening on %s", srv.Addr)
        if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
            log.Fatalf("server error: %v", err)
        }
    }()

    // Graceful shutdown on interrupt.
    quit := make(chan struct{})
    go func() {
        // In a real utility you would capture os.Signal here.
        // For this demo we simply block.
        <-quit
    }()
    <-quit
    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()
    srv.Shutdown(ctx)
}
