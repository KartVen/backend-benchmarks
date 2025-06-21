#!/bin/bash

FRAMEWORK=$1 # java / csharp / python / php
ENDPOINT=$2 # ping / fibonacci
CONTAINER=$3
PORT=$4
DURATION=$5
STEP_START=$6
STEP_STOP=$7
VUS_LIST=("${@:8}")

APP_STABILIZE_TIME=5

echo "=== Start tests ==="

for VUS in "${VUS_LIST[@]}"; do
  echo "Step: VUS=$VUS"

  for STEP in $(seq "$STEP_START" "$STEP_STOP"); do
    echo "$CONTAINER stopping..."
    docker stop "$CONTAINER" > /dev/null
    sleep 15

    echo "$CONTAINER starting..."
    docker start ${CONTAINER} > /dev/null

    START_TS=$(date --iso-8601=seconds)

    echo "Waiting to start $FRAMEWORK's app..."
    #case "$FRAMEWORK" in
    #java) REGEX="Started BenchmarkApplication in" ;;
    #python) REGEX="Watching for file changes with StatReloader" ;;
    #php) REGEX="NOTICE: ready to handle connections" ;;
    #php) REGEX="Server running on" ;;
    #esac

    timeout=90
    elapsed=0

    until curl -s -o /dev/null -w "%{http_code}" "http://localhost:$PORT/ping" | grep -q "200"; do
      sleep 2
      elapsed=$((elapsed+2))
      if [ "$elapsed" -ge "$timeout" ]; then
        echo "Timeout: $FRAMEWORK did not start in $timeout seconds"
        exit 1
      fi
    done
    sleep "$APP_STABILIZE_TIME"
    echo "Started $FRAMEWORK's app in (${elapsed} + $APP_STABILIZE_TIME)s"

    ./test.sh "$FRAMEWORK" "$ENDPOINT" "$CONTAINER" "$PORT" "$VUS" "$DURATION" "$STEP"
  done
done

echo "=== Done tests ==="
