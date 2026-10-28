package main

import (
    "fmt"
    "math/rand"
    "time"
)

var quotes = []string{
    "When the last candle flickers, the shadows will write the next chapter.",
    "Even the sun takes a coffee break before the final eclipse.",
    "The wind whispers the password to the vault of forgotten hopes.",
    "Stars are just the universe's way of leaving breadcrumbs.",
    "If the ground shakes, it's just the Earth doing a little dance.",
    "Silence is the loudest scream in the void.",
    "Rain is the sky's way of shedding tears for the world.",
    "Time is a looping playlist on an ancient jukebox.",
    "Dreams are the rehearsal for tomorrow's reality.",
    "Hope is the stubborn ember that refuses to die.",
}

// GetQuote returns a quote using the provided random source.
func GetQuote(r *rand.Rand) string {
    return quotes[r.Intn(len(quotes))]
}

func main() {
    // Seed with current time for true randomness in production.
    r := rand.New(rand.NewSource(time.Now().UnixNano()))
    fmt.Println(GetQuote(r))
}
