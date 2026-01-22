package main

import (
	"encoding/json"
	"math/rand"
	"net/http"
	"time"
)

var affirmations = []string{
	"You are a star in the void. ✨",
	"The silence empowers you. 🌌",
	"Embrace the cosmic unknown. 🌀",
	"You echo through eternity. 🌠",
	"Your thoughts ripple across galaxies. 🌍✨",
}

func getAffirmation() string {
	rand.Seed(time.Now().UnixNano())
	return affirmations[rand.Intn(len(affirmations))]
}

func handler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	voidStyle := r.URL.Query().Get("void") == "true"

	message := getAffirmation()
	if voidStyle {
		message = "🌀 ~ " + message + " ~ 🌀"
	}

	json.NewEncoder(w).Encode(map[string]string{"affirmation": message})
}

func main() {
	http.HandleFunc("/affirmation", handler)
	http.ListenAndServe(":8080", nil)
}
