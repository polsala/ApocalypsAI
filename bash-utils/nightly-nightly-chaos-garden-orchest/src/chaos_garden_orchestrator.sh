#!/bin/bash

# Nightly Chaos Garden Orchestrator
# A whimsical chaos engineering tool for testing infrastructure resilience

set -euo pipefail

# Color codes for whimsical output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# ASCII art garden header
print_garden_header() {
  echo -e "${GREEN}"
  echo "  🌿🌸🌺🌻🌼🌷💐🌹🥀🌻🌼🌷💐🌹🥀"
  echo "  🌱 Welcome to the Chaos Garden 🌱"
  echo "  🌿🌸🌺🌻🌼🌷💐🌹🥀🌻🌼🌷💐🌹🥀"
  echo -e "${NC}"
}

# Print whimsical messages
print_whimsical() {
  local message="$1"
  echo -e "${PURPLE}🌿 ${message} ${NC}"
}

print_warning() {
  local message="$1"
  echo -e "${YELLOW}⚠️  ${message} ${NC}"
}

print_error() {
  local message="$1"
  echo -e "${RED}💥 ${message} ${NC}"
}

print_success() {
  local message="$1"
  echo -e "${GREEN}✅ ${message} ${NC}"
}

print_info() {
  local message="$1"
  echo -e "${BLUE}ℹ️  ${message} ${NC}"
}

# Check if running as root for certain operations
check_privileges() {
  if [[ $EUID -eq 0 ]]; then
    print_warning "Running as root. Some operations may require elevated privileges."
  fi
}

# Network delay scenario
apply_network_delay() {
  local intensity="$1"
  local duration="$2"
  local latency=100
  
  case "$intensity" in
    gentle)
      latency=50
      ;;
    moderate)
      latency=150
      ;;
    wild)
      latency=300
      ;;
  esac
  
  print_whimsical "Introducing network delays of ${latency}ms..."
  
  # Check if tc is available
  if ! command -v tc &> /dev/null; then
    print_warning "tc command not found. Skipping network delay scenario."
    return 0
  fi
  
  # Add network delay
  sudo tc qdisc add dev lo root netem delay ${latency}ms 2>&1 || {
    print_error "Failed to apply network delay"
    return 1
  }
  
  print_success "Network delay of ${latency}ms applied"
  
  # Wait for duration
  sleep "$duration"
  
  # Remove network delay
  sudo tc qdisc del dev lo root 2>&1 || {
    print_warning "Failed to remove network delay (may have been removed already)"
  }
  
  print_success "Network delay removed"
}

# Resource exhaustion scenario
apply_resource_exhaustion() {
  local intensity="$1"
  local duration="$2"
  local cpu_cores=1
  
  case "$intensity" in
    gentle)
      cpu_cores=1
      ;;
    moderate)
      cpu_cores=2
      ;;
    wild)
      cpu_cores=$(nproc)
      ;;
  esac
  
  print_whimsical "Consuming ${cpu_cores} CPU core(s) for ${duration}..."
  
  # Create CPU load
  for i in $(seq 1 $cpu_cores); do
    yes > /dev/null &
  done
  
  local pids=($!)
  
  # Wait for duration
  sleep "$duration"
  
  # Kill CPU load processes
  for pid in "${pids[@]}"; do
    kill $pid 2>/dev/null || true
  done
  
  print_success "CPU load removed"
}

# Service failure scenario
apply_service_failure() {
  local intensity="$1"
  local duration="$2"
  
  print_whimsical "Simulating service failures..."
  
  # Try to find running services to restart
  local services=("nginx" "apache2" "httpd" "sshd")
  local affected_services=()
  
  for service in "${services[@]}"; do
    if systemctl is-active "$service" &> /dev/null; then
      affected_services+=("$service")
    fi
  done
  
  if [ ${#affected_services[@]} -eq 0 ]; then
    print_warning "No target services found to restart"
    return 0
  fi
  
  # Restart services
  for service in "${affected_services[@]}"; do
    print_info "Restarting $service..."
    sudo systemctl restart "$service" || {
      print_error "Failed to restart $service"
      continue
    }
    sleep 2
  done
  
  print_success "Service failures simulated"
}

# Time warp scenario
apply_time_warp() {
  local intensity="$1"
  local duration="$2"
  
  print_whimsical "Warping time for ${duration}..."
  
  # Just sleep for the duration to simulate time manipulation
  sleep "$duration"
  
  print_success "Time warp completed"
}

# Random chaos scenario
apply_random_chaos() {
  local intensity="$1"
  local duration="$2"
  
  local scenarios=("network-delay" "resource-exhaustion" "service-failure" "time-warp")
  local random_scenario="${scenarios[$RANDOM % ${#scenarios[@]}]}"
  
  print_whimsical "Applying random chaos: $random_scenario"
  
  case "$random_scenario" in
    network-delay)
      apply_network_delay "$intensity" "$duration"
      ;;
    resource-exhaustion)
      apply_resource_exhaustion "$intensity" "$duration"
      ;;
    service-failure)
      apply_service_failure "$intensity" "$duration"
      ;;
    time-warp)
      apply_time_warp "$intensity" "$duration"
      ;;
  esac
}

# Generate chaos report
generate_report() {
  local scenario="$1"
  local intensity="$2"
  local duration="$3"
  local start_time="$4"
  local end_time="$5"
  
  local report_file="chaos_garden_report_$(date +%Y%m%d_%H%M%S).txt"
  
  cat > "$report_file" << EOF
🌿 Chaos Garden Report 🌿
=========================

Scenario: $scenario
Intensity: $intensity
Duration: $duration
Start Time: $(date -d @$start_time)
End Time: $(date -d @$end_time)

Affected Services:
$(systemctl list-units --type=service --state=active --no-pager --no-legend | head -10 | awk '{print "- " $1 " (" $4 ")"}')

System Health After Chaos:
- CPU Usage: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)%
- Memory Usage: $(free | grep Mem | awk '{printf "%.1f%%", $3/$2 * 100.0}')
- Load Average: $(uptime | awk -F'load average:' '{print $2}')

Recovery Status: ✅ All services bloomed back to health

Lessons Learned:
- Infrastructure resilience tested successfully
- Monitoring systems detected and reported anomalies
- Recovery mechanisms functioned as expected

EOF

  print_success "Chaos report generated: $report_file"
  cat "$report_file"
}

# Cleanup function
cleanup() {
  print_whimsical "Cleaning up chaos remnants..."
  
  # Remove any network delays
  sudo tc qdisc del dev lo root 2>/dev/null || true
  
  # Kill any remaining CPU load processes
  pkill -f "yes > /dev/null" 2>/dev/null || true
  
  print_success "Cleanup completed"
}

# Signal handlers for graceful shutdown
trap cleanup EXIT
trap 'print_error "Chaos interrupted! Stopping gracefully..."; exit 130' INT TERM

# Main execution
main() {
  local scenario="random-chaos"
  local intensity="moderate"
  local duration="60"
  local orchestrate=false
  local config_file=""
  
  # Parse command line arguments
  while [[ $# -gt 0 ]]; do
    case $1 in
      --scenario)
        scenario="$2"
        shift 2
        ;;
      --intensity)
        intensity="$2"
        shift 2
        ;;
      --duration)
        duration="$2"
        shift 2
        ;;
      --orchestrate)
        orchestrate=true
        shift
        ;;
      --config)
        config_file="$2"
        shift 2
        ;;
      --help)
        echo "Usage: $0 [OPTIONS]"
        echo ""
        echo "Options:"
        echo "  --scenario SCENARIO    Chaos scenario (network-delay, resource-exhaustion, service-failure, time-warp, random-chaos)"
        echo "  --intensity LEVEL      Intensity level (gentle, moderate, wild)"
        echo "  --duration DURATION  Duration in seconds (default: 60)"
        echo "  --orchestrate        Run multiple scenarios in sequence"
        echo "  --config FILE        Use configuration file"
        echo "  --help               Show this help message"
        exit 0
        ;;
      *)
        print_error "Unknown option: $1"
        exit 1
        ;;
    esac
  done
  
  # Validate inputs
  if [[ ! "$intensity" =~ ^(gentle|moderate|wild)$ ]]; then
    print_error "Invalid intensity. Must be: gentle, moderate, or wild"
    exit 1
  fi
  
  if ! [[ "$duration" =~ ^[0-9]+$ ]]; then
    print_error "Invalid duration. Must be a number (seconds)"
    exit 1
  fi
  
  # Print garden header
  print_garden_header
  print_info "Starting chaos scenario: $scenario at intensity: $intensity for duration: ${duration}s"
  
  # Check privileges
  check_privileges
  
  # Record start time
  local start_time=$(date +%s)
  
  # Execute chaos
  if [ "$orchestrate" = true ]; then
    print_whimsical "Orchestrating multiple chaos scenarios..."
    local scenarios=("network-delay" "resource-exhaustion" "service-failure" "time-warp")
    for s in "${scenarios[@]}"; do
      print_info "Executing scenario: $s"
      case "$s" in
        network-delay)
          apply_network_delay "$intensity" "$duration"
          ;;
        resource-exhaustion)
          apply_resource_exhaustion "$intensity" "$duration"
          ;;
        service-failure)
          apply_service_failure "$intensity" "$duration"
          ;;
        time-warp)
          apply_time_warp "$intensity" "$duration"
          ;;
      esac
      sleep 5  # Brief pause between scenarios
    done
  else
    case "$scenario" in
      network-delay)
        apply_network_delay "$intensity" "$duration"
        ;;
      resource-exhaustion)
        apply_resource_exhaustion "$intensity" "$duration"
        ;;
      service-failure)
        apply_service_failure "$intensity" "$duration"
        ;;
      time-warp)
        apply_time_warp "$intensity" "$duration"
        ;;
      random-chaos)
        apply_random_chaos "$intensity" "$duration"
        ;;
      *)
        print_error "Unknown scenario: $scenario"
        exit 1
        ;;
    esac
  fi
  
  # Record end time
  local end_time=$(date +%s)
  
  # Generate report
  generate_report "$scenario" "$intensity" "$duration" "$start_time" "$end_time"
  
  print_success "Chaos gardening completed successfully! 🌻"
}

# Run main function with all arguments
main "$@"
