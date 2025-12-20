package main

import (
    "os"
    "path/filepath"
    "testing"
    "time"
)

func TestWatchDir(t *testing.T) {
    dir := t.TempDir()

    events := make(chan string, 1)
    go WatchDir(dir, func(name string) {
        events <- name
    })

    // Give the watcher a moment to start
    time.Sleep(200 * time.Millisecond)

    // Create a new file
    filePath := filepath.Join(dir, "testfile.txt")
    if err := os.WriteFile(filePath, []byte("hello"), 0644); err != nil {
        t.Fatalf("failed to create file: %v", err)
    }

    select {
    case name := <-events:
        if name != "testfile.txt" {
            t.Fatalf("expected testfile.txt, got %s", name)
        }
    case <-time.After(2 * time.Second):
        t.Fatal("timeout waiting for file event")
    }
}
