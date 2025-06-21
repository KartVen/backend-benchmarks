#!/bin/bash

FRAMEWORK=$1      # np. java
ENDPOINT=$2       # np. ping
CONTAINER=$3      # np. benchmark-java-benchmark-java-1
PORT=$4           # np. 8081
VUS=$5            # np. 10
DURATION=$6       # np. 60
STEP=$7           # np. 1..30

OUT_DIR=${OUT_DIR:-"."}

CSV_OUT="$OUT_DIR/metrics/${FRAMEWORK}/${ENDPOINT}_${VUS}_${DURATION}_step_${STEP}.csv"
SUMMARY_OUT="$OUT_DIR/metrics/${FRAMEWORK}/${ENDPOINT}_${VUS}_${DURATION}_summary_step_${STEP}.json"
STATS_OUT="$OUT_DIR/cpu_mem/${FRAMEWORK}/cpu_mem_${FRAMEWORK}_${ENDPOINT}_${VUS}_${DURATION}_step_${STEP}.csv"

mkdir -p "$(dirname "$CSV_OUT")"
mkdir -p "$(dirname "$STATS_OUT")"

./cgroup_stats.sh "$CONTAINER" "$STATS_OUT" "$((DURATION+1))" 0.5 &

VUS=$VUS DURATION=${DURATION}s PORT=$PORT k6 run k6/test_${ENDPOINT}.js \
    --out csv="$CSV_OUT" \
    --summary-export="$SUMMARY_OUT" \
    --address="127.0.0.1:0" \
    --no-usage-report

wait
