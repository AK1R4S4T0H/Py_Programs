#!/bin/bash

PUR='\033[0;32m'
NC='\033[0m' # no color

load_length=20

for i in $(seq 1 $load_length); do
  progress=$(echo "scale=2; $i/$load_length * 9001" | bc)
  complete=$((i * 75 / load_length))
  remaining=$((75 - complete))
  completed_symbols=$(printf ">%.0s" $(seq 1 $complete))
  printf "${PUR}\rLoading... [%s%-${remaining}s] %s%%" "$completed_symbols" "" "$progress"
  sleep 0.1
done

printf "\n"

