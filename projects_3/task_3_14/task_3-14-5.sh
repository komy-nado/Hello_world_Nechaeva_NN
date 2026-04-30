#!/bin/bash


df -h | awk '
NR==1 { next }
{
    fs = $1
    pct = $5
    gsub(/%/, "", pct)

    print fs, pct "%"

    if (pct ~ /^[0-9]+$/ && pct+0 > 90) {
        printf "WARNING: ФС %s переполнена более чем на 90%%\n", fs > "/dev/stderr"
    }
}'
