package main

import (
    "bufio"
    "encoding/json"
    "fmt"
    "io"
    "os"
    "sort"
)

type Item struct {
    Name  string `json:"name"`
    Value int    `json:"value"`
}

type Input struct {
    Items        []Item `json:"items"`
    Participants int    `json:"participants"`
}

type Allocation struct {
    Participant int    `json:"participant"`
    Items       []Item `json:"items"`
    TotalValue  int    `json:"total_value"`
}

type Output struct {
    Allocations []Allocation `json:"allocations"`
}

// allocate performs the greedy balancing algorithm.
func allocate(inp Input) Output {
    // Defensive copy and sort items descending by value.
    items := make([]Item, len(inp.Items))
    copy(items, inp.Items)
    sort.Slice(items, func(i, j int) bool { return items[i].Value > items[j].Value })

    // Initialise allocations.
    allocs := make([]Allocation, inp.Participants)
    for i := 0; i < inp.Participants; i++ {
        allocs[i] = Allocation{Participant: i, Items: []Item{}, TotalValue: 0}
    }

    // Greedy assignment.
    for _, it := range items {
        // Find participant with smallest total value (break ties by lower index).
        minIdx := 0
        minVal := allocs[0].TotalValue
        for i := 1; i < inp.Participants; i++ {
            if allocs[i].TotalValue < minVal {
                minVal = allocs[i].TotalValue
                minIdx = i
            }
        }
        // Assign item.
        allocs[minIdx].Items = append(allocs[minIdx].Items, it)
        allocs[minIdx].TotalValue += it.Value
    }

    return Output{Allocations: allocs}
}

func main() {
    // Read all of stdin.
    reader := bufio.NewReader(os.Stdin)
    var data []byte
    for {
        chunk, err := reader.ReadBytes('\n')
        data = append(data, chunk...)
        if err == io.EOF {
            break
        }
        if err != nil {
            fmt.Fprintf(os.Stderr, "error reading stdin: %v\n", err)
            os.Exit(1)
        }
    }

    var inp Input
    if err := json.Unmarshal(data, &inp); err != nil {
        fmt.Fprintf(os.Stderr, "invalid JSON input: %v\n", err)
        os.Exit(1)
    }
    if inp.Participants <= 0 {
        fmt.Fprintln(os.Stderr, "participants must be a positive integer")
        os.Exit(1)
    }

    out := allocate(inp)
    enc := json.NewEncoder(os.Stdout)
    enc.SetIndent("", "  ")
    if err := enc.Encode(out); err != nil {
        fmt.Fprintf(os.Stderr, "error encoding output: %v\n", err)
        os.Exit(1)
    }
}
