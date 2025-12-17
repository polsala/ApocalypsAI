package main

import (
    "os"
    "path/filepath"
    "testing"
)

func TestAddAndShowMood(t *testing.T) {
    // Create temp directory
    dir, err := os.MkdirTemp("", "moodtest")
    if err != nil {
        t.Fatalf("Failed to create temp dir: %v", err)
    }
    defer os.RemoveAll(dir)

    dataPath := filepath.Join(dir, dataFile)

    // Add mood
    if err := addMood(dataPath, "happy", "😊"); err != nil {
        t.Fatalf("addMood failed: %v", err)
    }

    // Show last mood
    entry, err := showLastMood(dataPath)
    if err != nil {
        t.Fatalf("showLastMood failed: %v", err)
    }

    if entry.Mood != "happy" {
        t.Errorf("Expected mood 'happy', got '%s'", entry.Mood)
    }
    if entry.Emoji != "😊" {
        t.Errorf("Expected emoji '😊', got '%s'", entry.Emoji)
    }
    if entry.Timestamp == "" {
        t.Errorf("Timestamp should not be empty")
    }
}

func TestMultipleMoods(t *testing.T) {
    dir, err := os.MkdirTemp("", "moodtest")
    if err != nil {
        t.Fatalf("Failed to create temp dir: %v", err)
    }
    defer os.RemoveAll(dir)

    dataPath := filepath.Join(dir, dataFile)

    moods := []struct {
        mood  string
        emoji string
    }{
        {"sad", "😢"},
        {"excited", "🤩"},
    }

    for _, m := range moods {
        if err := addMood(dataPath, m.mood, m.emoji); err != nil {
            t.Fatalf("addMood failed: %v", err)
        }
    }

    entry, err := showLastMood(dataPath)
    if err != nil {
        t.Fatalf("showLastMood failed: %v", err)
    }

    if entry.Mood != "excited" || entry.Emoji != "🤩" {
        t.Errorf("Expected last mood 'excited 🤩', got '%s %s'", entry.Mood, entry.Emoji)
    }
}
