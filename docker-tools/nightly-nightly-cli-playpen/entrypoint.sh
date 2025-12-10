#!/bin/sh

cat << 'EOF'

  _____ _                 _   _            
 |  __ (_)               | | | |           
 | |__) | ___  ___ _ __ | |_| |__   ___   
 |  ___/ / _ \/ _ \ '_ \| __| '_ \ / _ \  
 | |   | |  __/  __/ | | | |_| | | | (_) | 
 |_|   |_|\___|\___|_| |_|\__|_| |_|\___/  
                                            
EOF

# Show motivational message
fortune | cowsay

# Execute command or start shell
exec "$@"
