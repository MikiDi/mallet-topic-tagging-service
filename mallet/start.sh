#!/bin/bash

echo "Setting up memory"
/setup-memory.sh

mkdir -p $INPUT_PATH
mkdir -p $OUTPUT_PATH

echo "Importing directory"
/import-directory.sh

echo "Inferring topics"
/infer-topics.sh

echo "Clearing input files"
rm -rf $INPUT_PATH/*

#cat /tmp/mallet-data/output-data/output.txt
