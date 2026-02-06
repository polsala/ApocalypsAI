#!/usr/bin/env bash\n# nightly-docker-rot13 – apply ROT13 to STDIN and output to STDOUT\n# No external tools required beyond GNU tr, which is present in Alpine.\n\ntr 'A-Za-z' 'N-ZA-Mn-za-m'\n
