#!/bin/bash

awk '{ print $1 }' students.txt
awk '{ print $2 }' students.txt
awk '{ print $NR}' students.txt
