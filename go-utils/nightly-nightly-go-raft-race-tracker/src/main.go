package main

import (
	"context"
	"encoding/json"
	"flag"
	"fmt"
	"io/fs"
	"log"
	"net"
	"net/http"
	"os"
	"path/filepath"
	"strconv"
	"strings"
	"sync"
	"time"

	"github.com/hashicorp/raft"
	"github.com/hashicorp/raft-boltdb"
)

// Racer represents a participant in the race
type Racer struct {
	ID    int    `json:"id"`
	Name  string `json:"name"`
	Team  string `json:"team"`
	Position int    `json:"position"`
	Time  string `json:"time"`
}

// RaceState holds the current state of the race
type RaceState struct {
	Racers map[int]Racer `json:"racers"`
	NextID int            `json:"next_id"`
	mu     sync.RWMutex
}

// RaftCommand represents commands sent to the Raft cluster
type RaftCommand struct {
	Op  string      `json:"op"`  // "add_racer", "update_position", "reset_race"
	Key string      `json:"key"` // for updates
	Val interface{} `json:"val"` // data payload
}

// RaftFSM implements the finite state machine for Raft
type RaftFSM struct {
	state *RaceState
}

func (f *RaftFSM) Apply(log *raft.Log) interface{} {
	var cmd RaftCommand
	if err := json.Unmarshal(log.Data, &cmd); err != nil {
		log.Printf("Failed to unmarshal command: %v", err)
		return nil
	}

	f.state.mu.Lock()
	defer f.state.mu.Unlock()

	switch cmd.Op {
	case "add_racer":
		if racer, ok := cmd.Val.(map[string]interface{}); ok {
			r := Racer{
				ID:     f.state.NextID,
				Name:   racer["name"].(string),
				Team:   racer["team"].(string),
				Position: 0,
				Time:   "",
			}
			f.state.Racers[r.ID] = r
			f.state.NextID++
			return r.ID
		}
	case "update_position":
		if update, ok := cmd.Val.(map[string]interface{}); ok {
			if idStr, ok := cmd.Key.(string); ok {
				id, _ := strconv.Atoi(idStr)
				if racer, exists := f.state.Racers[id]; exists {
					position := int(update["position"].(float64))
					time := update["time"].(string)
					racer.Position = position
					racer.Time = time
					f.state.Racers[id] = racer
					return true
				}
				}
			}
	case "reset_race":
		for id := range f.state.Racers {
			f.state.Racers[id].Position = 0
			f.state.Racers[id].Time = ""
		}
		return true
	}
	return false
}

func (f *RaftFSM) Snapshot() (raft.FSMSnapshot, error) {
	f.state.mu.RLock()
	defer f.state.mu.RUnlock()

	data, err := json.Marshal(f.state)
	if err != nil {
		return nil, err
	}
	return &fsmSnapshot{data: data}, nil
}

func (f *RaftFSM) Restore(rc io.ReadCloser) error {
	defer rc.Close()
	
	f.state.mu.Lock()
	defer f.state.mu.Unlock()
	
	return json.NewDecoder(rc).Decode(f.state)
}

type fsmSnapshot struct {
	data []byte
}

func (s *fsmSnapshot) Persist(sink raft.SnapshotSink) error {
	if _, err := sink.Write(s.data); err != nil {
		return err
	}
	return sink.Close()
}

func (s *fsmSnapshot) Release() {}

// RaceTracker handles the Raft cluster and HTTP API
type RaceTracker struct {
	raft        *raft.Raft
	fsm         *RaftFSM
	transport   *raft.NetworkTransport
	store       raft.StableStore
	logStore    raft.LogStore
	snapshotStore raft.SnapshotStore
	httpPort    int
	raftPort    int
	nodeID      string
	advertiseAddr string
}

func NewRaceTracker(nodeID, advertiseAddr string, httpPort, raftPort int) (*RaceTracker, error) {
	tracker := &RaceTracker{
		nodeID:      nodeID,
		httpPort:    httpPort,
		raftPort:    raftPort,
		advertiseAddr: advertiseAddr,
		fsm:         &RaftFSM{state: &RaceState{Racers: make(map[int]Racer), NextID: 1}},
	}

	// Setup Raft configuration
	config := raft.DefaultConfig()
	config.LocalID = raft.ServerID(nodeID)
	config.Logger = raft.NewLogger(log.New(os.Stderr, "[RAFT] ", log.LstdFlags))

	// Create transport
	transport, err := raft.NewTCPTransport(advertiseAddr, nil, 3, 10*time.Second, os.Stderr)
	if err != nil {
		return nil, err
	}
	tracker.transport = transport

	// Create stores
	store, err := raftboltdb.NewBoltStore(filepath.Join("data", nodeID, "raft.db"))
	if err != nil {
		return nil, err
	}
	tracker.store = store

	logStore, err := raftboltdb.NewBoltStore(filepath.Join("data", nodeID, "raft-log.db"))
	if err != nil {
		return nil, err
	}
	tracker.logStore = logStore

	snapshotStore, err := raft.NewFileSnapshotStore(filepath.Join("data", nodeID, "snapshots"), 3, os.Stderr)
	if err != nil {
		return nil, err
	}
	tracker.snapshotStore = snapshotStore

	// Create Raft instance
	raftInstance, err := raft.NewRaft(config, tracker.fsm, tracker.logStore, tracker.store, tracker.snapshotStore, transport)
	if err != nil {
		return nil, err
	}
	tracker.raft = raftInstance

	return tracker, nil
}

func (rt *RaceTracker) JoinCluster(joinAddrs []string) error {
	for _, addr := range joinAddrs {
		resp, err := http.Get(addr + "/leader")
		if err != nil {
			log.Printf("Failed to contact %s: %v", addr, err)
			continue
		}
		defer resp.Body.Close()
		
		if resp.StatusCode == http.StatusOK {
			var leaderInfo struct {
				Leader string `json:"leader"`
			}
			if err := json.NewDecoder(resp.Body).Decode(&leaderInfo); err != nil {
				continue
			}
			
			// Join the cluster
			configuration := raft.Configuration{
				Servers: []raft.Server{
					{
						ID:      raft.ServerID(rt.nodeID),
						Address: raft.ServerAddress(fmt.Sprintf("%s:%d", rt.advertiseAddr, rt.raftPort)),
					},
				},
			}
			raft.AddVoter(rt.raft, raft.ServerID(rt.nodeID), raft.ServerAddress(fmt.Sprintf("%s:%d", rt.advertiseAddr, rt.raftPort)), 0, 0)
			log.Printf("Joined cluster via leader at %s", leaderInfo.Leader)
			return nil
		}
	}
	return fmt.Errorf("could not join any cluster nodes")
}

func (rt *RaceTracker) StartHTTPServer() {
	mux := http.NewServeMux()
	mux.HandleFunc("/racers", rt.handleRacers)
	mux.HandleFunc("/racers/", rt.handleRacer)
	mux.HandleFunc("/leaderboard", rt.handleLeaderboard)
	mux.HandleFunc("/race/reset", rt.handleResetRace)
	mux.HandleFunc("/health", rt.handleHealth)
	mux.HandleFunc("/leader", rt.handleLeader)
	mux.HandleFunc("/nodes", rt.handleNodes)

	server := &http.Server{
		Addr:    fmt.Sprintf(":%d", rt.httpPort),
		Handler: mux,
	}

	log.Printf("HTTP server starting on port %d", rt.httpPort)
	log.Fatal(server.ListenAndServe())
}

func (rt *RaceTracker) handleRacers(w http.ResponseWriter, r *http.Request) {
	if r.Method == http.MethodPost {
		if !rt.ensureLeader(w) {
			return
		}
		
		var racer struct {
			Name string `json:"name"`
			Team string `json:"team"`
		}
		if err := json.NewDecoder(r.Body).Decode(&racer); err != nil {
			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}
		
		cmd := RaftCommand{
			Op:  "add_racer",
			Val: map[string]interface{}{"name": racer.Name, "team": racer.Team},
		}
		data, _ := json.Marshal(cmd)
		future := rt.raft.Apply(data, 10*time.Second)
		if err := future.Error(); err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		
		w.WriteHeader(http.StatusCreated)
		json.NewEncoder(w).Encode(map[string]interface{}{
			"success": true,
			"id":      future.Response(),
		})
		return
	}
	
	if r.Method == http.MethodGet {
		rt.fsm.state.mu.RLock()
		racers := make([]Racer, 0, len(rt.fsm.state.Racers))
		for _, racer := range rt.fsm.state.Racers {
			racers = append(racers, racer)
		}
		rt.fsm.state.mu.RUnlock()
		
		json.NewEncoder(w).Encode(racers)
		return
	}
	
	http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
}

func (rt *RaceTracker) handleRacer(w http.ResponseWriter, r *http.Request) {
	parts := strings.Split(r.URL.Path, "/")
	if len(parts) < 3 {
		http.Error(w, "Invalid path", http.StatusBadRequest)
		return
	}
	
	racerIDStr := parts[2]
	tracerID, err := strconv.Atoi(tracerIDStr)
	if err != nil {
		http.Error(w, "Invalid racer ID", http.StatusBadRequest)
		return
	}
	
	if r.Method == http.MethodGet {
		rt.fsm.state.mu.RLock()
		racer, exists := rt.fsm.state.Racers[tracerID]
		rt.fsm.state.mu.RUnlock()
		
		if !exists {
			http.Error(w, "Racer not found", http.StatusNotFound)
			return
		}
		
		json.NewEncoder(w).Encode(tracer)
		return
	}
	
	if r.Method == http.MethodPost && strings.HasSuffix(r.URL.Path, "/position") {
		if !rt.ensureLeader(w) {
			return
		}
		
		var update struct {
			Position int    `json:"position"`
			Time     string `json:"time"`
		}
		if err := json.NewDecoder(r.Body).Decode(&update); err != nil {
			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}
		
		cmd := RaftCommand{
			Op:  "update_position",
			Key: tracerIDStr,
			Val: map[string]interface{}{
				"position": update.Position,
				"time":     update.Time,
			},
		}
		data, _ := json.Marshal(cmd)
		future := rt.raft.Apply(data, 10*time.Second)
		if err := future.Error(); err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		
		w.WriteHeader(http.StatusOK)
		json.NewEncoder(w).Encode(map[string]interface{}{
			"success": true,
		})
		return
	}
	
	http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
}

func (rt *RaceTracker) handleLeaderboard(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}
	
	rt.fsm.state.mu.RLock()
	leaderboard := make([]Racer, 0, len(rt.fsm.state.Racers))
	for _, racer := range rt.fsm.state.Racers {
		if racer.Position > 0 {
			leaderboard = append(leaderboard, racer)
		}
	}
	// Sort by position
	for i := 0; i < len(leaderboard)-1; i++ {
		for j := i + 1; j < len(leaderboard); j++ {
			if leaderboard[i].Position > leaderboard[j].Position {
				leaderboard[i], leaderboard[j] = leaderboard[j], leaderboard[i]
			}
		}
	}
	rt.fsm.state.mu.RUnlock()
	
	json.NewEncoder(w).Encode(leaderboard)
}

func (rt *RaceTracker) handleResetRace(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}
	
	if !rt.ensureLeader(w) {
		return
	}
	
	cmd := RaftCommand{
		Op: "reset_race",
	}
	data, _ := json.Marshal(cmd)
	future := rt.raft.Apply(data, 10*time.Second)
	if err := future.Error(); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(map[string]interface{}{
		"success": true,
	})
}

func (rt *RaceTracker) handleHealth(w http.ResponseWriter, r *http.Request) {
	status := map[string]interface{}{
		"node_id": rt.nodeID,
		"http_port": rt.httpPort,
		"raft_port": rt.raftPort,
		"leader": rt.raft.Leader(),
		"state": rt.raft.State().String(),
	}
	json.NewEncoder(w).Encode(status)
}

func (rt *RaceTracker) handleLeader(w http.ResponseWriter, r *http.Request) {
	leader := rt.raft.Leader()
	if leader == "" {
		http.Error(w, "No leader", http.StatusServiceUnavailable)
		return
	}
	
	json.NewEncoder(w).Encode(map[string]string{
		"leader": string(leader),
	})
}

func (rt *RaceTracker) handleNodes(w http.ResponseWriter, r *http.Request) {
	configurationFuture := rt.raft.GetConfiguration()
	if err := configurationFuture.Error(); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	
	nodes := make([]map[string]interface{}, 0)
	for _, server := range configurationFuture.Configuration().Servers {
		nodes = append(nodes, map[string]interface{}{
			"id":      string(server.ID),
			"address": string(server.Address),
			"leader":  server.Address == rt.raft.Leader(),
		})
	}
	
	json.NewEncoder(w).Encode(nodes)
}

func (rt *RaceTracker) ensureLeader(w http.ResponseWriter) bool {
	if rt.raft.State() != raft.Leader {
		http.Error(w, "Not the leader", http.StatusServiceUnavailable)
		return false
	}
	return true
}

func (rt *RaceTracker) Shutdown() {
	if rt.raft != nil {
		raft.Shutdown()
	}
	if rt.transport != nil {
		raft.Transport().Close()
	}
	if rt.store != nil {
		raft.Store().Close()
	}
	if rt.logStore != nil {
		raft.LogStore().Close()
	}
}

func main() {
	nodeID := flag.String("node-id", "node1", "Unique node identifier")
	httpPort := flag.Int("http-port", 8080, "HTTP API port")
	raftPort := flag.Int("raft-port", 7001, "Raft communication port")
	advertiseAddr := flag.String("advertise-addr", "localhost", "Advertised address for Raft")
	joinAddrs := flag.String("join-addrs", "", "Comma-separated list of join addresses")
	
	flag.Parse()
	
	// Create data directory
	dataDir := filepath.Join("data", *nodeID)
	if err := os.MkdirAll(dataDir, 0755); err != nil {
		log.Fatal(err)
	}
	
	// Create race tracker
	tracker, err := NewRaceTracker(*nodeID, *advertiseAddr, *httpPort, *raftPort)
	if err != nil {
		log.Fatal(err)
	}
	
	// Join cluster if specified
	if *joinAddrs != "" {
		addrs := strings.Split(*joinAddrs, ",")
		if err := tracker.JoinCluster(addrs); err != nil {
			log.Printf("Failed to join cluster: %v", err)
		}
	}
	
	// Start HTTP server
	tracker.StartHTTPServer()
}
