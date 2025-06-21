#!/bin/bash

OUT_DIR=/mnt/HC_Volume_102825035/spec
LOG_DIR="$OUT_DIR/logs"

mkdir -p "$LOG_DIR"

ENDPOINT=$1
screen -dmS php1 \
  -L -Logfile "$LOG_DIR/screenlog.php.$ENDPOINT.0" \
  bash -c "OUT_DIR=\"$OUT_DIR\" ./tests.sh php $ENDPOINT benchmark-php-benchmark-php-5 8084 30 1 30 10 20 50 100 200 500 1000"

ENDPOINT=$2
screen -dmS php2 \
  -L -Logfile "$LOG_DIR/screenlog.php.$ENDPOINT.0" \
  bash -c "OUT_DIR=\"$OUT_DIR\" ./tests.sh php $ENDPOINT benchmark-php-benchmark-php-6 8085 30 1 30 10 20 50 100 200 500 1000"

ENDPOINT=$3
screen -dmS php3 \
  -L -Logfile "$LOG_DIR/screenlog.php.$ENDPOINT.0" \
  bash -c "OUT_DIR=\"$OUT_DIR\" ./tests.sh php $ENDPOINT benchmark-php-benchmark-php-7 8086 30 1 30 10 20 50 100 200 500 1000"

ENDPOINT=$4
screen -dmS php4 \
  -L -Logfile "$LOG_DIR/screenlog.php.$ENDPOINT.0" \
  bash -c "OUT_DIR=\"$OUT_DIR\" ./tests.sh php $ENDPOINT benchmark-php-benchmark-php-8 8087 30 1 30 10 20 50 100 200 500 1000"
