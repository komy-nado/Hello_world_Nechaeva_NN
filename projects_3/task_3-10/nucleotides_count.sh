#!/bin/bash

printf "%-15s %-7s %-7s %-7s %-7s\n" "Файл" "A" "T" "G" "C"

for file in *.fasta; do
	if  [ ! -s "$file" ]; 
	then continue;
	fi

	seq=$(grep -v "^>" "$file"|  tr -d '\n')

	a=$(echo -n "$seq" | grep -o "A" | wc -l)
	t=$(echo -n "$seq" | grep -o "T" | wc -l)
	g=$(echo -n "$seq" | grep -o "G" | wc -l)
	c=$(echo -n "$seq" | grep -o "C" | wc -l)

printf "%-15s %-7s %-7s %-7s %-7s\n" "$file" "$a" "$t" "$g" "$c"

done
