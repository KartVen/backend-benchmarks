#!/bin/bash

CONTAINER_NAME=$1
OUT_FILE=$2
DURATION=$3
INTERVAL=${4:-0.5}

export LC_NUMERIC=C

echo "timestamp,cpu%,mem_usage,mem%" > "$OUT_FILE"

CONTAINER_ID=$(docker inspect --format '{{.Id}}' "$CONTAINER_NAME" 2>/dev/null)
if [ -z "$CONTAINER_ID" ]; then
    echo "Failed to get container ID for $CONTAINER_NAME"
    exit 1
fi
echo "Monitoring container: $CONTAINER_NAME (${CONTAINER_ID:0:12})"

CGROUP_DIR=$(find /sys/fs/cgroup/ -type d -name "*${CONTAINER_ID:0:12}*" 2>/dev/null | head -n 1)

if [ -z "$CGROUP_DIR" ]; then
    echo "Cgroup directory not found for container ID: ${CONTAINER_ID:0:12}"
    exit 1
fi

CPU_FILE="$CGROUP_DIR/cpu.stat"
CPU_MAX_FILE="$CGROUP_DIR/cpu.max"
MEM_FILE="$CGROUP_DIR/memory.current"
MEM_MAX_FILE="$CGROUP_DIR/memory.max"

if [ ! -f "$CPU_FILE" ] || [ ! -f "$CPU_MAX_FILE" ] || [ ! -f "$MEM_FILE" ] || [ ! -f "$MEM_MAX_FILE" ]; then
    echo "Missing required cgroup files:"
    [ ! -f "$CPU_FILE" ] && echo "- $CPU_FILE"
    [ ! -f "$CPU_MAX_FILE" ] && echo "- $CPU_MAX_FILE"
    [ ! -f "$MEM_FILE" ] && echo "- $MEM_FILE"
    [ ! -f "$MEM_MAX_FILE" ] && echo "- $MEM_MAX_FILE"
    exit 1
fi

read quota period < "$CPU_MAX_FILE"
if [ "$quota" = "max" ]; then
    NUM_CORES=$(nproc)
else
    NUM_CORES=$(echo "scale=4; $quota / $period" | bc)
fi

INTERVAL_MICRO=$(echo "$INTERVAL * 1000000" | bc | cut -d'.' -f1)

prev_cpu=$(awk '/usage_usec/ {print $2}' "$CPU_FILE")

if grep -q '^max$' "$MEM_MAX_FILE"; then
    total_mem=$(grep MemTotal /proc/meminfo | awk '{print $2 * 1024}')
else
    total_mem=$(cat "$MEM_MAX_FILE")
fi

start_time=$(date +%s.%N)
end_time=$(echo "$start_time + $DURATION" | bc)

END_TIME=$((SECONDS + DURATION))

while [ $SECONDS -lt $END_TIME ]; do
    sleep "$INTERVAL"

    now_time=$(date +%s.%N)
    if (( $(echo "$now_time >= $end_time" | bc -l) )); then
        break
    fi

    curr_cpu=$(awk '/usage_usec/ {print $2}' "$CPU_FILE")
    mem_bytes=$(cat "$MEM_FILE")

    cpu_delta=$((curr_cpu - prev_cpu))
    cpu_pct=$(echo "scale=6; $cpu_delta / $INTERVAL_MICRO / $NUM_CORES * 100" | bc | sed 's/^\./0./' | xargs printf "%.2f")

    mem_mib=$(echo "scale=2; $mem_bytes / 1024 / 1024" | bc)
    mem_gib=$(echo "scale=2; $total_mem / 1024 / 1024 / 1024" | bc)
    mem_pct=$(echo "scale=2; $mem_bytes * 100 / $total_mem" | bc)

    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "$timestamp,${cpu_pct}%,${mem_mib}MiB / ${mem_gib}GiB,${mem_pct}%" >> "$OUT_FILE"

    prev_cpu=$curr_cpu
done
