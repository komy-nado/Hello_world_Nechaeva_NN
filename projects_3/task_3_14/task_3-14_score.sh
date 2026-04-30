#!/bin/bash

awk '{ if($2>80) print $1 }' students.txt
awk '{ if($2<70) print $1 }' students.txt
awk '{ if($2==78) print $0 }' students.txt

