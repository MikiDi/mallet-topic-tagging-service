#!/bin/bash

echo "Setting up memory"
/setup-memory.sh

mkdir -p $INPUT_PATH
mkdir -p $OUTPUT_PATH

echo "Importing directory"
/import-directory.sh

echo "Inferring topics"
/infer-topics.sh

cat /tmp/mallet-data/output-data/output.txt
