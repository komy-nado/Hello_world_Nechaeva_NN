#!/bin/bash

for i in {1..10}; do
	touch "test${i}.txt"
done
for i in {10..1}; do
rm "test${i}.txt"
done
