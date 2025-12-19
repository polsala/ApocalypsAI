package main

import (
    "encoding/json"
    "flag"
    "fmt"
    "io/ioutil"
    "math/rand"
    "os"
    "time"
)

type Item struct {
    Name   string `json:"name"`
    Weight int    `json:"weight"`
}

// pickItem selects an item based on weight using the provided seed.
func pickItem(items []Item, seed int64) (string, error) {
    if len(items) == 0 {
        return "", fmt.Errorf("no items to choose from")
    }
    totalWeight := 0
    for _, it := range items {
        if it.Weight < 0 {
            return "", fmt.Errorf("negative weight for item %s", it.Name)
        }
        totalWeight += it.Weight
    }
    if totalWeight == 0 {
        return "", fmt.Errorf("total weight is zero")
    }
    rnd := rand.New(rand.NewSource(seed))
    r := rnd.Intn(totalWeight)
    cumulative := 0
    for _, it := range items {
        cumulative += it.Weight
        if r < cumulative {
            return it.Name, nil
        }
    }
    // Fallback – should never happen
    return items[len(items)-1].Name, nil
}

func loadItems(path string) ([]Item, error) {
    data, err := ioutil.ReadFile(path)
    if err != nil {
        return nil, err
    }
    var items []Item
    if err := json.Unmarshal(data, &items); err != nil {
        return nil, err
    }
    return items, nil
}

func main() {
    filePath := flag.String("file", "", "Path to JSON file with supplies (required)")
    seedPtr := flag.Int64("seed", 0, "Seed for RNG (optional, defaults to current time)")
    flag.Parse()

    if *filePath == "" {
        fmt.Fprintln(os.Stderr, "error: -file flag is required")
        flag.Usage()
        os.Exit(1)
    }

    items, err := loadItems(*filePath)
    if err != nil {
        fmt.Fprintf(os.Stderr, "error loading items: %v\n", err)
        os.Exit(1)
    }

    seed := *seedPtr
    if seed == 0 {
        seed = time.Now().UnixNano()
    }

    choice, err := pickItem(items, seed)
    if err != nil {
        fmt.Fprintf(os.Stderr, "error picking item: %v\n", err)
        os.Exit(1)
    }
    fmt.Println(choice)
}
