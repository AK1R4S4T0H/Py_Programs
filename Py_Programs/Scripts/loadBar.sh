#!/bin/bash
# loading Bar to 9001
PUR='\033[0;32m' # color value
NC='\033[0m' # no color

load_length=20 # edit here

for i in $(seq 1 $load_length); do
  progress=$(echo "scale=2; $i/$load_length * 9001" | bc) # edit 9001 to whatever
  complete=$((i * 75 / load_length)) # here
  remaining=$((75 - complete)) # and here to change how long it is
  completed_symbols=$(printf ">%.0s" $(seq 1 $complete)) # change > if you want diff. symbol to print
  printf "${PUR}\rLoading... [%s%-${remaining}s] %s%%" "$completed_symbols" "" "$progress"
  sleep 0.1
done

printf "\n"

