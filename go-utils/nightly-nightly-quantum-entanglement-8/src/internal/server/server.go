package server

import (
	"context"
	"encoding/json"
	"log"
	"net/http"
	"strconv"
	"time"

	"github.com/gorilla/mux"
	"github.com/polsala/ApocalypsAI/go-utils/nightly-quantum-entanglement-checker/internal/config"
	"github.com/polsala/ApocalypsAI/go-utils/nightly-quantum-entanglement-checker/internal/quantum"
)

// Server represents the HTTP server
type Server struct {
	config  *config.Config
	srv     *http.Server
	generator *quantum.PairGenerator
	verifier  *quantum.EntanglementVerifier
	monitor   *quantum.CoherenceMonitor
}

// New creates a new server instance
func New(cfg *config.Config) *Server {
	generator := quantum.NewPairGenerator(quantum.GeneratorConfig{
		DefaultFidelity: cfg.Quantum.DefaultFidelity,
	})
	verifier := quantum.NewEntanglementVerifier()
	monitor := quantum.NewCoherenceMonitor(cfg.Quantum.MeasurementThreshold)

	router := mux.NewRouter()

	s := &Server{
		config:    cfg,
		generator: generator,
		verifier:  verifier,
		monitor:   monitor,
	}

	s.setupRoutes(router)

	srv := &http.Server{
		Addr:         ":" + strconv.Itoa(cfg.Server.Port),
		Handler:      router,
		ReadTimeout:  15 * time.Second,
		WriteTimeout: 15 * time.Second,
	}

	s.srv = srv
	return s
}

// setupRoutes configures HTTP routes
func (s *Server) setupRoutes(router *mux.Router) {
	// API routes
	api := router.PathPrefix("/api/v1").Subrouter()
	api.HandleFunc("/health", s.healthHandler).Methods("GET")
	api.HandleFunc("/entangle", s.entangleHandler).Methods("POST")
	api.HandleFunc("/verify", s.verifyHandler).Methods("GET")
	api.HandleFunc("/coherence", s.coherenceHandler).Methods("GET")
	api.HandleFunc("/monitor", s.monitorHandler).Methods("POST")

	// Web UI routes
	router.HandleFunc("/", s.indexHandler).Methods("GET")
	router.HandleFunc("/dashboard", s.dashboardHandler).Methods("GET")
}

// Start starts the HTTP server
func (s *Server) Start() error {
	log.Printf("Server listening on %s", s.srv.Addr)
	return s.srv.ListenAndServe()
}

// Shutdown gracefully shuts down the server
func (s *Server) Shutdown() error {
	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()
	return s.srv.Shutdown(ctx)
}

// healthHandler returns server health status
func (s *Server) healthHandler(w http.ResponseWriter, r *http.Request) {
	status := map[string]interface{}{
		"status":    "healthy",
		"timestamp": time.Now().UTC(),
		"version":   "1.0.0",
	}

	json.NewEncoder(w).Encode(status)
}

// entangleHandler generates entangled pairs
func (s *Server) entangleHandler(w http.ResponseWriter, r *http.Request) {
	var req struct {
		Pairs    int     `json:"pairs"`
		Fidelity float64 `json:"fidelity"`
	}

	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid request body", http.StatusBadRequest)
		return
	}

	if req.Pairs <= 0 {
		req.Pairs = 5
	}
	if req.Fidelity <= 0 || req.Fidelity > 1 {
		req.Fidelity = s.config.Quantum.DefaultFidelity
	}

	pairs, err := s.generator.GeneratePairs(req.Pairs)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	response := map[string]interface{}{
		"success": true,
		"pairs":   pairs,
		"count":   len(pairs),
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

// verifyHandler verifies entanglement between nodes
func (s *Server) verifyHandler(w http.ResponseWriter, r *http.Request) {
	nodeA := r.URL.Query().Get("nodeA")
	nodeB := r.URL.Query().Get("nodeB")

	if nodeA == "" || nodeB == "" {
		http.Error(w, "Missing nodeA or nodeB parameter", http.StatusBadRequest)
		return
	}

	result := s.verifier.VerifyEntanglement(nodeA, nodeB)

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(result)
}

// coherenceHandler returns current coherence status
func (s *Server) coherenceHandler(w http.ResponseWriter, r *http.Request) {
	status := s.monitor.GetStatus()

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(status)
}

// monitorHandler simulates monitoring for a duration
func (s *Server) monitorHandler(w http.ResponseWriter, r *http.Request) {
	var req struct {
		Duration int `json:"duration"` // seconds
	}

	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid request body", http.StatusBadRequest)
		return
	}

	if req.Duration <= 0 {
		req.Duration = 30
	}

	status := s.monitor.SimulateDecoherence(time.Duration(req.Duration) * time.Second)

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(status)
}

// indexHandler serves the main page
func (s *Server) indexHandler(w http.ResponseWriter, r *http.Request) {
	html := `<!DOCTYPE html>
<html>
<head>
    <title>Quantum Entanglement Checker</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 800px; margin: 0 auto; }
        .card { border: 1px solid #ddd; padding: 20px; margin: 10px 0; border-radius: 5px; }
        input, button { padding: 10px; margin: 5px; }
        .status { font-weight: bold; }
        .healthy { color: green; }
        .unhealthy { color: red; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌌 Quantum Entanglement Checker</h1>
        <div class="card">
            <h2>Generate Entangled Pairs</h2>
            <input type="number" id="pairs" placeholder="Number of pairs" value="5">
            <input type="number" id="fidelity" placeholder="Fidelity (0-1)" step="0.01" value="0.95">
            <button onclick="generatePairs()">Generate</button>
            <div id="generationResult"></div>
        </div>
        <div class="card">
            <h2>Verify Entanglement</h2>
            <input type="text" id="nodeA" placeholder="Node A" value="node1">
            <input type="text" id="nodeB" placeholder="Node B" value="node2">
            <button onclick="verifyEntanglement()">Verify</button>
            <div id="verificationResult"></div>
        </div>
        <div class="card">
            <h2>Coherence Monitor</h2>
            <button onclick="getCoherence()">Check Coherence</button>
            <button onclick="startMonitoring()" id="monitorBtn">Start Monitoring</button>
            <div id="coherenceResult"></div>
        </div>
    </div>
    <script>
        async function generatePairs() {
            const pairs = document.getElementById('pairs').value;
            const fidelity = document.getElementById('fidelity').value;
            const response = await fetch('/api/v1/entangle', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ pairs: parseInt(pairs), fidelity: parseFloat(fidelity) })
            });
            const data = await response.json();
            document.getElementById('generationResult').innerHTML = JSON.stringify(data, null, 2);
        }
        async function verifyEntanglement() {
            const nodeA = document.getElementById('nodeA').value;
            const nodeB = document.getElementById('nodeB').value;
            const response = await fetch(`/api/v1/verify?nodeA=${nodeA}&nodeB=${nodeB}`);
            const data = await response.json();
            document.getElementById('verificationResult').innerHTML = JSON.stringify(data, null, 2);
        }
        async function getCoherence() {
            const response = await fetch('/api/v1/coherence');
            const data = await response.json();
            document.getElementById('coherenceResult').innerHTML = JSON.stringify(data, null, 2);
        }
        let monitoring = false;
        async function startMonitoring() {
            monitoring = !monitoring;
            const btn = document.getElementById('monitorBtn');
            if (monitoring) {
                btn.textContent = 'Stop Monitoring';
                btn.style.backgroundColor = '#ff6b6b';
                while (monitoring) {
                    await getCoherence();
                    await new Promise(resolve => setTimeout(resolve, 1000));
                }
            } else {
                btn.textContent = 'Start Monitoring';
                btn.style.backgroundColor = '#51cf66';
            }
        }
    </script>
</body>
</html>`

	w.Header().Set("Content-Type", "text/html")
	w.Write([]byte(html))
}

// dashboardHandler serves a more detailed dashboard
func (s *Server) dashboardHandler(w http.ResponseWriter, r *http.Request) {
	html := `<!DOCTYPE html>
<html>
<head>
    <title>Quantum Dashboard</title>
    <style>
        body { font-family: monospace; background: #0f0f23; color: #e2e2e2; }
        .grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
        .card { background: #1a1a2e; border: 1px solid #333; padding: 20px; border-radius: 10px; }
        .metric { font-size: 2em; font-weight: bold; }
        .good { color: #51cf66; }
        .warn { color: #ffd43b; }
        .bad { color: #ff6b6b; }
    </style>
</head>
<body>
    <div class="grid">
        <div class="card">
            <h3>Coherence Level</h3>
            <div id="coherence" class="metric">--</div>
        </div>
        <div class="card">
            <h3>System Status</h3>
            <div id="status" class="metric">--</div>
        </div>
        <div class="card">
            <h3>Measurements</h3>
            <div id="measurements" class="metric">--</div>
        </div>
    </div>
    <script>
        setInterval(async () => {
            const response = await fetch('/api/v1/coherence');
            const data = await response.json();
            document.getElementById('coherence').textContent = (data.coherence * 100).toFixed(1) + '%';
            document.getElementById('measurements').textContent = data.measurements;
            
            const statusEl = document.getElementById('status');
            if (data.stable) {
                statusEl.textContent = 'STABLE';
                statusEl.className = 'metric good';
            } else {
                statusEl.textContent = 'UNSTABLE';
                statusEl.className = 'metric bad';
            }
        }, 1000);
    </script>
</body>
</html>`

	w.Header().Set("Content-Type", "text/html")
	w.Write([]byte(html))
}
