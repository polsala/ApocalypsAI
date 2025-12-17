package main

import (
    "encoding/json"
    "fmt"
    "io/ioutil"
    "os"
    "path/filepath"
    "time"
)

type MoodEntry struct {
    Timestamp string `json:\\"timestamp\\"`
    Mood      string `json:\\"mood\\"`
    Emoji     string `json:\\"emoji\\"`
}

const dataFile = "moods.json"

func loadMoods(path string) ([]MoodEntry, error) {
    if _, err := os.Stat(path); os.IsNotExist(err) {
        return []MoodEntry{}, nil
    }
    data, err := ioutil.ReadFile(path)
    if err != nil {
        return nil, err
    }
    var moods []MoodEntry
    if err := json.Unmarshal(data, &moods); err != nil {
        return nil, err
    }
    return moods, nil
}

func saveMoods(path string, moods []MoodEntry) error {
    data, err := json.MarshalIndent(moods, "", "  ")
    if err != nil {
        return err
    }
    return ioutil.WriteFile(path, data, 0644)
}

func addMood(path, mood, emoji string) error {
    moods, err := loadMoods(path)
    if err != nil {
        return err
    }
    entry := MoodEntry{
        Timestamp: time.Now().Format(time.RFC3339),
        Mood:      mood,
        Emoji:     emoji,
    }
    moods = append(moods, entry)
    return saveMoods(path, moods)
}

func showLastMood(path string) (MoodEntry, error) {
    moods, err := loadMoods(path)
    if err != nil {
        return MoodEntry{}, err
    }
    if len(moods) == 0 {
        return MoodEntry{}, fmt.Errorf("no moods logged")
    }
    return moods[len(moods)-1], nil
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: mood-tracker add <mood> <emoji> | show")
        os.Exit(1)
    }
    cmd := os.Args[1]
    dataPath := filepath.Join(".", dataFile)
    switch cmd {
    case "add":
        if len(os.Args) != 4 {
            fmt.Println("Usage: mood-tracker add <mood> <emoji>")
            os.Exit(1)
        }
        mood := os.Args[2]
        emoji := os.Args[3]
        if err := addMood(dataPath, mood, emoji); err != nil {
            fmt.Println("Error adding mood:", err)
            os.Exit(1)
        }
        fmt.Println("Mood logged:", mood, emoji)
    case "show":
        entry, err := showLastMood(dataPath)
        if err != nil {
            fmt.Println("Error:", err)
            os.Exit(1)
        }
        fmt.Printf("Last mood: %s %s (at %s)\\n", entry.Mood, entry.Emoji, entry.Timestamp)
    default:
        fmt.Println("Unknown command:", cmd)
        os.Exit(1)
    }
}
