package main

import (
    "crypto/rand"
    "encoding/binary"
    "fmt"
    "math"
    "math/big"
)

var adjectives = []string{
    "Dusty", "Radiant", "Silent", "Forgotten", "Bleak", "Shimmering", "Cinder", "Wasted", "Echoing", "Gloomy",
}

var nouns = []string{
    "Oasis", "Haven", "Sanctum", "Bunker", "Vault", "Refuge", "Outpost", "Shelter", "Citadel", "Harbor",
}

// generateName returns a random safe‑house name.
func generateName() string {
    adj := randomChoice(adjectives)
    noun := randomChoice(nouns)
    return fmt.Sprintf("%s %s", adj, noun)
}

// randomChoice picks a random element from slice using crypto/rand.
func randomChoice(list []string) string {
    max := big.NewInt(int64(len(list)))
    n, err := rand.Int(rand.Reader, max)
    if err != nil {
        // fallback to math/rand based on a crypto‑derived float
        idx := int(math.Floor(float64(len(list)) * randFloat()))
        return list[idx]
    }
    return list[n.Int64()]
}

// randFloat returns a float64 in [0,1) using crypto/rand.
func randFloat() float64 {
    var b [8]byte
    _, err := rand.Read(b[:])
    if err != nil {
        return 0.5
    }
    u := binary.LittleEndian.Uint64(b[:])
    return float64(u) / (1 << 64)
}

func main() {
    fmt.Println(generateName())
}
