#!/bin/bash

cd /usr/src/mallet

time bin/mallet infer-topics --inferencer $TRAIN_PATH/topics/inferencer --input $OUTPUT_PATH/corpus.mallet --output-doc-topics $OUTPUT_PATH/output.txt --doc-topics-threshold 0.001
