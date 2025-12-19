package main

import (
	"bytes"
	"encoding/json"
	"io"
	"net/http"
	"net/http/httptest"
	"os"
	"path/filepath"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestRaceState(t *testing.T) {
	state := &RaceState{
		Racers: make(map[int]Racer),
		NextID: 1,
	}
	
	// Test adding racers
	r1 := Racer{ID: 1, Name: "Alice", Team: "Red"}
	state.Racers[1] = r1
	assert.Equal(t, 1, len(state.Racers))
	
	r2 := Racer{ID: 2, Name: "Bob", Team: "Blue"}
	state.Racers[2] = r2
	assert.Equal(t, 2, len(state.Racers))
	
	// Test updating positions
	state.Racers[1].Position = 1
	state.Racers[1].Time = "00:01:23.45"
	assert.Equal(t, 1, state.Racers[1].Position)
	assert.Equal(t, "00:01:23.45", state.Racers[1].Time)
}

func TestRaftFSM_Apply(t *testing.T) {
	fsm := &RaftFSM{
		state: &RaceState{
			Racers: make(map[int]Racer),
			NextID: 1,
		},
	}
	
	// Test adding a racer
	cmd1 := RaftCommand{
		Op: "add_racer",
		Val: map[string]interface{}{
			"name": "Alice",
			"team": "Red",
		},
	}
	data1, _ := json.Marshal(cmd1)
	log1 := &raft.Log{Data: data1}
	result1 := fsm.Apply(log1)
	assert.Equal(t, 1, result1)
	assert.Equal(t, 1, len(fsm.state.Racers))
	assert.Equal(t, "Alice", fsm.state.Racers[1].Name)
	assert.Equal(t, "Red", fsm.state.Racers[1].Team)
	
	// Test updating position
	cmd2 := RaftCommand{
		Op:  "update_position",
		Key: "1",
		Val: map[string]interface{}{
			"position": 1.0,
			"time":     "00:01:23.45",
		},
	}
	data2, _ := json.Marshal(cmd2)
	log2 := &raft.Log{Data: data2}
	result2 := fsm.Apply(log2)
	assert.True(t, result2.(bool))
	assert.Equal(t, 1, fsm.state.Racers[1].Position)
	assert.Equal(t, "00:01:23.45", fsm.state.Racers[1].Time)
	
	// Test reset race
	cmd3 := RaftCommand{
		Op: "reset_race",
	}
	data3, _ := json.Marshal(cmd3)
	log3 := &raft.Log{Data: data3}
	result3 := fsm.Apply(log3)
	assert.True(t, result3.(bool))
	assert.Equal(t, 0, fsm.state.Racers[1].Position)
	assert.Equal(t, "", fsm.state.Racers[1].Time)
}

func TestRaftFSM_Snapshot(t *testing.T) {
	fsm := &RaftFSM{
		state: &RaceState{
			Racers: map[int]Racer{
				1: {ID: 1, Name: "Alice", Team: "Red", Position: 1, Time: "00:01:23.45"},
				2: {ID: 2, Name: "Bob", Team: "Blue", Position: 2, Time: "00:01:30.12"},
			},
			NextID: 3,
		},
	}
	
	snapshot, err := fsm.Snapshot()
	require.NoError(t, err)
	
	// Test restore
	newFSM := &RaftFSM{state: &RaceState{Racers: make(map[int]Racer)}}
	reader := bytes.NewReader(snapshot.(*fsmSnapshot).data)
	closer := io.NopCloser(reader)
	err = newFSM.Restore(closer)
	require.NoError(t, err)
	
	assert.Equal(t, 2, len(newFSM.state.Racers))
	assert.Equal(t, 3, newFSM.state.NextID)
	assert.Equal(t, "Alice", newFSM.state.Racers[1].Name)
	assert.Equal(t, 1, newFSM.state.Racers[1].Position)
}

func TestHTTPAPI(t *testing.T) {
	// Create a test tracker
	tracker, err := NewRaceTracker("test-node", "localhost", 0, 0)
	require.NoError(t, err)
	defer tracker.Shutdown()
	
	// Create a test server
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		switch r.URL.Path {
		case "/racers":
			tracker.handleRacers(w, r)
		case "/leaderboard":
			tracker.handleLeaderboard(w, r)
		case "/health":
			tracker.handleHealth(w, r)
		default:
			http.NotFound(w, r)
		}
	}))
	defer srv.Close()
	
	// Test adding racers
	racerData := map[string]interface{}{
		"name": "Alice",
		"team": "Red",
	}
	data, _ := json.Marshal(racerData)
	resp, err := http.Post(srv.URL+"/racers", "application/json", bytes.NewBuffer(data))
	require.NoError(t, err)
	assert.Equal(t, http.StatusCreated, resp.StatusCode)
	
	var result map[string]interface{}
	json.NewDecoder(resp.Body).Decode(&result)
	assert.True(t, result["success"].(bool))
	assert.Equal(t, float64(1), result["id"])
	resp.Body.Close()
	
	// Test getting racers
	resp, err = http.Get(srv.URL + "/racers")
	require.NoError(t, err)
	assert.Equal(t, http.StatusOK, resp.StatusCode)
	
	var racers []Racer
	json.NewDecoder(resp.Body).Decode(&racers)
	assert.Equal(t, 1, len(racers))
	assert.Equal(t, "Alice", racers[0].Name)
	resp.Body.Close()
	
	// Test leaderboard
	resp, err = http.Get(srv.URL + "/leaderboard")
	require.NoError(t, err)
	assert.Equal(t, http.StatusOK, resp.StatusCode)
	
	var leaderboard []Racer
	json.NewDecoder(resp.Body).Decode(&leaderboard)
	assert.Equal(t, 0, len(leaderboard)) // No positions set yet
	resp.Body.Close()
	
	// Test health check
	resp, err = http.Get(srv.URL + "/health")
	require.NoError(t, err)
	assert.Equal(t, http.StatusOK, resp.StatusCode)
	
	var health map[string]interface{}
	json.NewDecoder(resp.Body).Decode(&health)
	assert.Equal(t, "test-node", health["node_id"])
	resp.Body.Close()
}

func TestRaceTrackerIntegration(t *testing.T) {
	// Skip integration tests by default
	if testing.Short() {
		t.Skip("Skipping integration test in short mode")
	}
	
	// Clean up any existing data
	os.RemoveAll("data")
	
	// Start first node
	node1, err := NewRaceTracker("node1", "localhost", 8080, 7001)
	require.NoError(t, err)
	defer node1.Shutdown()
	
	// Give some time for Raft to initialize
	time.Sleep(100 * time.Millisecond)
	
	// Test that we can add racers via HTTP
	racerData := map[string]interface{}{
		"name": "Speedy Sam",
		"team": "A",
	}
	data, _ := json.Marshal(tracerData)
	resp, err := http.Post("http://localhost:8080/racers", "application/json", bytes.NewBuffer(data))
	require.NoError(t, err)
	assert.Equal(t, http.StatusCreated, resp.StatusCode)
	resp.Body.Close()
	
	// Test getting leaderboard
	resp, err = http.Get("http://localhost:8080/leaderboard")
	require.NoError(t, err)
	assert.Equal(t, http.StatusOK, resp.StatusCode)
	resp.Body.Close()
	
	// Clean up
	os.RemoveAll("data")
}

func TestMain(t *testing.T) {
	// Test that main function can be called with different flags
	oldArgs := os.Args
	defer func() { os.Args = oldArgs }()
	
	// Test with minimal args
	os.Args = []string{"test", "-node-id=test", "-http-port=0", "-raft-port=0"}
	
	// We can't actually run main() in a test, but we can test the logic
	// by creating a tracker with the same parameters
	tracker, err := NewRaceTracker("test", "localhost", 0, 0)
	require.NoError(t, err)
	defer tracker.Shutdown()
	
	assert.NotNil(t, tracker)
	assert.Equal(t, "test", tracker.nodeID)
}

func TestConcurrency(t *testing.T) {
	fsm := &RaftFSM{
		state: &RaceState{
			Racers: make(map[int]Racer),
			NextID: 1,
		},
	}
	
	// Test concurrent access to race state
	concurrentOps := 100
	errChan := make(chan error, concurrentOps*2)
	
	// Goroutines adding racers
	for i := 0; i < concurrentOps; i++ {
		go func(id int) {
			cmd := RaftCommand{
				Op: "add_racer",
				Val: map[string]interface{}{
					"name": fmt.Sprintf("Racer %d", id),
					"team": "Team A",
				},
			}
			data, _ := json.Marshal(cmd)
			log := &raft.Log{Data: data}
			fsm.Apply(log)
			errChan <- nil
		}(i)
	}
	
	// Goroutines updating positions
	for i := 0; i < concurrentOps; i++ {
		go func(id int) {
			cmd := RaftCommand{
				Op:  "update_position",
				Key: fmt.Sprintf("%d", id%50), // Update existing racers
				Val: map[string]interface{}{
					"position": id % 10,
					"time":     fmt.Sprintf("00:00:%02d.%02d", id%60, id%100),
				},
			}
			data, _ := json.Marshal(cmd)
			log := &raft.Log{Data: data}
			fsm.Apply(log)
			errChan <- nil
		}(i)
	}
	
	// Wait for all operations
	for i := 0; i < concurrentOps*2; i++ {
		err := <-errChan
		assert.NoError(t, err)
	}
	
	// Verify final state
	fsm.state.mu.RLock()
	defer fsm.state.mu.RUnlock()
	
	assert.Greater(t, len(fsm.state.Racers), 0)
	for _, racer := range fsm.state.Racers {
		assert.NotEmpty(t, racer.Name)
		assert.NotEmpty(t, racer.Team)
	}
}

func BenchmarkRaceState(b *testing.B) {
	fsm := &RaftFSM{
		state: &RaceState{
			Racers: make(map[int]Racer),
			NextID: 1,
		},
	}
	
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		cmd := RaftCommand{
			Op: "add_racer",
			Val: map[string]interface{}{
				"name": fmt.Sprintf("Racer %d", i),
				"team": "Team A",
			},
		}
		data, _ := json.Marshal(cmd)
		log := &raft.Log{Data: data}
		fsm.Apply(log)
	}
}

func BenchmarkRaceStateConcurrent(b *testing.B) {
	fsm := &RaftFSM{
		state: &RaceState{
			Racers: make(map[int]Racer),
			NextID: 1,
		},
	}
	
	b.ResetTimer()
	b.RunParallel(func(pb *testing.PB) {
		i := 0
		for pb.Next() {
			cmd := RaftCommand{
				Op: "add_racer",
				Val: map[string]interface{}{
					"name": fmt.Sprintf("Racer %d", i),
					"team": "Team A",
				},
			}
			data, _ := json.Marshal(cmd)
			log := &raft.Log{Data: data}
			fsm.Apply(log)
			i++
		}
	})
}
