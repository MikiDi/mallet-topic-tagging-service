#!/bin/bash

cd /usr/src/mallet

time bin/mallet import-dir --input $INPUT_PATH --output $OUTPUT_PATH/corpus.mallet --keep-sequence --use-pipe-from $TRAIN_PATH/processed/corpus.mallet
