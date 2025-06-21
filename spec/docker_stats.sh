#!/bin/bash

CONTAINER_NAME=$1
OUT_FILE=$2
DURATION=$3           # ile sekund monitorować (np. 60)
INTERVAL=${4:-0.5}      # co ile sekund (domyślnie 1s)

echo "timestamp,cpu%,mem_usage,mem%" > "$OUT_FILE"

END_TIME=$((SECONDS + DURATION))

while [ $SECONDS -lt $END_TIME ]; do
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    STATS=$(docker stats --no-stream --format "{{.CPUPerc}},{{.MemUsage}},{{.MemPerc}}" "$CONTAINER_NAME")

    if [ -z "$STATS" ]; then
        echo "Error reading container stats for $CONTAINER_NAME"
        break
    fi

    echo "$TIMESTAMP,$STATS" >> "$OUT_FILE"
    sleep "$INTERVAL"
done
