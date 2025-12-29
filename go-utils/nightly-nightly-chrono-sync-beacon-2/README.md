# Nightly Chrono-Sync Beacon

A whimsical yet crucial Go-based HTTP server designed to emit precise UTC time signals across the temporal wasteland, accompanied by a reassuring (or alarming) temporal status report. In an era of shifting realities, maintaining accurate time synchronization is paramount. This beacon serves as a reliable anchor in the chronal currents.

## Features

*   **Precise UTC Time**: Delivers current UTC time in `RFC3339Nano` format.
*   **Temporal Status Report**: Provides a whimsical message about the stability of the temporal flow.
*   **Lightweight & Concurrent**: Built with Go, it efficiently handles multiple client requests.
*   **Easy to Deploy**: A single executable for simple setup.

## Usage

### Running the Beacon Server

1.  **Clone the repository (or navigate to this utility's directory):**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/go-utils/nightly-chrono-sync-beacon
    ```

2.  **Build the Go application:**
    ```bash
    go build -o chrono-beacon src/main.go
    ```

3.  **Run the server:**
    ```bash
    ./chrono-beacon
    ```
    The beacon will start listening on `http://localhost:8080`.

### Querying the Beacon

Once the server is running, you can query it using `curl` or any HTTP client:

```bash
curl http://localhost:8080/time
```

**Example Response:**

```json
{
  "utc_time": "2023-10-27T10:30:00.123456789Z",
  "temporal_status": "Temporal flow is stable. All systems nominal."
}
```

### Calculating Temporal Drift (Client-side Example)

You can use the beacon's response to calculate your local system's time drift. Here's a simple Go client example that you can compile and run separately:

```go
package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"time"
)

type TimeResponse struct {
	UTCTime        string `json:"utc_time"`
	TemporalStatus string `json:"temporal_status"`
}

func main() {
	beaconURL := "http://localhost:8080/time"
	
	start := time.Now()
	resp, err := http.Get(beaconURL)
	if err != nil {
		fmt.Printf("Error connecting to beacon: %v\n", err)
		return
	}
	defer resp.Body.Close()
	end := time.Now()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Printf("Error reading beacon response: %v\n", err)
		return
	}

	var beaconResp TimeResponse
	err = json.Unmarshal(body, &beaconResp)
	if err != nil {
		fmt.Printf("Error parsing beacon response: %v\n", err)
		return
	}

	beaconTime, err := time.Parse(time.RFC3339Nano, beaconResp.UTCTime)
	if err != nil {
		fmt.Printf("Error parsing beacon UTC time: %v\n", err)
		return
	}

	// Estimate server time at mid-point of request
	rtt := end.Sub(start)
	estimatedServerTime := beaconTime.Add(rtt / 2)

	localTime := time.Now().UTC()
	drift := localTime.Sub(estimatedServerTime)

	fmt.Printf("--- Chrono-Sync Beacon Report ---\n")
	fmt.Printf("Beacon UTC Time: %s\n", beaconResp.UTCTime)
	fmt.Printf("Temporal Status: %s\n", beaconResp.TemporalStatus)
	fmt.Printf("Round Trip Time (RTT): %s\n", rtt)
	fmt.Printf("Estimated Local Drift: %s\n", drift)
	fmt.Printf("---------------------------------\n")

	if drift > 100*time.Millisecond || drift < -100*time.Millisecond {
		fmt.Printf("WARNING: Significant temporal drift detected! Consider recalibrating your chronometer.\n")
	} else {
		fmt.Printf("Temporal alignment within acceptable parameters.\n")
	}
}
```

To run this client example:

1.  Save the code above as `client.go` in a separate directory.
2.  Build it: `go build -o chrono-client client.go`
3.  Run it: `./chrono-client` (ensure the beacon server is running first).
