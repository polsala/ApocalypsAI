#!/bin/bash

# Nightly Chaos Config Validator
# Validates configuration files against chaos engineering principles

set -euo pipefail

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Scoring
TOTAL_SCORE=100
CRITICAL_ISSUES=()
WARNINGS=()
SUGGESTIONS=()

# Functions
print_header() {
    echo -e "${CYAN}${BOLD}=== Chaos Config Validator ===${NC}"
    echo
}

print_help() {
    cat << EOF
${BOLD}Nightly Chaos Config Validator${NC}

Validates configuration files against chaos engineering principles.

${BOLD}Usage:${NC}
  $0 [OPTIONS] <config_file>...

${BOLD}Options:${NC}
  --help, -h     Show this help message
  --verbose, -v  Enable verbose output

${BOLD}Examples:${NC}
  $0 config.yaml
  $0 --verbose app.json service.ini
  $0 --help

${BOLD}Supported Formats:${NC}
  - JSON
  - YAML
  - INI

EOF
}

log() {
    local level=$1
    shift
    case $level in
        ERROR)
            echo -e "${RED}[ERROR]${NC} $*" >&2
            ;;
        WARN)
            echo -e "${YELLOW}[WARN]${NC} $*"
            ;;
        INFO)
            echo -e "${BLUE}[INFO]${NC} $*"
            ;;
        SUCCESS)
            echo -e "${GREEN}[SUCCESS]${NC} $*"
            ;;
        DEBUG)
            if [[ $VERBOSE == true ]]; then
                echo -e "${PURPLE}[DEBUG]${NC} $*"
            fi
            ;;
    esac
}

check_file_exists() {
    local file=$1
    if [[ ! -f "$file" ]]; then
        log ERROR "File not found: $file"
        return 1
    fi
}

get_file_extension() {
    local file=$1
    echo "${file##*.}" | tr '[:upper:]' '[:lower:]'
}

validate_json() {
    local file=$1
    log DEBUG "Validating JSON file: $file"
    
    # Check if valid JSON
    if ! jq empty "$file" 2>/dev/null; then
        log ERROR "Invalid JSON format: $file"
        return 1
    fi
    
    # Check for single points of failure
    check_single_points_of_failure_json "$file"
    
    # Check for circuit breakers
    check_circuit_breakers_json "$file"
    
    # Check for timeouts
    check_timeouts_json "$file"
    
    # Check for retries
    check_retries_json "$file"
    
    # Check for health checks
    check_health_checks_json "$file"
    
    # Check for load balancing
    check_load_balancing_json "$file"
}

validate_yaml() {
    local file=$1
    log DEBUG "Validating YAML file: $file"
    
    # Check if valid YAML (basic check)
    if ! python3 -c "import yaml; yaml.safe_load(open('$file'))" 2>/dev/null; then
        log ERROR "Invalid YAML format: $file"
        return 1
    fi
    
    # Convert YAML to JSON for processing
    local temp_json
    temp_json=$(mktemp)
    python3 -c "import yaml, json, sys; json.dump(yaml.safe_load(open('$file')), sys.stdout)" > "$temp_json"
    
    # Validate the converted JSON
    validate_json "$temp_json"
    
    # Clean up
    rm -f "$temp_json"
}

validate_ini() {
    local file=$1
    log DEBUG "Validating INI file: $file"
    
    # Basic INI structure check
    if ! grep -q '^\[.*\]' "$file"; then
        log WARN "No sections found in INI file: $file"
    fi
    
    # Check for single points of failure
    check_single_points_of_failure_ini "$file"
    
    # Check for timeouts
    check_timeouts_ini "$file"
    
    # Check for retries
    check_retries_ini "$file"
}

check_single_points_of_failure_json() {
    local file=$1
    
    # Check for single database instances
    local db_count
    db_count=$(jq '[.services[] | select(.type == "database") // .databases[] // .db[] // .database)] | length' "$file" 2>/dev/null || echo 0)
    
    if [[ $db_count -lt 3 ]]; then
        add_critical_issue "Single point of failure: Only $db_count database instance(s) found. Recommend at least 3 for high availability."
        add_suggestion "Add at least 3 database replicas for high availability. Consider master-slave or cluster setup."
        TOTAL_SCORE=$((TOTAL_SCORE - 20))
    fi
    
    # Check for single API endpoints
    local api_count
    api_count=$(jq '[.services[] | select(.type == "api") // .endpoints[] // .api[])] | length' "$file" 2>/dev/null || echo 0)
    
    if [[ $api_count -lt 2 ]]; then
        add_warning "Only $api_count API endpoint(s) found. Consider multiple endpoints for redundancy."
        add_suggestion "Implement multiple API endpoints with load balancing for better fault tolerance."
        TOTAL_SCORE=$((TOTAL_SCORE - 10))
    fi
    
    # Check for single cache instances
    local cache_count
    cache_count=$(jq '[.services[] | select(.type == "cache") // .cache[] // .redis[] // .memcached[])] | length' "$file" 2>/dev/null || echo 0)
    
    if [[ $cache_count -lt 2 ]]; then
        add_warning "Only $cache_count cache instance(s) found. Consider multiple instances for redundancy."
        add_suggestion "Implement cache clustering or multiple cache instances for better performance and availability."
        TOTAL_SCORE=$((TOTAL_SCORE - 5))
    fi
}

check_single_points_of_failure_ini() {
    local file=$1
    
    # Check for single database configuration
    local db_hosts
    db_hosts=$(grep -c "^host.*=.*" "$file" | head -1)
    
    if [[ $db_hosts -lt 3 ]]; then
        add_critical_issue "Single point of failure: Database configuration appears to have only one host."
        add_suggestion "Configure multiple database hosts for high availability."
        TOTAL_SCORE=$((TOTAL_SCORE - 15))
    fi
}

check_circuit_breakers_json() {
    local file=$1
    
    # Check if circuit breaker configuration exists
    local has_circuit_breaker
    has_circuit_breaker=$(jq 'any(.services[]; has("circuit_breaker") or has("circuitBreaker") or .type == "circuit_breaker")' "$file" 2>/dev/null || echo false)
    
    if [[ $has_circuit_breaker == "false" ]]; then
        add_critical_issue "Missing circuit breaker configuration. Systems are vulnerable to cascading failures."
        add_suggestion "Implement circuit breakers for all external service calls to prevent cascading failures."
        TOTAL_SCORE=$((TOTAL_SCORE - 25))
    fi
}

check_timeouts_json() {
    local file=$1
    
    # Check for timeout configurations
    local has_timeouts
    has_timeouts=$(jq 'any(.services[]; has("timeout") or has("timeouts") or has("request_timeout") or has("connection_timeout"))' "$file" 2>/dev/null || echo false)
    
    if [[ $has_timeouts == "false" ]]; then
        add_warning "No timeout configurations found. Operations may hang indefinitely."
        add_suggestion "Configure appropriate timeouts for all network operations and API calls."
        TOTAL_SCORE=$((TOTAL_SCORE - 10))
    fi
    
    # Check for reasonable timeout values
    local timeout_value
    timeout_value=$(jq '.services[] | .timeout // .timeouts // .request_timeout // .connection_timeout // 0' "$file" 2>/dev/null | head -1)
    
    if [[ -n "$timeout_value" ]] && [[ $timeout_value -gt 0 ]] && [[ $timeout_value -lt 5000 ]]; then
        add_warning "Timeout value ($timeout_value ms) may be too low for some operations."
        add_suggestion "Consider increasing timeout values for slow operations or implementing retry logic."
    fi
}

check_timeouts_ini() {
    local file=$1
    
    # Check for timeout configurations
    if ! grep -q "timeout" "$file"; then
        add_warning "No timeout configurations found. Operations may hang indefinitely."
        add_suggestion "Configure appropriate timeouts for all network operations and API calls."
        TOTAL_SCORE=$((TOTAL_SCORE - 8))
    fi
}

check_retries_json() {
    local file=$1
    
    # Check for retry configurations
    local has_retries
    has_retries=$(jq 'any(.services[]; has("retry") or has("retries") or has("retry_count") or has("max_retries"))' "$file" 2>/dev/null || echo false)
    
    if [[ $has_retries == "false" ]]; then
        add_warning "No retry logic found. Transient failures may not be handled gracefully."
        add_suggestion "Implement retry logic with exponential backoff for network requests and external API calls."
        TOTAL_SCORE=$((TOTAL_SCORE - 10))
    fi
    
    # Check for retry count
    local retry_count
    retry_count=$(jq '.services[] | .retry_count // .max_retries // .retries // 0' "$file" 2>/dev/null | head -1)
    
    if [[ -n "$retry_count" ]] && [[ $retry_count -gt 0 ]] && [[ $retry_count -lt 3 ]]; then
        add_warning "Retry count ($retry_count) may be too low for reliable recovery."
        add_suggestion "Consider increasing retry count or implementing exponential backoff strategy."
    fi
}

check_retries_ini() {
    local file=$1
    
    # Check for retry configurations
    if ! grep -q "retry" "$file"; then
        add_warning "No retry logic found. Transient failures may not be handled gracefully."
        add_suggestion "Implement retry logic with exponential backoff for network requests and external API calls."
        TOTAL_SCORE=$((TOTAL_SCORE - 8))
    fi
}

check_health_checks_json() {
    local file=$1
    
    # Check for health check configurations
    local has_health_checks
    has_health_checks=$(jq 'any(.services[]; has("health_check") or has("healthCheck") or has("health") or has("liveness_probe") or has("readiness_probe"))' "$file" 2>/dev/null || echo false)
    
    if [[ $has_health_checks == "false" ]]; then
        add_warning "No health check configurations found. Service failures may go undetected."
        add_suggestion "Implement health checks for all services to enable automatic failure detection and recovery."
        TOTAL_SCORE=$((TOTAL_SCORE - 10))
    fi
}

check_load_balancing_json() {
    local file=$1
    
    # Check for load balancing configurations
    local has_load_balancer
    has_load_balancer=$(jq 'any(.services[]; has("load_balancer") or has("loadBalancer") or .type == "load_balancer" or .type == "lb")' "$file" 2>/dev/null || echo false)
    
    if [[ $has_load_balancer == "false" ]]; then
        add_warning "No load balancing configuration found. Traffic may not be distributed evenly."
        add_suggestion "Implement load balancing to distribute traffic and improve system resilience."
        TOTAL_SCORE=$((TOTAL_SCORE - 5))
    fi
}

add_critical_issue() {
    CRITICAL_ISSUES+=("$1")
}

add_warning() {
    WARNINGS+=("$1")
}

add_suggestion() {
    SUGGESTIONS+=("$1")
}

print_results() {
    local file=$1
    
    echo -e "${BOLD}File:${NC} $file"
    echo -e "${BOLD}Resilience Score:${NC} $TOTAL_SCORE/100"
    echo
    
    # Critical Issues
    if [[ ${#CRITICAL_ISSUES[@]} -gt 0 ]]; then
        echo -e "${RED}${BOLD}Critical Issues:${NC}"
        for issue in "${CRITICAL_ISSUES[@]}"; do
            echo -e "${RED}❌${NC} $issue"
        done
        echo
    fi
    
    # Warnings
    if [[ ${#WARNINGS[@]} -gt 0 ]]; then
        echo -e "${YELLOW}${BOLD}Warnings:${NC}"
        for warning in "${WARNINGS[@]}"; do
            echo -e "${YELLOW}⚠️${NC} $warning"
        done
        echo
    fi
    
    # Suggestions
    if [[ ${#SUGGESTIONS[@]} -gt 0 ]]; then
        echo -e "${GREEN}${BOLD}Suggestions:${NC}"
        for suggestion in "${SUGGESTIONS[@]}"; do
            echo -e "${GREEN}💡${NC} $suggestion"
        done
        echo
    fi
    
    # Final message
    if [[ $TOTAL_SCORE -ge 80 ]]; then
        echo -e "${GREEN}Excellent chaos readiness! Your system is well-prepared for failure. 🚀${NC}"
    elif [[ $TOTAL_SCORE -ge 60 ]]; then
        echo -e "${YELLOW}Good chaos readiness, but there's room for improvement. Keep going! 💪${NC}"
    elif [[ $TOTAL_SCORE -ge 40 ]]; then
        echo -e "${YELLOW}Moderate chaos readiness. Significant improvements needed. 🔧${NC}"
    else
        echo -e "${RED}Poor chaos readiness. Critical issues must be addressed immediately! 🚨${NC}"
    fi
    
    echo -e "${CYAN}Remember: In chaos, we find order. In failure, we find strength! 🎭${NC}"
}

validate_file() {
    local file=$1
    local ext
    ext=$(get_file_extension "$file")
    
    log INFO "Validating: $file (format: $ext)"
    
    case $ext in
        json)
            validate_json "$file"
            ;;
        yaml|yml)
            validate_yaml "$file"
            ;;
        ini)
            validate_ini "$file"
            ;;
        *)
            log ERROR "Unsupported file format: $ext"
            log ERROR "Supported formats: JSON, YAML, INI"
            return 1
            ;;
    esac
}

main() {
    local files=()
    VERBOSE=false
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --help|-h)
                print_help
                exit 0
                ;;
            --verbose|-v)
                VERBOSE=true
                shift
                ;;
            -*|--*)
                log ERROR "Unknown option: $1"
                print_help
                exit 1
                ;;
            *)
                files+=("$1")
                shift
                ;;
        esac
    done
    
    # Check if jq is available
    if ! command -v jq &> /dev/null; then
        log ERROR "jq is required but not installed. Please install jq: https://stedolan.github.io/jq/"
        exit 1
    fi
    
    # Check if Python 3 is available
    if ! command -v python3 &> /dev/null; then
        log ERROR "Python 3 is required but not installed."
        exit 1
    fi
    
    # Check if files were provided
    if [[ ${#files[@]} -eq 0 ]]; then
        log ERROR "No files specified."
        print_help
        exit 1
    fi
    
    print_header
    
    # Process each file
    for file in "${files[@]}"; do
        # Reset scores and issues for each file
        TOTAL_SCORE=100
        CRITICAL_ISSUES=()
        WARNINGS=()
        SUGGESTIONS=()
        
        # Validate file exists
        if ! check_file_exists "$file"; then
            continue
        fi
        
        # Validate file
        validate_file "$file"
        
        # Print results
        print_results "$file"
        echo
        echo "---"
        echo
    done
}

# Run main function with all arguments
main "$@"
