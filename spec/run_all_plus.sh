#!/bin/bash

ENDPOINT=$1
OUT_DIR=/mnt/HC_Volume_102825035/spec
LOG_DIR="$OUT_DIR/logs"

mkdir -p "$LOG_DIR"

screen -dmS php \
  -L -Logfile "$LOG_DIR/screenlog.php.$ENDPOINT.0.plus" \
  bash -c "OUT_DIR=\"$OUT_DIR\" ./tests.sh php $ENDPOINT benchmark-php-benchmark-php-2 8088 30 1 30 2000 5000 10000"

screen -dmS java \
  -L -Logfile "$LOG_DIR/screenlog.java.$ENDPOINT.0.plus" \
  bash -c "OUT_DIR=\"$OUT_DIR\" ./tests.sh java $ENDPOINT benchmark-java-benchmark-java-2 8085 30 1 30 2000 5000 10000"

screen -dmS cs \
  -L -Logfile "$LOG_DIR/screenlog.cs.$ENDPOINT.0.plus" \
  bash -c "OUT_DIR=\"$OUT_DIR\" ./tests.sh csharp $ENDPOINT benchmark-csharp-benchmark-csharp-2 8086 30 1 30 2000 5000 10000"

screen -dmS py \
  -L -Logfile "$LOG_DIR/screenlog.py.$ENDPOINT.0.plus" \
  bash -c "OUT_DIR=\"$OUT_DIR\" ./tests.sh python $ENDPOINT benchmark-python-benchmark-python-2 8087 30 1 30 2000 5000 10000"
