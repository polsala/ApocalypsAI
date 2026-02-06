package main

import (
	"encoding/json"
	"math/rand"
	"net/http"
	"time"
)

type AffirmationResponse struct {
	Affirmation string `json:"affirmation"`
}

var affirmations = []string{
	"You are a radiant force of nature, unstoppable in your kindness.",
	"The universe whispers that you are exactly where you need to be.",
	"Your potential glows brighter than the void is deep.",
	"Even in chaos, your calm is a superpower.",
	"You are a masterpiece of resilience and grace.",
}

func getAffirmation() string {
	rand.Seed(time.Now().UnixNano())
	return affirmations[rand.Intn(len(affirmations))]
}

func affirmationHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	response := AffirmationResponse{Affirmation: getAffirmation()}
	json.NewEncoder(w).Encode(response)
}

func main() {
	http.HandleFunc("/affirmation", affirmationHandler)
	http.ListenAndServe(":8080", nil)
}
