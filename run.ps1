# Health Coach Startup Script
# This script clears the SSLKEYLOGFILE environment variable to avoid permission issues

$env:SSLKEYLOGFILE = ""
python main.py
