#!/bin/bash

echo "Setting up memory"
/setup-memory.sh

mkdir -p $INPUT_PATH #/tmp/mallet-data/input-files
mkdir -p /tmp/mallet-data/output-data

echo "Importing directory"
/import-directory.sh

echo "Inferring topics"
/infer-topics.sh

cat /tmp/mallet-data/output-data/output.txt
