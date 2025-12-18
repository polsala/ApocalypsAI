#!/usr/bin/env bash
set -euo pipefail

# Test that script outputs a quote from default list
output=$(./src/quote.sh)
case "$output" in
    \"Believe you can and you're halfway there.\"|\
    \"The only limit to our realization of tomorrow is our doubts of today.\"|\
    \"Do not wait to strike till the iron is hot; but make it hot by striking.\") 
        echo \"PASS default\"
        ;;
    *) echo \"FAIL default: $output\" && exit 1
esac

# Test with custom quotes file
echo -e \"Custom quote 1\nCustom quote 2\" > quotes.txt
output=$(./src/quote.sh)
case "$output" in
    \"Custom quote 1\"|\"Custom quote 2\") echo \"PASS custom\";;
    *) echo \"FAIL custom: $output\" && exit 1
esac
rm quotes.txt
