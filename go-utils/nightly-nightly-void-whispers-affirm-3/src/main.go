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
	"Even in the wasteland, your code compiles.",
	"The void whispers: you are enough.",
	"Radiation cannot decay your spirit.",
	"You debug like a scavenger reclaims resources.",
	"Chaos is just entropy with flair.",
}

func getAffirmation() string {
	rand.Seed(time.Now().UnixNano())
	return affirmations[rand.Intn(len(affirmations))]
}

func affirmationHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(AffirmationResponse{Message: getAffirmation()})
}

func main() {
	http.HandleFunc("/affirmation", affirmationHandler)
	http.ListenAndServe(":8080", nil)
}
