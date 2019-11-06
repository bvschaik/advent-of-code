#!/usr/bin/env bash

for f in day*.py
do
    INPUT=input/${f:3:2}.txt
    python3 $f skip-test < $INPUT
done