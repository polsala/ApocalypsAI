package main

import (
	"encoding/json"
	"math/rand"
	"net/http"
	"time"
)

type AffirmationResponse struct {
	Message string `json:"message"`
}

var affirmations = []string{
	"You are a radiant beacon of possibility in a world of endless wonders.",
	"Even in chaos, your thoughts create pockets of serenity and strength.",
	"The universe whispers: you are exactly where you need to be.",
	"Your quirks are not flaws—they are the brushstrokes of your masterpiece.",
	"You bloom beautifully in the strangest seasons of life.",
}

func getAffirmation() string {
	rand.Seed(time.Now().UnixNano())
	return affirmations[rand.Intn(len(affirmations))]
}

func affirmationHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	response := AffirmationResponse{Message: getAffirmation()}
	json.NewEncoder(w).Encode(response)
}

func main() {
	http.HandleFunc("/affirmation", affirmationHandler)
	http.ListenAndServe(":8080", nil)
}
