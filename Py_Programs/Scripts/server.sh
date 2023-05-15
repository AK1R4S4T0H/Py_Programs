#!/bin/bash
# Simple bash script for launching a python http server
# in the current Directory, press ENTER to stop server
# also auto opens your default web browser to he server
# alternatively you could pu this as a function in your .bashrc
# if you want to use a different port, change all instances of 8877
# or as an alias with the path to the file
# examples: alias server = "/path/to/script"
# or 
#
# function server() {the code below between these and add the funciton to .bashrc}
python3 -m http.server 8877 &
DIR=$(pwd)
echo "Server is running at: http://localhost:8877"
python3 -m webbrowser -t "http://localhost:8877"
read -rp "Press Enter to stop the server" </dev/tty
kill $(lsof -t -i:8877)