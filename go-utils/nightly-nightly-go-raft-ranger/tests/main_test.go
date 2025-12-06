package main

import (
	"testing"
	"time"
)

// TestNewRaftCluster creates a cluster and verifies initial state
func TestNewRaftCluster(t *testing.T) {
	cluster := NewRaftCluster(3)
	
	if len(cluster.Nodes) != 3 {
		t.Errorf("Expected 3 nodes, got %d", len(cluster.Nodes))
	}
	
	if cluster.LeaderID != -1 {
		t.Errorf("Expected no leader initially, got %d", cluster.LeaderID)
	}
	
	if cluster.CurrentTerm != 0 {
		t.Errorf("Expected term 0 initially, got %d", cluster.CurrentTerm)
	}
	
	for i, node := range cluster.Nodes {
		if node.ID != i {
			t.Errorf("Expected node ID %d, got %d", i, node.ID)
		}
		if node.Status != "follower" {
			t.Errorf("Expected node %d status 'follower', got '%s'", i, node.Status)
		}
		if !node.Alive {
			t.Errorf("Expected node %d to be alive", i)
		}
	}
}

// TestStartElection tests leader election
func TestStartElection(t *testing.T) {
	cluster := NewRaftCluster(3)
	
	// Start election for node 0
	cluster.StartElection(0)
	
	// Give time for election to complete
	time.Sleep(100 * time.Millisecond)
	
	// Check if there's a leader
	if cluster.LeaderID == -1 {
		t.Error("Expected a leader after election")
	}
	
	// Verify leader status
	leader := cluster.Nodes[cluster.LeaderID]
	leader.Mutex.RLock()
	if leader.Status != "leader" {
		t.Errorf("Expected leader status, got '%s'", leader.Status)
	}
	leader.Mutex.RUnlock()
}

// TestKillNode tests node failure
func TestKillNode(t *testing.T) {
	cluster := NewRaftCluster(3)
	
	// Start election
	cluster.StartElection(0)
	time.Sleep(100 * time.Millisecond)
	
	// Kill the leader
	leaderID := cluster.LeaderID
	cluster.KillNode(leaderID)
	
	// Give time for new election
	time.Sleep(200 * time.Millisecond)
	
	// Verify node is dead
	deadNode := cluster.Nodes[leaderID]
	deadNode.Mutex.RLock()
	if deadNode.Alive {
		t.Error("Expected node to be dead")
	}
	if deadNode.Status != "dead" {
		t.Errorf("Expected dead status, got '%s'", deadNode.Status)
	}
	deadNode.Mutex.RUnlock()
}

// TestReviveNode tests node revival
func TestReviveNode(t *testing.T) {
	cluster := NewRaftCluster(3)
	
	// Kill a node
	cluster.KillNode(1)
	
	// Revive the node
	cluster.ReviveNode(1)
	
	// Check if node is alive
	node := cluster.Nodes[1]
	node.Mutex.RLock()
	if !node.Alive {
		t.Error("Expected node to be alive after revival")
	}
	if node.Status != "follower" {
		t.Errorf("Expected follower status after revival, got '%s'", node.Status)
	}
	node.Mutex.RUnlock()
}

// TestAddNode tests adding nodes
func TestAddNode(t *testing.T) {
	cluster := NewRaftCluster(2)
	initialCount := len(cluster.Nodes)
	
	cluster.AddNode()
	
	if len(cluster.Nodes) != initialCount+1 {
		t.Errorf("Expected %d nodes, got %d", initialCount+1, len(cluster.Nodes))
	}
	
	// Check new node properties
	newNode := cluster.Nodes[len(cluster.Nodes)-1]
	newNode.Mutex.RLock()
	if newNode.ID != initialCount {
		t.Errorf("Expected new node ID %d, got %d", initialCount, newNode.ID)
	}
	if !newNode.Alive {
		t.Error("Expected new node to be alive")
	}
	newNode.Mutex.RUnlock()
}

// TestRemoveNode tests removing nodes
func TestRemoveNode(t *testing.T) {
	cluster := NewRaftCluster(3)
	initialCount := len(cluster.Nodes)
	
	// Remove middle node
	cluster.RemoveNode(1)
	
	if len(cluster.Nodes) != initialCount-1 {
		t.Errorf("Expected %d nodes, got %d", initialCount-1, len(cluster.Nodes))
	}
	
	// Check node IDs are updated
	for i, node := range cluster.Nodes {
		node.Mutex.RLock()
		if node.ID != i {
			t.Errorf("Expected node ID %d, got %d", i, node.ID)
		}
		node.Mutex.RUnlock()
	}
}

// TestGetStatus tests status reporting
func TestGetStatus(t *testing.T) {
	cluster := NewRaftCluster(2)
	status := cluster.GetStatus()
	
	if status == "" {
		t.Error("Expected non-empty status")
	}
	
	if !strings.Contains(status, "Cluster Status") {
		t.Error("Expected 'Cluster Status' in status")
	}
}

// TestConcurrentElections tests multiple concurrent elections
func TestConcurrentElections(t *testing.T) {
	cluster := NewRaftCluster(5)
	
	// Start multiple elections concurrently
	for i := 0; i < 3; i++ {
		go cluster.StartElection(i)
	}
	
	// Give time for elections to complete
	time.Sleep(500 * time.Millisecond)
	
	// Should have exactly one leader
	leaderCount := 0
	for _, node := range cluster.Nodes {
		node.Mutex.RLock()
		if node.Status == "leader" {
			leaderCount++
		}
		node.Mutex.RUnlock()
	}
	
	if leaderCount != 1 {
		t.Errorf("Expected exactly 1 leader, got %d", leaderCount)
	}
}

// TestPartitionTolerance tests network partition scenarios
func TestPartitionTolerance(t *testing.T) {
	cluster := NewRaftCluster(5)
	
	// Start election
	cluster.StartElection(0)
	time.Sleep(200 * time.Millisecond)
	
	// Kill majority of nodes (simulate partition)
	cluster.KillNode(1)
	cluster.KillNode(2)
	cluster.KillNode(3)
	
	// Give time for recovery
	time.Sleep(300 * time.Millisecond)
	
	// Should still have at most one leader
	leaderCount := 0
	for _, node := range cluster.Nodes {
		node.Mutex.RLock()
		if node.Status == "leader" {
			leaderCount++
		}
		node.Mutex.RUnlock()
	}
	
	if leaderCount > 1 {
		t.Errorf("Expected at most 1 leader during partition, got %d", leaderCount)
	}
}

// TestNodeNames tests post-apocalyptic naming
func TestNodeNames(t *testing.T) {
	cluster := NewRaftCluster(12) // More than available names
	
	nameCounts := make(map[string]int)
	for _, node := range cluster.Nodes {
		node.Mutex.RLock()
		nameCounts[node.Name]++
		node.Mutex.RUnlock()
	}
	
	// Check that names are from our list and cycle properly
	for name := range nameCounts {
		found := false
		for _, validName := range postApocNames {
			if name == validName {
				found = true
				break
			}
		}
		if !found {
			t.Errorf("Unexpected node name: %s", name)
		}
	}
}

// TestTermProgression tests term incrementation
func TestTermProgression(t *testing.T) {
	cluster := NewRaftCluster(3)
	initialTerm := cluster.CurrentTerm
	
	// Trigger multiple elections
	for i := 0; i < 3; i++ {
		cluster.StartElection(i)
		time.Sleep(100 * time.Millisecond)
	}
	
	if cluster.CurrentTerm <= initialTerm {
		t.Error("Expected term to increase after elections")
	}
}

// TestVoteForConsistency tests vote consistency
func TestVoteForConsistency(t *testing.T) {
	cluster := NewRaftCluster(3)
	
	// Start election for node 0
	cluster.StartElection(0)
	time.Sleep(100 * time.Millisecond)
	
	// Check that all nodes voted for the leader
	leaderID := cluster.LeaderID
	if leaderID == -1 {
		t.Fatal("No leader elected")
	}
	
	for _, node := range cluster.Nodes {
		node.Mutex.RLock()
		if node.Alive && node.VoteFor != leaderID {
			t.Errorf("Expected node to vote for leader %d, got %d", leaderID, node.VoteFor)
		}
		node.Mutex.RUnlock()
	}
}
