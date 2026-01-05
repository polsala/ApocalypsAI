package catfacts

import (
	"encoding/json"
	"fmt"
	"net/http"
)

type catFactResponse struct {
	Fact string `json:\\"fact\\"`
}

func FetchCatFact(apiURL string) (string, error) {
	resp, err := http.Get(apiURL)
	if err != nil {
		return "", fmt.Errorf(\\"failed to fetch cat fact: %w\\", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return "", fmt.Errorf(\\"unexpected status code: %d\\", resp.StatusCode)
	}

	var result catFactResponse
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return "", fmt.Errorf(\\"failed to decode response: %w\\", err)
	}

	return result.Fact, nil
}
