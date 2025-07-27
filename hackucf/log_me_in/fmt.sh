#!/bin/sh

for i in $(seq 1 30); do
    #printf "%%%d\$p => " "$i"
    printf "%%%d\$p\n" "$i" | ./logmein
done