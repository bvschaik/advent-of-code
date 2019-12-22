#!/usr/bin/env bash

for f in day*.py
do
	python3 $f skip-test
done
