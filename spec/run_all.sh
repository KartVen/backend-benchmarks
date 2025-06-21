#!/bin/bash

ENDPOINT=$1
OUT_DIR=/media/kartven/Backup\ Drive/spec
LOG_DIR="$OUT_DIR/logs"

mkdir -p "$LOG_DIR"

screen -dmS php \
  -L -Logfile "$LOG_DIR/screenlog.php.$ENDPOINT.0" \
  bash -c "OUT_DIR=\"$OUT_DIR\" ./tests_opt.sh php $ENDPOINT benchmark-php-benchmark-php-1 8084 30 1 30 10 20 50 100 200 500 1000 2000"

screen -dmS java \
  -L -Logfile "$LOG_DIR/screenlog.java.$ENDPOINT.0" \
  bash -c "OUT_DIR=\"$OUT_DIR\" ./tests_opt.sh java $ENDPOINT benchmark-java-benchmark-java-1 8081 30 1 30 10 20 50 100 200 500 1000 2000"

screen -dmS cs \
  -L -Logfile "$LOG_DIR/screenlog.cs.$ENDPOINT.0" \
  bash -c "OUT_DIR=\"$OUT_DIR\" ./tests_opt.sh csharp $ENDPOINT benchmark-csharp-benchmark-csharp-1 8082 30 1 30 10 20 50 100 200 500 1000 2000"

screen -dmS py \
  -L -Logfile "$LOG_DIR/screenlog.py.$ENDPOINT.0" \
  bash -c "OUT_DIR=\"$OUT_DIR\" ./tests_opt.sh python $ENDPOINT benchmark-python-benchmark-python-1 8083 30 1 30 10 20 50 100 200 500 1000 2000"

