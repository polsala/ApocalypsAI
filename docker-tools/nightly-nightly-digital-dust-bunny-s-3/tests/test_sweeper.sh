#!/bin/bash

set -euo pipefail

# Define colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "Running tests for Nightly Digital Dust Bunny Sweeper..."

# Test 1: Report mode output
echo -e "\n${GREEN}--- Test 1: Report Mode ---${NC}"
REPORT_OUTPUT=$(MOCK_DOCKER=true bash src/dust_bunny_sweeper.sh report)

# Check for expected phrases in report mode
if echo "$REPORT_OUTPUT" | grep -q "Found these dusty image bunnies:"; then
    echo -e "${GREEN}PASS: Found expected image bunny message.${NC}"
else
    echo -e "${RED}FAIL: Did not find expected image bunny message in report mode.${NC}"
    echo "$REPORT_OUTPUT"
    exit 1
fi

if echo "$REPORT_OUTPUT" | grep -q "Discovered these snoozing container critters:"; then
    echo -e "${GREEN}PASS: Found expected container critter message.${NC}"
else
    echo -e "${RED}FAIL: Did not find expected container critter message in report mode.${NC}"
    echo "$REPORT_OUTPUT"
    exit 1
fi

if echo "$REPORT_OUTPUT" | grep -q "Uncovered these forgotten volume trinkets:"; then
    echo -e "${GREEN}PASS: Found expected volume trinket message.${NC}"
else
    echo -e "${RED}FAIL: Did not find expected volume trinket message in report mode.${NC}"
    echo "$REPORT_OUTPUT"
    exit 1
fi

if echo "$REPORT_OUTPUT" | grep -q "Currently in 'report' mode. No changes were made."; then
    echo -e "${GREEN}PASS: Found expected report mode disclaimer.${NC}"
else
    echo -e "${RED}FAIL: Did not find expected report mode disclaimer.${NC}"
    echo "$REPORT_OUTPUT"
    exit 1
fi

# Test 2: Clean mode output
echo -e "\n${GREEN}--- Test 2: Clean Mode ---${NC}"
CLEAN_OUTPUT=$(MOCK_DOCKER=true bash src/dust_bunny_sweeper.sh clean)

# Check for expected phrases in clean mode
if echo "$CLEAN_OUTPUT" | grep -q "Initiating the grand sweep! Prepare for digital tidiness!"; then
    echo -e "${GREEN}PASS: Found expected sweep initiation message.${NC}"
else
    echo -e "${RED}FAIL: Did not find expected sweep initiation message in clean mode.${NC}"
    echo "$CLEAN_OUTPUT"
    exit 1
fi

if echo "$CLEAN_OUTPUT" | grep -q "Sweeping away dangling images..."; then
    echo -e "${GREEN}PASS: Found expected image sweep message.${NC}"
else
    echo -e "${RED}FAIL: Did not find expected image sweep message in clean mode.${NC}"
    echo "$CLEAN_OUTPUT"
    exit 1
fi

if echo "$CLEAN_OUTPUT" | grep -q "Evicting stopped containers..."; then
    echo -e "${GREEN}PASS: Found expected container eviction message.${NC}"
else
    echo -e "${RED}FAIL: Did not find expected container eviction message in clean mode.${NC}"
    echo "$CLEAN_OUTPUT"
    exit 1
fi

if echo "$CLEAN_OUTPUT" | grep -q "Reclaiming unused volumes..."; then
    echo -e "${GREEN}PASS: Found expected volume reclaim message.${NC}"
else
    echo -e "${RED}FAIL: Did not find expected volume reclaim message in clean mode.${NC}"
    echo "$CLEAN_OUTPUT"
    exit 1
fi

if echo "$CLEAN_OUTPUT" | grep -q "The digital realm is now pristine! Enjoy your reclaimed space!"; then
    echo -e "${GREEN}PASS: Found expected completion message.${NC}"
else
    echo -e "${RED}FAIL: Did not find expected completion message in clean mode.${NC}"
    echo "$CLEAN_OUTPUT"
    exit 1
fi

echo -e "\n${GREEN}All tests passed!${NC}"
