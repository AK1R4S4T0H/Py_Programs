#!/bin/bash

# Simple bash script for launching a python http server
# in the current Directory, press ENTER to stop server
# also auto opens your default web browser to he server
# alternatively you could put this as a function in your .bashrc
# or as an alias with the path to the file
# examples: alias server = "/path/to/script"

read -rp "Enter the port number (default: 8877): " port
port=${port:-8877}

start_server() {
  python3 -m http.server "$port" --bind 127.0.0.1 --directory "$DIR" >/dev/null 2>&1
}

DIR=$(pwd)

start_server &
server_pid=$!
server_url="http://localhost:$port"
echo "Server is running at: $server_url"

python3 -m webbrowser -t "$server_url"

echo "Press Enter to stop the server"
read -r

kill "$server_pid" 2>/dev/null

