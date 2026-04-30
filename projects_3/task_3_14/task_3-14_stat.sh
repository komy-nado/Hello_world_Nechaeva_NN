#!/bin/bash

awk '{sum += $2;n++} END {print sum}' students.txt
awk '{sum += $2;n++} END {print sum/n}' students.txt
awk 'NR==1{max=$2} $2>max{max=$2} END{print max}' students.txt
