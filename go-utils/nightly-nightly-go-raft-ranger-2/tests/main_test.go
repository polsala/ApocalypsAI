package main

import (
	"testing"
	"time"
)

func TestNewRaftSimulation(t *testing.T) {
	numNodes := 5
	simulation := NewRaftSimulation(numNodes, 1000*time.Millisecond)

	if len(simulation.Nodes) != numNodes {
		t.Errorf("Expected %d nodes, got %d", numNodes, len(simulation.Nodes))
	}

	if simulation.CurrentTerm != 0 {
		t.Errorf("Expected initial term 0, got %d", simulation.CurrentTerm)
	}

	if simulation.CurrentLeader != -1 {
		t.Errorf("Expected no initial leader, got %d", simulation.CurrentLeader)
	}

	for i, node := range simulation.Nodes {
		if node.ID != i {
			t.Errorf("Expected node ID %d, got %d", i, node.ID)
		}
		if node.State != Follower {
			t.Errorf("Expected node %d to be Follower, got %v", i, node.State)
		}
		if node.Term != 0 {
			t.Errorf("Expected node %d term 0, got %d", i, node.Term)
		}
	}
}

func TestNodeString(t *testing.T) {
	node := &Node{ID: 0, State: Follower}
	result := node.String()
	expected := "\033[36m[0] Follower\033[0m"
	if result != expected {
		t.Errorf("Expected %q, got %q", expected, result)
	}

	node.State = Candidate
	result = node.String()
	expected = "\033[33m[0] Candidate\033[0m"
	if result != expected {
		t.Errorf("Expected %q, got %q", expected, result)
	}

	node.State = Leader
	result = node.String()
	expected = "\033[32m[0] Leader\033[0m"
	if result != expected {
		t.Errorf("Expected %q, got %q", expected, result)
	}
}

func TestSimulateVote(t *testing.T) {
	simulation := NewRaftSimulation(3, 100*time.Millisecond)
	candidate := simulation.Nodes[0]
	candidate.State = Candidate
	candidate.Term = 1
	candidate.VoteFor = 0
	candidate.Votes = 1

	follower := simulation.Nodes[1]
	follower.State = Follower
	follower.VoteFor = -1

	// Test voting
	voted := simulation.simulateVote(follower, candidate)
	if voted && follower.VoteFor != 0 {
		t.Errorf("Expected follower to vote for candidate 0, got %d", follower.VoteFor)
	}
	if voted {
		if candidate.Votes != 2 {
			t.Errorf("Expected candidate votes to be 2, got %d", candidate.Votes)
		}
	} else {
		if candidate.Votes != 1 {
			t.Errorf("Expected candidate votes to remain 1, got %d", candidate.Votes)
		}
	}
}

func TestSimulateReplication(t *testing.T) {
	simulation := NewRaftSimulation(3, 100*time.Millisecond)
	node := simulation.Nodes[1]
	initialLogLen := len(node.Log)

	// Test successful replication
	replicated := simulation.simulateReplication(node, 1)
	if !replicated {
		t.Errorf("Expected replication to succeed")
	}
	if len(node.Log) != initialLogLen+1 {
		t.Errorf("Expected log length to increase by 1, got %d", len(node.Log))
	}
	if node.Log[len(node.Log)-1] != 1 {
		t.Errorf("Expected last log entry to be 1, got %d", node.Log[len(node.Log)-1])
	}
}

func TestStartElection(t *testing.T) {
	simulation := NewRaftSimulation(3, 100*time.Millisecond)

	// Manually trigger election
	simulation.startElection()

	// Check that there's a candidate
	candidateFound := false
	for _, node := range simulation.Nodes {
		if node.State == Candidate {
			candidateFound = true
			break
		}
	}
	if !candidateFound {
		t.Errorf("Expected to find a candidate after election start")
	}
}

// Mock rationale: These tests verify the core logic of the Raft simulation
// without requiring actual network communication or timing dependencies.
// They test node initialization, state transitions, voting, and log replication
// using deterministic logic that can be reliably tested in an isolated environment.
