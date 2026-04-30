#!/bin/bash

awk '{ print $2 }' data2.xlsx
awk '{ if($3>20) print $2 }' data2.xlsx
awk '{sum += $3;n++} END {print sum}' data2.xlsx
