package main

import (
	\"encoding/json\"
	\"math/rand\"
	\"net/http\"
	\"time\"
)

var quotes = []string{
	\"When the world ends, the jokes are still funny.\",
	\"Apocalypse is just a reset button for humanity.\",
	\"Survive the end, then enjoy the afterlife.\",
	\"Even in ruin, hope finds a way.\",
	\"Remember: the apocalypse is only a new beginning.\",
}

func init() {
	rand.Seed(time.Now().UnixNano())
}

func quoteHandler(w http.ResponseWriter, r *http.Request) {
	index := rand.Intn(len(quotes))
	resp := map[string]string{\"quote\": quotes[index]}
	w.Header().Set(\"Content-Type\", \"application/json\")
	json.NewEncoder(w).Encode(resp)
}

func main() {
	http.HandleFunc(\"/quote\", quoteHandler)
	http.ListenAndServe(\":8080\", nil)
}
