package main

import (
	"bytes"
	"encoding/binary"
	"encoding/json"
	"fmt"
	"log"
	"net"
	"net/http"
	"os"
	"sort"
	"strconv"
	"strings"
	"sync"
	"time"
)

const (
	defaultPort        = "8080"
	defaultNTPServers  = "pool.ntp.org,time.google.com,time.nist.gov"
	ntpPacketSize      = 48
	ntpEpochOffset     = 2208988800 // Seconds between 1900-01-01 and 1970-01-01
	ntpTimeout         = 5 * time.Second
)

type NTPResponse struct {
	Server string    `json:"server"`
	Time   time.Time `json:"time"`
	Error  string    `json:"error,omitempty"`
}

type SyncResponse struct {
	ConsensusTime time.Time     `json:"consensus_time"`
	SourceTimes   []NTPResponse `json:"source_times"`
}

// ntpQueryFunc is a variable that holds the function to query an NTP server.
// It can be overridden for testing purposes.
var ntpQueryFunc = queryNTPReal

// queryNTPReal performs an actual NTP query to the given server address.
func queryNTPReal(serverAddr string) (time.Time, error) {
	conn, err := net.DialTimeout("udp", net.JoinHostPort(serverAddr, "123"), ntpTimeout)
	if err != nil {
		return time.Time{}, fmt.Errorf("dial udp: %w", err)
	}
	defer conn.Close()

	if err := conn.SetDeadline(time.Now().Add(ntpTimeout)); err != nil {
		return time.Time{}, fmt.Errorf("set deadline: %w", err)
	}

	// NTP request packet (48 bytes, mostly zeros, with LI=0, VN=3, Mode=3 (client))
	request := make([]byte, ntpPacketSize)
	request[0] = 0x1B // LI=0, VN=3, Mode=3

	_, err = conn.Write(request)
	if err != nil {
		return time.Time{}, fmt.Errorf("write request: %w", err)
	}

	response := make([]byte, ntpPacketSize)
	_, err = conn.Read(response)
	if err != nil {
		return time.Time{}, fmt.Errorf("read response: %w", err)
	}

	// Extract Transmit Timestamp (64-bit fixed-point, seconds since 1900-01-01)
	// It's at byte offset 40.
	seconds := binary.BigEndian.Uint32(response[40:44])
	fraction := binary.BigEndian.Uint32(response[44:48])

	// Convert to Unix epoch (seconds since 1970-01-01)
	unixSeconds := int64(seconds) - ntpEpochOffset
	// Convert fractional part to nanoseconds
	nanoseconds := (int64(fraction) * 1e9) / (1 << 32)

	return time.Unix(unixSeconds, nanoseconds).UTC(), nil
}

// getEnvOrDefault retrieves an environment variable or returns a default value.
func getEnvOrDefault(key, defaultValue string) string {
	if value, exists := os.LookupEnv(key); exists && value != "" {
		return value
	}
	return defaultValue
}

// syncHandler handles HTTP requests for time synchronization.
func syncHandler(w http.ResponseWriter, r *http.Request) {
	ntpServersStr := getEnvOrDefault("CHRONOSYNC_NTP_SERVERS", defaultNTPServers)
	ntpServers := strings.Split(ntpServersStr, ",")

	if len(ntpServers) == 0 || (len(ntpServers) == 1 && ntpServers[0] == "") {
		http.Error(w, "No NTP servers configured", http.StatusInternalServerError)
		return
	}

	var wg sync.WaitGroup
	results := make(chan NTPResponse, len(ntpServers))

	for _, server := range ntpServers {
		server := strings.TrimSpace(server)
		if server == "" {
			continue
		}
		wg.Add(1)
		go func(s string) {
			defer wg.Done()
			tm, err := ntpQueryFunc(s)
			if err != nil {
				results <- NTPResponse{Server: s, Time: time.Time{}, Error: err.Error()}
			} else {
				results <- NTPResponse{Server: s, Time: tm, Error: ""}
			}
		}(server)
	}

	wg.Wait()
	close(results)

	var validTimes []time.Time
	var allResponses []NTPResponse

	for res := range results {
		allResponses = append(allResponses, res)
		if res.Error == "" && !res.Time.IsZero() {
			validTimes = append(validTimes, res.Time)
		}
	}

	var consensusTime time.Time
	if len(validTimes) > 0 {
		// Calculate median time
		sort.Slice(validTimes, func(i, j int) bool {
			return validTimes[i].Before(validTimes[j])
		})
		consensusTime = validTimes[len(validTimes)/2]
	} else {
		consensusTime = time.Time{} // Zero time if no valid responses
	}

	resp := SyncResponse{
		ConsensusTime: consensusTime,
		SourceTimes:   allResponses,
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(resp)
}

func main() {
	port := getEnvOrDefault("CHRONOSYNC_PORT", defaultPort)

	http.HandleFunc("/sync", syncHandler)

	log.Printf("Cosmic Chronosync service starting on :%s", port)
	log.Printf("NTP servers: %s", getEnvOrDefault("CHRONOSYNC_NTP_SERVERS", defaultNTPServers))

	if err := http.ListenAndServe(":"+port, nil); err != nil {
		log.Fatalf("Failed to start server: %v", err)
	}
}
